/**
 * Copyright 2024 Huawei Technologies Co., Ltd
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

#ifndef MATMULSTRIDEDSLICE_TILING_DATA_H
#define MATMULSTRIDEDSLICE_TILING_DATA_H

#include <stdint.h>
#include <algorithm>

namespace mindspore {
namespace internal {
namespace tiling {
struct MatmulStridedSliceFusionTilingData {
  uint32_t tilingId{0};
  uint32_t BlockDimM{0};
  uint32_t BlockDimN{0};
  uint32_t BlockTotal{0};
  uint32_t M{0};
  uint32_t K{0};
  uint32_t N{0};
  uint32_t N0{0};
  uint32_t N1{0};
  uint32_t N2{0};
  uint32_t BaseM{0};
  uint32_t BaseK{0};
  uint32_t BaseN{0};
  uint32_t BlockLenM{0};
  uint32_t BlockLenK{0};
  uint32_t BlockLenN{0};
  uint32_t BaseMNum{0};
  uint32_t BaseKNum{0};
  uint32_t BaseNNum{0};
  uint32_t MmadM{0};
  uint32_t MmadK{0};
  uint32_t MmadN{0};
  uint32_t FractalKNum{0};
  uint32_t FractalKInBlockNum{0};
  uint32_t PartKInL0A{2};
  uint32_t TransA{0};
  uint32_t TransB{1};
};

}  // namespace tiling
}  // namespace internal
}  // namespace mindspore
#endif  // MATMULSTRIDEDSLICE_TILING_DATA_H