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
#ifndef COMMON_RT_DEVICE_DEVICE_H
#define COMMON_RT_DEVICE_DEVICE_H
#include "asdops/utils/rt/base/types.h"

#ifdef __cplusplus
extern "C" {
#endif
namespace AsdOps {
int AsdRtDeviceGetCount(int32_t *devCount);
int AsdRtDeviceGetIds(int32_t *devIds, int32_t devIdNum);
int AsdRtDeviceGetCurrent(int32_t *devId);
int AsdRtDeviceSetCurrent(int32_t devId);
int AsdRtDeviceResetCurrent(int32_t devId);
int AsdRtDeviceSetSocVersion(const char *version);
int AsdRtDeviceGetSocVersion(char *version, uint32_t maxLen);
int AsdRtDeviceGetBareTgid(uint32_t *pid);
int AsdRtDeviceGetPairDevicesInfo(uint32_t devId, uint32_t otherDevId, int32_t infoType, int64_t *val);
}
#ifdef __cplusplus
}
#endif
#endif