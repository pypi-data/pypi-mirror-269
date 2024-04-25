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
#ifndef ASDOPS_KERNEL_INFO_H
#define ASDOPS_KERNEL_INFO_H

#include <cstdint>

#include "asdops/utils/noncopyable/noncopyable.h"
#include "asdops/utils/status/status.h"
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
template <typename T> using MiniVector = SVector<T, 8>; // 8 小容量SVECTOR

class KernelInfo : public NonCopyable {
public:
struct ConstTensorInfo {
    uint64_t argIdx = 0;
    uint64_t size = 0;
};

struct TilingExtInfo {
    uint32_t blockDim = 0;
    uint64_t tilingId = 0;
    uint64_t constTensorOffset = 0; // const tensor offset in host tiling
    uint64_t usedSize = 0; // actual tiling size used
    uint8_t *hostTilingAddr = nullptr;
    uint64_t hostTilingSize = 0;
};

struct MemsetInfo {
    uint64_t argIdx = 0;
    uint64_t size = 0;
};

public:
    KernelInfo() = default;
    ~KernelInfo();

public:
    void Reset(bool deleteTiling);
    // Args
    Status InitArgs(uint64_t len);
    uint8_t *GetArgs() const;
    uint64_t GetArgsSize() const;

    // Hwsync
    void SetHwsyncIdx(int64_t idx);
    int64_t GetHwsyncIdx() const;

    // TilingExtInfo - BlockDim / TilingId
    void SetBlockDim(uint32_t blockDim);
    uint32_t GetBlockDim() const;
    void SetTilingId(uint64_t tilingId);
    uint64_t GetTilingId() const;

    // TilingExtInfo - TilingHost
    Status AllocTilingHost(uint64_t len);
    void SetTilingHostAddr(uint8_t *addr, uint64_t len);
    uint8_t *GetTilingHostAddr() const;
    uint64_t GetTilingSize() const;

    void SetTilingUsedSize(uint64_t usedSize);
    uint64_t GetTilingUsedSize() const;

    // TilingExtInfo - ConstTensorOffset
    void SetConstTensorOffset(uint64_t offset);
    uint64_t GetConstTensorOffset() const;

    // ConstTensor
    template <typename T_SRC, typename T_DST = T_SRC, typename T_CONT = SVector<T_SRC>>
    bool AddConstTensorData(uint64_t argIdx, const T_CONT &tensorData);

    size_t GetConstTensorCount() const;
    const ConstTensorInfo &GetConstTensorInfo(size_t id) const;

    // Workspace
    MiniVector<uint64_t> &GetWorkspaceSizes();
    uint64_t GetTotalWorkspaceSize() const;

    // Memset
    void SetMemsetInfo(uint64_t argIdx, uint64_t size);
    MiniVector<KernelInfo::MemsetInfo> &GetMemsetInfo();

    std::string ToString() const;
    void CopyTo(KernelInfo &kernelInfo) const;

private:
    void ResetArgs();
    void ResetTilingInfo();
    void ResetConstTensorInfo();
    void ResetWorkspaceSizes();
    void ResetMemsetInfo();

private:
    uint8_t *args_ = nullptr;
    uint64_t argsSize_ = 0;

    int64_t hwsyncIdx_ = -1; // <: no hwsync, >=0: hwsync arg idx
    TilingExtInfo tilingExtInfo_;
    MiniVector<ConstTensorInfo> constTensorInfo_;
    MiniVector<uint64_t> workspaceSizes_;
    MiniVector<MemsetInfo> memsetInfo_;
};
} // namespace AsdOps

#endif
