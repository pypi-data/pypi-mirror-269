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
#ifndef ASDOPS_PARAMS_MULTINOMIAL_H
#define ASDOPS_PARAMS_MULTINOMIAL_H

#include <string>
#include <sstream>

namespace AsdOps {
namespace OpParam {
struct Multinomial {
    uint32_t numSamples = 1;
    uint32_t randSeed = 0;
    bool operator==(const Multinomial &other) const
    {
        if (this->randSeed == 0xffffffff || other.randSeed == 0xffffffff) {
            return false;
        }
        return (this->numSamples == other.numSamples) && (this->randSeed == other.randSeed);
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif