/**
 * Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
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
#ifndef ASDOPS_PATH_UTILS_H
#define ASDOPS_PATH_UTILS_H

#include <cstdint>
#include <dlfcn.h>
#include <libgen.h>
#include <iostream>

namespace AsdOps {

static int stubFunc() {return 0;}

static std::string getAsdopHomePath() {
    void* anyFunc = (void*)stubFunc;
    Dl_info dl_info;
    if (dladdr(anyFunc, &dl_info)) {
        auto soPath = std::string(dl_info.dli_fname);
        auto pos = soPath.rfind('/');
        pos = soPath.rfind('/', pos - 1);
        if (pos != std::string::npos) {
            soPath = soPath.substr(0, pos);
        }
        return soPath;
    }
    return "";
}

} // namespace AsdOps

#endif


