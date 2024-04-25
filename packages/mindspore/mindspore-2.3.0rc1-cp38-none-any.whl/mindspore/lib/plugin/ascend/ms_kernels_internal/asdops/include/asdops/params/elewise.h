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
#ifndef ASDOPS_PARAMS_ELEWISE_H
#define ASDOPS_PARAMS_ELEWISE_H

#include "asdops/types.h"
#include "asdops/utils/compare/compare.h"

namespace AsdOps {
namespace OpParam {
struct Elewise {
    enum ElewiseType {
        ELEWISE_UNDEFINED = 0,
        ELEWISE_CAST,
        ELEWISE_MULS,
        ELEWISE_COS,
        ELEWISE_SIN,
        ELEWISE_NEG,
        ELEWISE_QUANT,
        ELEWISE_LOGICAL_NOT,
        ELEWISE_ADD,
        ELEWISE_MUL,
        ELEWISE_REALDIV,
        ELEWISE_LOGICAL_AND,
        ELEWISE_LOGICAL_OR,
        ELEWISE_LESS,
        ELEWISE_GREATER,
        ELEWISE_SUB,
        ELEWISE_TANH,
        ELEWISE_EQUAL,
        ELEWISE_QUANT_PER_CHANNEL,
        ELEWISE_DEQUANT_PER_CHANNEL,
    };
    ElewiseType elewiseType;

    float varAttr = 0.0f;    // MULS
    float inputScale = 1.0f; // QUANT
    int inputOffset = 0;     // QUANT
    int roundMode = 0;     // cast roundmode
    TensorDType outTensorType = TENSOR_DTYPE_UNDEFINED;

    bool operator==(const Elewise &other) const
    {
        return this->elewiseType == other.elewiseType && Utils::Compare<float>::IsEqual(this->varAttr, other.varAttr) &&
               Utils::Compare<float>::IsEqual(this->inputScale, other.inputScale) &&
               this->inputOffset == other.inputOffset &&
               this->roundMode == other.roundMode &&
               this->outTensorType == other.outTensorType;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif
