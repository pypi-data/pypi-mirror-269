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

#ifndef MS_KERNELS_INTERNAL_KERNEL_MATMUL_MATMUL_STRIDEDSLICE_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_MATMUL_MATMUL_STRIDEDSLICE_IMPL_H_

#include "asdops/op_desc.h"
#include "asdops/operation.h"
#include "asdops/run_info.h"
#include "asdops/tactic.h"
#include "asdops/tensor.h"

#include "utils.h"
// #include "pp_matmul_info.h"
#include "backend_param.h"
#include "tiling_data.h"
#include "param/matmul_qkv_param.h"
// #include "pp_matmul_common_tiling.h"
#include "tune_repo/utils.h"

#include "internal_kernel.h"

#include "acl_rt.h"
#include <unordered_map>

namespace mindspore {
namespace internal {

class MatMulStridedSliceFusionImpl : public InternelKernelImpl {
 public:
  MatMulStridedSliceFusionImpl(const OpParamPtr &param) : InternelKernelImpl(param){};
  virtual ~MatMulStridedSliceFusionImpl() = default;
  bool Init(const ValidateInfo &info) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  size_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  int TilingLLMCustom(HostRawBuf &tilingBuf);
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) override;

 private:
  std::string soc_{"Ascend910B2"};
  HardwareInfo hwInfo_;
  uint32_t m_, k_, n0_, n1_, n2_;
  const char *func_name_ = "UnknownFunc";
  DeviceRawBuf tiling_addr_;
  TensorDType input_dtype_;
  TensorDType output_dtype_;
  int block_dim_ = 0;
  bool trans_a_{false};
  bool trans_b_{true};

  REPO tuningTable_;
  tiling::MatmulStridedSliceFusionTilingData t_;
  void GetTunedKey(std::vector<int> &tune_key);
  void GetTunedValue(const std::vector<int> &tuned_config);
};

}  // namespace internal
}  // namespace mindspore
#endif
