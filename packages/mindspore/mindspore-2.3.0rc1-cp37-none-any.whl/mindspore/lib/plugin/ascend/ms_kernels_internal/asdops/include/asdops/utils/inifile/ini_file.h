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
#ifndef ASDOPS_INI_FILE_H
#define ASDOPS_INI_FILE_H
#include <string>
#include <map>

namespace AsdOps {
class IniFile {
public:
    static bool ParseIniFileToMap(const std::string &iniFilePath,
        std::map<std::string, std::map<std::string, std::string>> &contentInfoMap);
};
} // namespace AsdOps
#endif