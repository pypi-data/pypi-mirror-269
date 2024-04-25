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
#ifndef ASDOPS_LAUNCH_PARAM_H
#define ASDOPS_LAUNCH_PARAM_H

#include <string>
#include "asdops/types.h"
#include "asdops/tensor.h"
#include "asdops/op_desc.h"

namespace AsdOps {
class LaunchParam {
public:
    LaunchParam() = default;
    LaunchParam(const LaunchParam &other);
    LaunchParam &operator=(const LaunchParam &other);
    ~LaunchParam();

public:
    void Reset();

    const OpDesc &GetOpDesc() const;
    void SetOpDesc(const OpDesc &opDesc);

    void AddInTensor(const Tensor &tensor);
    size_t GetInTensorCount() const;
    const Tensor &GetInTensor(size_t pos) const;
    Tensor &GetInTensor(size_t pos);
    const SVector<Tensor> &GetInTensors() const;
    SVector<Tensor> &GetInTensors();

    void AddOutTensor(const Tensor &tensor);
    size_t GetOutTensorCount() const;
    const Tensor &GetOutTensor(size_t pos) const;
    Tensor &GetOutTensor(size_t pos);
    const SVector<Tensor> &GetOutTensors() const;
    SVector<Tensor> &GetOutTensors();

    std::string ToString() const;

private:
    OpDesc opDesc_;
    SVector<Tensor> inTensors_;
    SVector<Tensor> outTensors_;
};
} // namespace AsdOps

#endif
