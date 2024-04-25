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
#ifndef ASDOPS_RUNINFO_H
#define ASDOPS_RUNINFO_H

#include <cstdint>

#include "asdops/kernel_info.h"
#include "asdops/utils/noncopyable/noncopyable.h"

namespace AsdOps {
class RunInfo : public NonCopyable {
public:
    RunInfo() = default;
    ~RunInfo();

public:
    void Reset();

    void SetStream(void *stream);
    void *GetStream() const;

    void SetLaunchWithTiling(bool flag);
    bool GetLaunchWithTiling() const;

    size_t GetWorkspaceSize() const;
    void SetWorkspaceDeviceAddr(uint8_t *addr);
    uint8_t *GetWorkspaceDeviceAddr() const;

    void SetTilingHostAddr(uint8_t *addr, uint64_t len);
    void SetTilingDeviceAddr(uint8_t *addr);
    uint8_t *GetTilingDeviceAddr() const;

    KernelInfo &GetKernelInfo();

    std::string ToString() const;

    void CopyTo(RunInfo &runInfo) const;

private:
    // used by User
    bool launchWithTiling_ = true;
    void *stream_ = nullptr;
    uint8_t *workspaceAddr_ = nullptr;
    uint8_t *tilingDeviceAddr_ = nullptr;

    // used by Tactic
    KernelInfo kernelInfo_;
};
} // namespace AsdOps

#endif
