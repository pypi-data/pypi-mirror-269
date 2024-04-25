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
#ifndef COMMON_LOG_LOG_H
#define COMMON_LOG_LOG_H
#include "asdops/utils/log/log_stream.h"
#include "asdops/utils/log/log_core.h"
#include "asdops/utils/log/log_sink.h"
#include "asdops/utils/log/log_entity.h"

#define ASD_LOG(level) ASD_LOG_##level

#define ASD_FLOG(level, format, ...) ASD_FLOG_##level(format, __VA_ARGS__)

#define ASD_LOG_IF(condition, level)                                                                                   \
    if (condition)                                                                                                     \
    ASD_LOG(level)

#define ASD_LOG_TRACE                                                                                                  \
    if (AsdOps::LogLevel::TRACE >= AsdOps::LogCore::Instance().GetLogLevel())                                          \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::TRACE)
#define ASD_LOG_DEBUG                                                                                                  \
    if (AsdOps::LogLevel::DEBUG >= AsdOps::LogCore::Instance().GetLogLevel())                                          \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::DEBUG)
#define ASD_LOG_INFO                                                                                                   \
    if (AsdOps::LogLevel::INFO >= AsdOps::LogCore::Instance().GetLogLevel())                                           \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::INFO)
#define ASD_LOG_WARN                                                                                                   \
    if (AsdOps::LogLevel::WARN >= AsdOps::LogCore::Instance().GetLogLevel())                                           \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::WARN)
#define ASD_LOG_ERROR                                                                                                  \
    if (AsdOps::LogLevel::ERROR >= AsdOps::LogCore::Instance().GetLogLevel())                                          \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::ERROR)
#define ASD_LOG_FATAL                                                                                                  \
    if (AsdOps::LogLevel::FATAL >= AsdOps::LogCore::Instance().GetLogLevel())                                          \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::FATAL)

#define ASD_FLOG_TRACE(format, ...)                                                                                    \
    if (AsdOps::LogLevel::TRACE >= AsdOps::LogCore::Instance().GetLogLevel())                                          \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::TRACE).Format(format, __VA_ARGS__)
#define ASD_FLOG_DEBUG(format, ...)                                                                                    \
    if (AsdOps::LogLevel::DEBUG >= AsdOps::LogCore::Instance().GetLogLevel())                                          \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::DEBUG).Format(format, __VA_ARGS__)
#define ASD_FLOG_INFO(format, ...)                                                                                     \
    if (AsdOps::LogLevel::INFO >= AsdOps::LogCore::Instance().GetLogLevel())                                           \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::INFO).Format(format, __VA_ARGS__)
#define ASD_FLOG_WARN(format, ...)                                                                                     \
    if (AsdOps::LogLevel::WARN >= AsdOps::LogCore::Instance().GetLogLevel())                                           \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::WARN).Format(format, __VA_ARGS__)
#define ASD_FLOG_ERROR(format, ...)                                                                                    \
    if (AsdOps::LogLevel::ERROR >= AsdOps::LogCore::Instance().GetLogLevel())                                          \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::ERROR).Format(format, __VA_ARGS__)
#define ASD_FLOG_FATAL(format, ...)                                                                                    \
    if (AsdOps::LogLevel::FATAL >= AsdOps::LogCore::Instance().GetLogLevel())                                          \
    AsdOps::LogStream(__FILE__, __LINE__, __FUNCTION__, AsdOps::LogLevel::FATAL).Format(format, __VA_ARGS__)

#endif