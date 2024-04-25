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

#ifndef ASDOPS_PARAMS_COPY_H
#define ASDOPS_PARAMS_COPY_H

#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
namespace OpParam {
struct Copy {
    SVector<int64_t> dstSize;
    SVector<int64_t> dstStride;
    SVector<int64_t> dstOffset;

    bool operator==(const Copy &other) const
    {
        return this->dstSize == other.dstSize && this->dstStride == other.dstStride &&
               this->dstOffset == other.dstOffset;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif