/**
 * Copyright 2023-2024 Huawei Technologies Co., Ltd
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
#ifndef MS_KERNELS_INTERNAL_OP_PARAM_H_
#define MS_KERNELS_INTERNAL_OP_PARAM_H_
#include "asdops/op_desc.h"
#include "asdops/params/matmul.h"
#include "asdops/params/mix.h"
#include "asdops/params/slice.h"
#include "asdops/params/gather.h"
#include "asdops/params/elewise.h"
#include "asdops/params/activation.h"
#include "asdops/params/concat.h"
#include "asdops/params/transpose.h"
#include "asdops/params/norm.h"
#include "asdops/params/softmax.h"
#include "asdops/params/split.h"
#include "attention_param.h"
#include "asdops/params/expand.h"
#include "asdops/params/fill.h"
#include "asdops/params/reduce.h"
#include "asdops/params/sort.h"
#include <memory>
#include <vector>
namespace mindspore {
namespace internal {
using OpParam = AsdOps::OpDesc;
enum OpId : int {
  MatMul,
  KVCache,
  ReshapeAndCache,
  Slice,
  Gather,
  ApplyRotaryPosEmb,
  Add,
  Sub,
  FlashAttentionScore,
  PagedAttention,
  Cast,
  Gelu,
  Transpose,
  Equal,
  NotEqual,
  LogicalNot,
  Less,
  LessEqual,
  Greater,
  GreaterEqual,
  Mul,
  RealDiv,
  LayerNorm,
  AddLayerNorm,
  RmsNorm,
  AddRmsNorm,
  Softmax,
  Split,
  Swish,
  SwiGLU,
  Concat,
  MatmulQkv,
  MaskedFill,
  BroadcastTo,
  ReduceSum,
  TopK,
  Tile,
};
using MatMulParam = AsdOps::OpParam::MatMul;
using MixParam = AsdOps::OpParam::Mix;
using GatherParam = AsdOps::OpParam::Gather;
using ElewiseParam = AsdOps::OpParam::Elewise;
using SliceParam = AsdOps::OpParam::Slice;
using ActivationParam = AsdOps::OpParam::Activation;
using TransposeParam = AsdOps::OpParam::Transpose;
using NormParam = AsdOps::OpParam::Norm;
using SoftmaxParam = AsdOps::OpParam::Softmax;
using SplitParam = AsdOps::OpParam::Split;
using ConcatParam = AsdOps::OpParam::Concat;
using MaskedFillParam = AsdOps::OpParam::Fill;
using BroadcastToParam = AsdOps::OpParam::Expand;
using ReduceParam = AsdOps::OpParam::Reduce;
using SortParam = AsdOps::OpParam::Sort;
using ExpandParam = AsdOps::OpParam::Expand;

struct AddLayerNormParam {
  float eps;
  bool operator==(const AddLayerNormParam &other) const { return this->eps == other.eps; }
};

struct ApplyRotaryPosEmbParam {
  int32_t cosFormat{0};
};

struct AddRmsNormParam {
  float eps;
  bool operator==(const AddRmsNormParam &other) const { return this->eps == other.eps; }
};
}  // namespace internal
}  // namespace mindspore
#endif
