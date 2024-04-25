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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ASDOP_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASDOP_IMPL_H_
#include "asdops/op_desc.h"
#include "asdops/operation.h"
#include "asdops/run_info.h"
#include "asdops/tactic.h"
#include "asdops/tensor.h"
#include "internal_kernel.h"
#include <unordered_map>
namespace mindspore {
namespace internal {

class AsdOpsImpl : public InternelKernelImpl {
 public:
  AsdOpsImpl(const OpParamPtr &param) : InternelKernelImpl(param){};
  virtual ~AsdOpsImpl() = default;
  bool Init(const ValidateInfo &info) override;
  void SetInputs(const std::vector<Tensor *> &inputs) override;
  void SetOutputs(const std::vector<Tensor *> &outputs) override;
  void SetWorkSpace(const std::vector<DeviceRawBuf> &workspace) override;
  void SetStream(const void *stream_ptr) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  size_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) override;

  void SetCacheInfo(const CacheInfo &cache_info);

 private:
  AsdOps::Tactic *InitAndGetTactic();

 protected:
  AsdOps::Tactic *tactic_ = nullptr;
  AsdOps::Operation *op_ = nullptr;
  AsdOps::LaunchParam launch_param_;
  AsdOps::OpDesc op_desc_;
  bool validated_ = false;

  RunInfo run_info_;
};

}  // namespace internal
}  // namespace mindspore
#endif
