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
#ifndef ASDOPS_PARAMS_ACTIVATION_H
#define ASDOPS_PARAMS_ACTIVATION_H
#include <string>
#include <sstream>
#include "asdops/utils/compare/compare.h"

namespace AsdOps {
namespace OpParam {
struct Activation {
    enum ActivationType {
        ACTIVATION_UNDEFINED = 0,
        ACTIVATION_RELU,
        ACTIVATION_GELU,
        ACTIVATION_FAST_GELU,
        ACTIVATION_SWISH,
        ACTIVATION_LOG,
        ACTIVATION_SWIGLU_FORWARD,
        ACTIVATION_SWIGLU_BACKWARD,
    };
    ActivationType activationType;

    float scale = 1.0f;       // for Swish
    int32_t dim = -1;         // SWIGLU

    bool operator==(const Activation &other) const
    {
        return this->activationType == other.activationType &&
               Utils::Compare<float>::IsEqual(this->scale, other.scale) && this->dim == other.dim;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif