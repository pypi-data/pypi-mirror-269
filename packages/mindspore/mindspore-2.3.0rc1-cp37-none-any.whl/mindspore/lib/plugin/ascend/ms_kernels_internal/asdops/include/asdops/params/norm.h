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
#ifndef ASDOPS_PARAMS_NORM_H
#define ASDOPS_PARAMS_NORM_H

#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"
#include "asdops/utils/compare/compare.h"

namespace AsdOps {
namespace OpParam {
struct Norm {
    enum NormType { NORM_UNDEFINED = 0, LAYER_NORM, RMS_NORM, RMS_NORM_FORWARD, RMS_NORM_BACKWARD};
    NormType normType;
    // layernorm
    int32_t beginNormAxis = 0;
    int32_t beginParamsAxis = 0;
    // postlayernorm
    // opsMode = 0 : high precision
    // opsMode = 1 : high performance
    size_t opsMode = 0;
    float epsilon = 0.1f;
    float zoomScaleValue = 1.0f;
    float inputScale = 1.0f; // NORM_POSTLAYERNORMQUANT
    int inputOffset = 0;     // NORM_POSTLAYERNORMQUANT
    float inputAlpha = 1.0f; // NORM_POSTLAYERNORMQUANT
    bool inGamma = false; // LayernormF16Tactic, LayernormBF16Tactic, LayernormF32Tactic, PostLayernormF16Tactic,
                          // LayernormF16QuantTactic, PostLayernormF16QuantTactic, RmsPreNormQuantTactic, RmsNormTactic,
                          // RmsNormQuantTactic
    bool inBeta = false;  // LayernormF16Tactic, LayernormBF16Tactic, LayernormF32Tactic, PostLayernormF16Tactic,
                          // LayernormF16QuantTactic, PostLayernormF16QuantTactic, RmsNormQuantTactic
    bool inRes = false;   // PostLayernormF16Tactic, PostLayernormF16QuantTactic, RmsPreNormQuantTactic
    bool inNormBias = false;  // RmsPreNormQuantTactic
    bool outMean = false;     // LayernormF16Tactic, LayernormBF16Tactic, LayernormF32Tactic
    bool outVarience = false; // LayernormF16Tactic, LayernormBF16Tactic, LayernormF32Tactic
    bool outResQuant = false; // LayernormF16QuantTactic, PostLayernormF16QuantTactic
    bool outRes = false;      // RmsPreNormQuantTactic

    bool operator==(const Norm &other) const
    {
        return this->normType == other.normType && this->beginNormAxis == other.beginNormAxis &&
               this->beginParamsAxis == other.beginParamsAxis && this->opsMode == other.opsMode &&
               Utils::Compare<float>::IsEqual(this->epsilon, other.epsilon) &&
               Utils::Compare<float>::IsEqual(this->zoomScaleValue, other.zoomScaleValue) &&
               Utils::Compare<float>::IsEqual(this->inputScale, other.inputScale) &&
               this->inputOffset == other.inputOffset &&
               Utils::Compare<float>::IsEqual(this->inputAlpha, other.inputAlpha) &&
               this->inGamma == other.inGamma &&
               this->inBeta == other.inBeta &&
               this->inRes == other.inRes &&
               this->inNormBias == other.inNormBias &&
               this->outMean == other.outMean &&
               this->outVarience == other.outVarience &&
               this->outResQuant == other.outResQuant &&
               this->outRes == other.outRes;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif