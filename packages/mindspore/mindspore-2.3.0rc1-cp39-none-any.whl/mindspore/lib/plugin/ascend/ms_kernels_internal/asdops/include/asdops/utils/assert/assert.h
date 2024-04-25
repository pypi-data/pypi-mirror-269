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
#ifndef ASDOPS_UTILS_ASSERT_ASSERT_H
#define ASDOPS_UTILS_ASSERT_ASSERT_H

#include "asdops/utils/log/log.h"

namespace AsdOps {
namespace Utils {
#define ASDOPS_CHECK(condition, logExpr, handleExpr)                                                                   \
    if (!(condition)) {                                                                                                \
        ASD_LOG(ERROR) << logExpr;                                                                                     \
        handleExpr;                                                                                                    \
    }

#define ASDOPS_CHECK_NO_LOG(condition, handleExpr)                                                                     \
    if (!(condition)) {                                                                                                \
        handleExpr;                                                                                                    \
    }
}
} // namespace AsdOps
#endif