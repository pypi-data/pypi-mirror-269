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
#ifndef ASDOPS_PARAMS_MIX_H
#define ASDOPS_PARAMS_MIX_H

#include <cstdint>
#include <string>
#include <sstream>
#include <vector>
#include "asdops/utils/compare/compare.h"

namespace AsdOps {
namespace OpParam {
struct Mix {
    enum MixType {
        MIX_TRANSFORMER_ROPE_START = 1000,
        MIX_TRANSFORMER_ROPE_END = 1100,
        MIX_ROPE = 2,
        MIX_ROPE_GRAD = 19,

        MIX_TRANSFORMER_KVCACHE_START = 1100,
        MIX_RESHAPE_AND_CACHE_NZ = 1101,
        MIX_TRANSFORMER_KVCACHE_END = 1200,
        MIX_KVCACHE_ND = 0,
        MIX_KVCACHE_NZ = 3,
        MIX_KVCACHE_DYNAMIC_BATCH = 5,
        MIX_RESHAPE_AND_CACHE_ND = 9,

        MIX_TRANSFORMER_UNPAD_START = 1300,
        MIX_UNPAD_FASTSOFTMAX = 1301,
        MIX_UNPAD_FASTSOFTMAXGRAD = 1302,
        MIX_UNPAD_STRIDEDBATCHMATMUL = 1303,
        MIX_UNPAD_WITH_HIDDEN_STATE = 1304,
        MIX_PAD_WITH_HIDDEN_STATE = 1305,
        MIX_TRANSFORMER_UNPAD_END = 1500,
        MIX_UNPAD = 14,
        MIX_PAD = 15,
        MIX_UNPAD_GEN_ATTENTION_MASK = 16,

        MIX_TRANSFORMER_ATTENTION_START = 2000,
        MIX_UNPAD_FLASH_ATTENTION_FP32_ND = 2001,
        MIX_PAGED_ATTENTION_MASK_ND = 2002,
        MIX_PAGED_ATTENTION_NZ_MASK = 2003,
        MIX_PAGED_ATTENTION_NZ = 2004,
        MIX_UNPAD_FLASH_ATTENTION_NZ_ENCODER_NOCACHE = 2005,
        MIX_FLASH_ATTENTION_FORWARD = 2500,
        MIX_FLASH_ATTENTION_BACKWARD = 2501,
        MIX_TRANSFORMER_ATTENTION_END = 3000,
        MIX_UNPAD_FLASH_ATTENTION_ND = 1,
        MIX_UNPAD_DYNAMIC_BATCH_FLASH_ATTENTION = 4,
        MIX_UNPAD_FLASH_ATTENTION_NZ = 6,
        MIX_UNPAD_ALIBI_FLASH_ATTENTION_NZ = 7,
        MIX_PAGED_ATTENTION_ND = 8,
        MIX_UNPAD_DYNAMIC_BATCH_FLASH_ATTENTION_DECODER = 13,
        MIX_UNPAD_FLASH_ATTENTION_ENCODER_ND = 10,
        MIX_UNPAD_ALIBI_FLASH_ATTENTION_ND = 11,
        MIX_UNPAD_FLASH_ATTENTION_DECODER_ND = 12,
        MIX_UNPAD_FLASH_ATTENTION_NZ_ENCODER = 17,
        MIX_UNPAD_FLASH_ATTENTION_NZ_DECODER = 18
    };
    MixType mixType;

    // UNPAD_FLASH_ATTENTION
    int32_t headSize = 0;
    std::vector<int32_t> qSeqLen;
    std::vector<int32_t> kvSeqLen;

    float tor = 0;
    int32_t kvHead = 0;
    // UNPAD_BATCH_DYNAMIC_FLASH_ATTENTION
    std::vector<int32_t> batchRunStatus;
    // clamp 算子
    int32_t isClamp = 0;
    float clampMin = 0;
    float clampMax = 0;

    uint32_t isTriuMask = 0;
    // ROPE
    int32_t rotaryCoeff = 4;
    int32_t cosFormat = 0;
    // MIX_UNPAD_GEN_ATTENTION_MASK
    int32_t headNum = 0;
    // UNPAD_STRIDEDBATCHMATMUL
    int32_t batch = 1;
    int32_t transA = 0;
    int32_t transB = 0;
    std::vector<int32_t> m;
    std::vector<int32_t> k;
    std::vector<int32_t> n;
    std::vector<int32_t> lda;
    std::vector<int32_t> ldb;
    std::vector<int32_t> ldc;
    std::vector<int32_t> strideA;
    std::vector<int32_t> strideB;
    std::vector<int32_t> strideC;
    // MIX_PAGED_ATTENTION_MASK_ND, MIX_UNPAD_FLASH_ATTENTION_ENCODER_ND
    enum MaskType {
        MASK_TYPE_NONE = 0,
        MASK_TYPE_NORM = 1,
        MASK_TYPE_ALIBI = 2
    };
    std::vector<int8_t> identityM = {0};
    MaskType maskType = MASK_TYPE_NONE;

    // FLASH_ATTENTION_FORWARD_BACKWARD
    float scale = 1.0;
    enum IoLayout : int {
        BNSD = 0,
        BSH,
        SBH
    };
    IoLayout ioLayout = BNSD;
    float keepProb = 1.0;
    int32_t preTokens = 2147483647;
    int32_t nextTokens = 1;
    // UNPAD_WITH_HIDDEN_STATE & PAD_WITH_HIDDEN_STATE
    uint32_t maxSeqLen = 0;

    bool operator==(const Mix &other) const
    {
        return this->mixType == other.mixType && this->headSize == other.headSize &&
            this->qSeqLen == other.qSeqLen && this->kvSeqLen == other.kvSeqLen &&
            this->batchRunStatus == other.batchRunStatus && this->kvHead == other.kvHead &&
            Utils::Compare<float>::IsEqual(this->tor, other.tor) && this->rotaryCoeff == other.rotaryCoeff &&
            this->isTriuMask == other.isTriuMask && this->cosFormat == other.cosFormat &&
            this->headNum == other.headNum && this->batch == other.batch &&
            this->transA == other.transA && this->transB == other.transB &&
            this->m == other.m && this->k == other.k && this->n == other.n &&
            this->lda == other.lda && this->ldb == other.ldb && this->ldc == other.ldc &&
            this->strideA == other.strideA && this->strideB == other.strideB && this->strideC == other.strideC &&
            this->maskType == other.maskType && Utils::Compare<float>::IsEqual(this->scale, other.scale) &&
            this->ioLayout == other.ioLayout && Utils::Compare<float>::IsEqual(this->keepProb, other.keepProb) &&
            this->preTokens == other.preTokens && this->nextTokens == other.nextTokens &&
            this->maxSeqLen == other.maxSeqLen && this->identityM == other.identityM;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif // ASDOPS_PARAMS_ATTENTION_H