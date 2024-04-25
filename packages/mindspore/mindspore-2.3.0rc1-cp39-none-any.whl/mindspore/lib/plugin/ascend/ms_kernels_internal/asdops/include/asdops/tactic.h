/**
 * Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef ASDOPS_TACTIC_H
#define ASDOPS_TACTIC_H

#include <string>
#include <vector>
#include "asdops/launch_param.h"
#include "asdops/run_info.h"
#include "asdops/utils/status/status.h"

namespace AsdOps {
class Tactic {
public:
    Tactic() = default;
    virtual ~Tactic() = default;
    virtual std::string GetName() const = 0;
    virtual uint64_t GetId() const = 0;

    virtual bool CanSupport(const LaunchParam &launchParam) const = 0;

    virtual uint64_t GetTilingSize(const LaunchParam &launchParam) const = 0;
    virtual Status InitRunInfo(const LaunchParam &launchParam, RunInfo &runInfo) const = 0;
    virtual Status Run(const LaunchParam &launchParam, RunInfo &runInfo) = 0;

    virtual bool Serialize(std::vector<char> &hostCode, std::vector<char> &deviceCode) = 0;

    enum OpType {
        OP_TYPE_AI_CORE = 0,
        OP_TYPE_AI_CPU,
        OP_TYPE_AIV,
        OP_TYPE_WRITE_BACK,
        OP_TYPE_MIX_AIC,
        OP_TYPE_MIX_AIV,
        OP_TYPE_FFTS_PLUS,
        OP_TYPE_DSA,
        OP_TYPE_DVPP,
        OP_TYPE_HCCL,
        OP_TYPE_INVALID
    };
    virtual OpType GetType() const = 0;
};
} // namespace AsdOps

#endif