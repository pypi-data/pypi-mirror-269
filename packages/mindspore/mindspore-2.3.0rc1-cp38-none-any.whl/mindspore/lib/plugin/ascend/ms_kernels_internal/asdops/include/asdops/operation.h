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
#ifndef ASDOPS_OPERATION_H
#define ASDOPS_OPERATION_H

#include <string>
#include <vector>
#include "asdops/launch_param.h"
#include "asdops/tactic.h"
#include "asdops/utils/status/status.h"

namespace AsdOps {
class Operation {
public:
    Operation() = default;
    virtual ~Operation() = default;
    virtual std::string GetName() const = 0;
    virtual uint64_t GetId() const = 0;
    virtual void GetAllTacticNames(std::vector<std::string> &tacticNames) const = 0;
    virtual void GetAllTactics(std::vector<Tactic *> &tactics) const = 0;
    virtual AsdOps::Status InferShape(LaunchParam &launchParam) const = 0;
    virtual void GetValidTactics(const LaunchParam &launchParam, std::vector<Tactic *> &validTactics) const = 0;
    virtual Tactic *GetBestTactic(const LaunchParam &launchParam) const = 0;
    virtual uint64_t GetTacticCount() const = 0;
    virtual Tactic *GetTacticByName(const std::string &tacticName) const = 0;
    virtual Tactic *GetTacticById(uint64_t tacticId) const = 0;
    virtual int64_t GetInputNum(const OpDesc &opDesc) const = 0;
    virtual int64_t GetOutputNum(const OpDesc &opDesc) const = 0;
    virtual bool IsConsistent(const LaunchParam &launchParam) const = 0;
};
} // namespace AsdOps

#endif