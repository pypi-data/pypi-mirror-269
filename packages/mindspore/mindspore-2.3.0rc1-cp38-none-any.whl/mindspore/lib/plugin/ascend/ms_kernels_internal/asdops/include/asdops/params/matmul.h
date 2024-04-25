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
#ifndef ASDOPS_PARAMS_MATMUL_H
#define ASDOPS_PARAMS_MATMUL_H

#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
namespace OpParam {
struct MatMul {
    bool transposeA = false;
    bool transposeB = false;
    SVector<int64_t> oriShape = {0, 0, 0}; // original shape: m,k,n - (m,k) * (k,n)
    bool withBias = false;
    bool enDequant = false;
    uint32_t tilingN = 0;    // 压缩算法透传参数, 单压缩块 n 方向的基块数
    uint32_t tilingK = 0;    // 压缩算法透传参数, 单压缩块 k 方向的基块数
    bool enShuffleK = false; // Shuffle-K使能，默认关。

    bool operator==(const MatMul &other) const
    {
        return this->transposeA == other.transposeA && this->transposeB == other.transposeB &&
               this->oriShape == other.oriShape && this->withBias == other.withBias &&
               this->enDequant == other.enDequant && this->tilingN == other.tilingN && this->tilingK == other.tilingK;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif // ASDOPS_PARAMS_MATMUL_H