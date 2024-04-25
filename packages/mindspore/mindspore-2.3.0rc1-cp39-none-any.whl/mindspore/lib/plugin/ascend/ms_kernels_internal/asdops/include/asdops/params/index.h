/**
 * Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
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
#ifndef ASDOPS_PARAMS_INDEX_H
#define ASDOPS_PARAMS_INDEX_H

#include <string>
#include <sstream>

namespace AsdOps {
namespace OpParam {
struct Index {
    enum IndexType {
        INDEX_UNDEFINED = 0,
        INDEX_ADD,
    };
    IndexType indexType;
    int64_t axis = 0;

    bool operator==(const Index &other) const
    {
        return (this->indexType == other.indexType) && (this->axis == other.axis);
    };
};
} // namespace OpParam
} // namespace AsdOps

#endif