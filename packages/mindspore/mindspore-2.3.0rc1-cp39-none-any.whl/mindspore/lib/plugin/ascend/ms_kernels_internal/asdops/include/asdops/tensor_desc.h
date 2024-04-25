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
#ifndef ASDOPS_TENSORDESC_H
#define ASDOPS_TENSORDESC_H
#include "asdops/types.h"
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
struct TensorDesc {
    TensorDType dtype = TENSOR_DTYPE_UNDEFINED;
    TensorFormat format = TENSOR_FORMAT_UNDEFINED;
    AsdOps::SVector<int64_t> dims;
    int64_t Numel() const;
    void View(const AsdOps::SVector<int64_t> &newDims);
    void CombinDim(size_t fromDimPos, size_t endDimPos);
    void EraseFirstDimOne(); // 删除Dim等于1的第一个维度
    void AddDimOne();
    std::string ToString() const;
};
} // namespace AsdOps

#endif