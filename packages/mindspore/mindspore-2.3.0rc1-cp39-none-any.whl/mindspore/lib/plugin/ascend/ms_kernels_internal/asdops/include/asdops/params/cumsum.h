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
#ifndef ASDOPS_PARAMS_CUMSUM_H
#define ASDOPS_PARAMS_CUMSUM_H

#include <cstdint>
#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
namespace OpParam {
struct Cumsum {
    SVector<int64_t> axis;
    bool exclusive = false;
    bool reverse = false;
    bool deterministic = false;

    bool operator==(const Cumsum &other) const
    {
        return (this->axis == other.axis) && (this->exclusive == other.exclusive) && (this->reverse == other.reverse);
    };
};
} // namespace OpParam
} // namespace AsdOps

#endif // ASDOPS_PARAMS_CUMSUM_H