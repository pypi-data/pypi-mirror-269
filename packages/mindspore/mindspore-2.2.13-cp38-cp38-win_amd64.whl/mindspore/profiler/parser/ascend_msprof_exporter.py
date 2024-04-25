# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""msprof PROF data export api file"""
import os
import shutil
import json
from json import JSONDecodeError
from collections import defaultdict
from subprocess import CalledProcessError, TimeoutExpired
from subprocess import Popen, PIPE
import csv
from mindspore import log as logger
from mindspore.profiler.common.util import get_file_path


class AscendMsprofExporter:
    """
    msprof exporter. export cann edge profiling data.

    args:
       source_path: the root path of PROF_* files

    files under prof_root_dir is like:
        profiler/PROF_*/device_{id}/data/xxx
        profiler/PROF_*/host/data/xxx
        ...

    usage:
        >> ms_exporter = AscendMsprofExporter("path/to/profiler/data")
        >> ms_exporter.export(start_time)
    """
    DRV_VERSION = 467473
    _hiai_msprof_tail = "Ascend/latest/tools/profiler/bin"
    _msprof_cmd = "msprof"
    _ascend_mark = "Ascend"
    _summary_dir = "summary"
    _timeline_dir = "timeline"
    _step_trace_mark = "step_trace"
    _op_summary_mark = "op_summary"
    _op_statistic_mark = "op_statistic"

    def __init__(self, source_path, time_out=3600):
        self._time_out = time_out
        self.source_path = source_path
        self.prof_root_dir = os.path.abspath(os.path.join(self.source_path, os.path.pardir))  # PROF*/

        self._check_msprof_env()

    def get_drv_version(self):
        """Get the drv_version for choosing the export mode."""
        host_dir = os.path.join(self.prof_root_dir, 'host')
        cmd = ['python',
               '/usr/local/Ascend/latest/tools/profiler/profiler_tool/analysis/interface/get_msprof_info.py',
               '-dir', host_dir]
        try:
            outs, _ = self._run_cmd(cmd)
            if not outs:
                logger.warning('Check the drvVersion can`t find the result, use single export mode instead.')
                return False
            result = json.loads(outs)
            logger.info('get drv_version result is : %s', result)
            status = result.get('status', 1)
            if status == 1:
                return False
            drv_version = result.get('data', {}).get('version_info', {}).get('drv_version', 0)
            if drv_version >= self.DRV_VERSION:
                return True
            return False
        except (RuntimeError, JSONDecodeError, AttributeError) as err:
            logger.warning('Get the drvVersion error, use single-export mode instead. detail : %s', err)
            return False

    def export(self, model_iteration_dict=None):
        """start_time is the time to collect PROF data"""

        flag = self.get_drv_version()
        if not flag or model_iteration_dict:
            flag = False
            if not model_iteration_dict:
                model_iteration_dict = self._generate_step_trace(self.prof_root_dir, self.source_path)

            if model_iteration_dict:
                for model_id, value in model_iteration_dict.items():
                    for iteration_id in value:
                        msprof_export_cmd = self._msprof_command_generator_old(self.prof_root_dir, model_id,
                                                                               iteration_id)
                        self._run_cmd(msprof_export_cmd)

                self._check_export_files_old(self.source_path, model_iteration_dict)
        else:
            msprof_export_cmd = self._msprof_command_generator(self.prof_root_dir)
            self._run_cmd(msprof_export_cmd)
            self._check_export_files(self.source_path)

        return flag

    def _run_cmd(self, cmd):
        """run shell command"""
        try:
            proc = Popen(cmd, stdout=PIPE, stderr=PIPE, text=True)
        except (FileNotFoundError, PermissionError, CalledProcessError) as exc:
            raise RuntimeError(exc) from exc
        try:
            outs, errs = proc.communicate(timeout=self._time_out)
        except TimeoutExpired as err:
            proc.kill()
            msg = "The possible cause is that too much data is collected " \
                  "and the export time is too long."
            logger.error(msg)
            raise TimeoutError(msg) from err
        logger.info(outs)
        return outs, errs

    def _msprof_command_generator_old(self, output, model_id=None, iter_id=None):
        """msprof export helper"""
        export_cmd = [self._msprof_cmd, "--export=on", "--output={}".format(output)]
        if isinstance(model_id, int) and model_id >= 0:
            export_cmd.append("--model-id={}".format(model_id))
        if isinstance(iter_id, int) and iter_id >= 0:
            export_cmd.append("--iteration-id={}".format(iter_id))
        return export_cmd

    def _msprof_command_generator(self, output):
        """msprof export helper"""
        return [self._msprof_cmd, "--export=on", "--output={}".format(output)]

    def _check_msprof_env(self):
        """Check the existence of msprof binary tool"""

        def _check_msprof(temp_path: str):
            if not os.path.isdir(temp_path):
                return False
            sub_files = os.listdir(temp_path)
            if self._msprof_cmd in sub_files:
                return True
            return False

        msprof_cmd = ["which", self._msprof_cmd]
        outs, _ = self._run_cmd(msprof_cmd)
        if outs != "":
            return
        logger.warning("[Profiler]The msprof command was not found. Searching from environment variables...")

        msprof_path = None
        envs = os.environ
        if envs.get("ASCEND_TOOLKIT_HOME"):
            temp_path = os.path.join(envs.get("ASCEND_TOOLKIT_HOME"), "bin")
            if _check_msprof(temp_path):
                msprof_path = temp_path

        if not msprof_path and envs.get("PATH"):
            path_list = envs.get("PATH").split(":")
            for path in path_list:
                if self._ascend_mark in path:
                    prefix = path.split(self._ascend_mark)[0]
                    temp_path = os.path.join(prefix, self._hiai_msprof_tail)
                    if _check_msprof(temp_path):
                        msprof_path = temp_path
                        break
        if msprof_path:
            envs["PATH"] = msprof_path + ":" + envs.get("PATH", "")
        else:
            raise FileNotFoundError("The msprof command was not found!")

        logger.info("The msprof command has been added to the path!")

    def _generate_step_trace(self, prof_path, device_path):
        """"generate model_id iteration_id dict"""

        summary_path = os.path.join(device_path, self._summary_dir)
        timeline_path = os.path.join(device_path, self._timeline_dir)

        self._run_cmd(self._msprof_command_generator_old(prof_path))

        if not os.path.isdir(summary_path):
            msg = "Path {} is not a existing directory. Make sure there is " \
                  "valid profiling data directory!".format(summary_path)
            raise FileNotFoundError(msg)

        step_trace_file = get_file_path(summary_path, self._step_trace_mark)

        if not step_trace_file:
            logger.info("Do not found step trace csv file in {} .".format(summary_path))
            return None

        step_trace = defaultdict(list)
        with os.fdopen(os.open(step_trace_file, os.O_RDONLY, 0o600), newline='', mode='r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for index, value in enumerate(next(reader)):
                if value == 'Model ID':
                    model_id = index
                if value == 'Iteration ID':
                    iteration_id = index
            for row in reader:
                step_trace[int(row[model_id])].append(int(row[iteration_id]))

        if os.path.isdir(summary_path):
            shutil.rmtree(summary_path)
        if os.path.isdir(timeline_path):
            shutil.rmtree(timeline_path)

        return step_trace

    def _check_export_files_old(self, source_path, step_trace):
        """Check the existence of op_summary & op_statistic files."""
        summary_path = os.path.join(source_path, self._summary_dir)
        if not os.path.isdir(summary_path):
            raise RuntimeError("Path {} is not a existing directory.".format(summary_path))
        op_summary = set()
        op_statistic = set()

        for summary_file in os.listdir(summary_path):
            if summary_file.startswith(self._op_summary_mark):
                op_summary.add(summary_file)
            elif summary_file.startswith(self._op_statistic_mark):
                op_statistic.add(summary_file)

        if not op_summary:
            raise RuntimeError("The op_summary file was not found, perhaps the original data was not collected.")
        if not op_statistic:
            raise RuntimeError("The op_statistics file was not found, perhaps the original data was not collected.")

        logger.info("Finish checking files.")

    def _check_export_files(self, source_path):
        """Check the existence of op_summary & op_statistic files."""
        summary_path = os.path.join(source_path, self._summary_dir)
        if not os.path.isdir(summary_path):
            raise RuntimeError("Path {} is not a existing directory.".format(summary_path))
        summary_file_list = os.listdir(summary_path)
        op_summary = set()
        op_statistic = set()

        for summary_file in summary_file_list:
            if summary_file.startswith(self._op_summary_mark):
                op_summary.add(summary_file)
            elif summary_file.startswith(self._op_statistic_mark):
                op_statistic.add(summary_file)

        if not op_summary:
            raise RuntimeError("The op_summary file was not found, perhaps the original data was not collected.")
        if not op_statistic:
            raise RuntimeError("The op_statistics file was not found, perhaps the original data was not collected.")
        logger.info("Finish checking files.")
