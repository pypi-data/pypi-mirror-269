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
#ifndef ASDOPS_OPS_H
#define ASDOPS_OPS_H
#include <vector>
#include <string>
#include <memory>
#include "asdops/tensor.h"
#include "asdops/op_desc.h"
#include "asdops/run_info.h"
#include "asdops/operation.h"
#include "asdops/tactic.h"

namespace AsdOps {
class OpSchedule;

class Ops {
public:
    /**
     * @brief Return the singleton object
     *
     * @return Ops&
     */
    static Ops &Instance();
    /**
     * @brief Get the All Operations object
     *
     * @param[std::vector<Operation *> &] ops
     */
    void GetAllOperations(std::vector<Operation *> &ops) const;
    /**
     * @brief Get the Operation By Name object
     *
     * @param[const std::string&] opName
     * @return Operation*
     */
    Operation *GetOperationByName(const std::string &opName) const;
    /**
     * @brief Get the Operation By Id object
     *
     * @param[uint64_t] opId
     * @return Operation*
     */
    Operation *GetOperationById(uint64_t opId) const;
    /**
     * @brief Get the Tactic By Name object
     *
     * @param[const std::string &] tacticName
     * @return Tactic*
     */
    Tactic *GetTacticByName(const std::string &tacticName) const;
    /**
     * @brief Get the Tactic By Id object
     *
     * @param[uint64_t] tacticId
     * @return Tactic*
     */
    Tactic *GetTacticById(uint64_t tacticId) const;

private:
    Ops();
    ~Ops();

private:
    std::unique_ptr<OpSchedule> opSchedule_;
};
} // namespace AsdOps

#endif