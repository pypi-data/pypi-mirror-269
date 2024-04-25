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
#ifndef CORE_BASE_OPERATION_REGISTER_H
#define CORE_BASE_OPERATION_REGISTER_H

#include <map>
#include <vector>

#include "asdops/operation.h"
#include "asdops/tactic.h"
#include "asdops/utils/assert/assert.h"
#include "asdops/utils/log/log.h"

namespace AsdOps {
using NewOperationFunc = Operation*(*)();
using NewTacticFunc = Tactic*(*)();

class OperationRegister {
public:
    OperationRegister(const char *opName, NewOperationFunc func) noexcept
    {
        ASDOPS_CHECK(opName != nullptr, "opName is nullptr", return);
        auto &operationCreators = OperationCreators();
        operationCreators.push_back(func);
        ASD_LOG(INFO) << "register operation " << opName;
    }

    OperationRegister(const char *opName, const char *tacName, NewTacticFunc func) noexcept
    {
        ASDOPS_CHECK(opName != nullptr, "opName is nullptr", return);
        ASDOPS_CHECK(tacName != nullptr, "tacName is nullptr", return);
        auto &tacticCreators = TacticCreators();
        tacticCreators[func] = opName;
        ASD_LOG(INFO) << "register tactic " << tacName << " of operation " << opName;
    }

    static std::vector<NewOperationFunc> &OperationCreators()
    {
        static std::vector<NewOperationFunc> operationCreators;
        return operationCreators;
    }

    static std::map<NewTacticFunc, std::string> &TacticCreators()
    {
        static std::map<NewTacticFunc, std::string> tacticCreators;
        return tacticCreators;
    }
};

#define REG_OPERATION(opName)                                                   \
    Operation *GetOperation##opName()                                           \
    {                                                                           \
        static opName op##opName(#opName);                                      \
        return &op##opName;                                                     \
    }                                                                           \
    static OperationRegister opName##register =                                 \
        OperationRegister(#opName, GetOperation##opName)

#define REG_TACTIC(tacName)                                                     \
    Tactic *GetTactic##tacName()                                                \
    {                                                                           \
        static tacName tac##tacName(#tacName);                                  \
        return &tac##tacName;                                                   \
    }                                                                           \
    static OperationRegister tacName##register =                                \
        OperationRegister(OperationPlaceHolder, #tacName, GetTactic##tacName)
}

#endif