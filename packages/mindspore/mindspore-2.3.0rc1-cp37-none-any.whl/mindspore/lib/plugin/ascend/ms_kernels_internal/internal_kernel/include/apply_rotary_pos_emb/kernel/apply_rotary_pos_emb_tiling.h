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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ASCENDC_APPLY_ROTARY_POS_EMB_TILING_DATA_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASCENDC_APPLY_ROTARY_POS_EMB_TILING_DATA_H_

#include <stdint.h>

struct ApplyRotaryPosEmbTilingData {
  uint32_t hiddenSizeQ{16};
  uint32_t hiddenSizeK{16};
  uint32_t headDim{1};
  uint32_t headNumQ{1};
  uint32_t headNumK{1};
  uint32_t rotaryCoeff{4};
  uint32_t ntokens{1};
  uint32_t ropeFormat{0};
  uint32_t realCore{0};
  uint32_t cosFormat{0};
  uint32_t batch{32};
  uint32_t highPrecision{0};
  uint32_t maxUbSize{0};

  int32_t ndim;
  int32_t qkDtype;   // 0=fp16 1=bf16 2=fp32
  int32_t posDtype;  // 0=i64 1=u64 2=i32 3=u32

  // int32_t batch;
  int32_t numHeadQ;
  int32_t numHeadK;
  // int32_t hiddenDim;
  int32_t seqLen;
  int32_t maxSeqLen;

  int32_t posSize;  // seqLen==1 ? batch : seqLen
};

#endif
