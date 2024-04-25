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
#ifndef COMMON_RT_BACKEND_HELPMACRO_H
#define COMMON_RT_BACKEND_HELPMACRO_H

#define CHECK_FUNC_EIXST_RETURN(func)                                                                                  \
    if ((func) == nullptr) {                                                                                           \
        return ASDRT_ERROR_FUNC_NOT_EXIST;                                                                             \
    }

#define CHECK_STATUS_RETURN(fun)                                                                                       \
    int ret = (fun);                                                                                                   \
    if (ret == 0) {                                                                                                    \
        return ASDRT_SUCCESS;                                                                                          \
    } else {                                                                                                           \
        return ret;                                                                                                    \
    }

#define CHECK_STATUS_WITH_DESC_RETURN(ret, funcName)                                                                   \
    if ((ret) == 0) {                                                                                                  \
        ASD_LOG(DEBUG) << (funcName) << " success";                                                                    \
        return ASDRT_SUCCESS;                                                                                          \
    } else {                                                                                                           \
        ASD_LOG(ERROR) << (funcName) << " fail, error:" << (ret);                                                      \
        return ret;                                                                                                    \
    }

#define CHECK_INITED_RETURN(ret)                                                                                       \
    if ((ret) != ASDRT_SUCCESS) {                                                                                      \
        return ret;                                                                                                    \
    }

#define CHECK_FUN_PARA_RETURN(para)                                                                                    \
    if ((para) == nullptr) {                                                                                           \
        return ASDRT_ERROR_PARA_CHECK_FAIL;                                                                            \
    }

#endif