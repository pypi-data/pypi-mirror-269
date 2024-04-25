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

#ifndef COMMON_FP16_T_H
#define COMMON_FP16_T_H

#include <cstdint>
#include <cmath>
#include <algorithm>
#include <ostream>

namespace AsdOps {
/**
 * @ingroup fp16_t
 * @brief   Half precision float
 *          bit15:       1 bit SIGN      +---+-----+------------+
 *          bit14-10:    5 bit EXP       | S |EEEEE|MM MMMM MMMM|
 *          bit0-9:      10bit MAN       +---+-----+------------+
 */
struct fp16_t {
    uint16_t val = 0;

public:
    /**
     * @ingroup fp16_t constructor
     * @brief   Constructor without any param(default constructor)
     */
    fp16_t(void) { val = 0x0u; }

    /**
     * @ingroup all type constructor
     * @brief   Constructor with all type
     */
    template <typename T>
    explicit fp16_t(const T& value) { *this = value; }

    /**
     * @ingroup fp16_t constructor
     * @brief   Constructor with an uint16_t value
     */
    explicit fp16_t(const uint16_t& uiVal) : val(uiVal) {}

    /**
     * @ingroup fp16_t constructor
     * @brief   Constructor with a fp16_t object(copy constructor)
     */
    fp16_t(const fp16_t& fp) : val(fp.val) {}

    /**
     * @ingroup fp16_t math operator
     * @param [in] fp fp16_t object to be added
     * @brief   Override addition operator to performing fp16_t addition
     * @return  Return fp16_t result of adding this and fp
     */
    fp16_t operator+(const fp16_t fp) const;

    /**
     * @ingroup fp16_t math operator
     * @param [in] fp fp16_t object to be subtracted
     * @brief   Override addition operator to performing fp16_t subtraction
     * @return  Return fp16_t result of subtraction fp from this
     */
    fp16_t operator-(const fp16_t fp) const;

    /**
     * @ingroup fp16_t math operator
     * @param [in] fp fp16_t object to be multiplied
     * @brief   Override multiplication operator to performing fp16_t multiplication
     * @return  Return fp16_t result of multiplying this and fp
     */
    fp16_t operator*(const fp16_t fp) const;

    /**
     * @ingroup fp16_t math operator divided
     * @param [in] fp fp16_t object to be divided
     * @brief   Override division operator to performing fp16_t division
     * @return  Return fp16_t result of division this by fp
     */
    fp16_t operator/(const fp16_t fp) const;

    /**
     * @ingroup fp16_t math operator
     * @param [in] fp fp16_t object to be added
     * @brief   Override addition operator to performing fp16_t addition
     * @return  Return fp16_t result of adding this and fp
     */
    fp16_t operator+=(const fp16_t fp);

    /**
     * @ingroup fp16_t math operator
     * @param [in] fp fp16_t object to be subtracted
     * @brief   Override addition operator to performing fp16_t subtraction
     * @return  Return fp16_t result of subtraction fp from this
     */
    fp16_t operator-=(const fp16_t fp);

    /**
     * @ingroup fp16_t math operator
     * @param [in] fp fp16_t object to be multiplied
     * @brief   Override multiplication operator to performing fp16_t multiplication
     * @return  Return fp16_t result of multiplying this and fp
     */
    fp16_t operator*=(const fp16_t fp);

    /**
     * @ingroup fp16_t math operator divided
     * @param [in] fp fp16_t object to be divided
     * @brief   Override division operator to performing fp16_t division
     * @return  Return fp16_t result of division this by fp
     */
    fp16_t operator/=(const fp16_t fp);

    /**
     * @ingroup fp16_t math compare operator
     * @param [in] fp fp16_t object to be compared
     * @brief   Override basic comparison operator to performing fp16_t if-equal comparison
     * @return  Return boolean result of if-equal comparison of this and fp.
     */
    bool operator==(const fp16_t& fp) const;

    /**
     * @ingroup fp16_t math compare operator
     * @param [in] fp fp16_t object to be compared
     * @brief   Override basic comparison operator to performing fp16_t not-equal comparison
     * @return  Return boolean result of not-equal comparison of this and fp.
     */
    bool operator!=(const fp16_t& fp) const;

    /**
     * @ingroup fp16_t math compare operator
     * @param [in] fp fp16_t object to be compared
     * @brief   Override basic comparison operator to performing fp16_t greater-than comparison
     * @return  Return boolean result of greater-than comparison of this and fp.
     */
    bool operator>(const fp16_t& fp) const;

    /**
     * @ingroup fp16_t math compare operator
     * @param [in] fp fp16_t object to be compared
     * @brief   Override basic comparison operator to performing fp16_t greater-equal comparison
     * @return  Return boolean result of greater-equal comparison of this and fp.
     */
    bool operator>=(const fp16_t& fp) const;

    /**
     * @ingroup fp16_t math compare operator
     * @param [in] fp fp16_t object to be compared
     * @brief   Override basic comparison operator to performing fp16_t less-than comparison
     * @return  Return boolean result of less-than comparison of this and fp.
     */
    bool operator<(const fp16_t& fp) const;

    /**
     * @ingroup fp16_t math compare operator
     * @param [in] fp fp16_t object to be compared
     * @brief   Override basic comparison operator to performing fp16_t less-equal comparison
     * @return  Return boolean result of less-equal comparison of this and fp.
     */
    bool operator<=(const fp16_t& fp) const;

    /**
     * @ingroup fp16_t math evaluation operator
     * @param [in] fp fp16_t object to be copy to fp16_t
     * @brief   Override basic evaluation operator to copy fp16_t to a new fp16_t
     * @return  Return fp16_t result from fp
     */
    fp16_t& operator=(const fp16_t& fp);

    /**
     * @ingroup fp16_t math evaluation operator
     * @param [in] fVal float object to be converted to fp16_t
     * @brief   Override basic evaluation operator to convert float to fp16_t
     * @return  Return fp16_t result from fVal
     */
    fp16_t& operator=(const float& fVal);

    /**
     * @ingroup fp16_t math evaluation operator
     * @param [in] dVal double object to be converted to fp16_t
     * @brief   Override basic evaluation operator to convert double to fp16_t
     * @return  Return fp16_t result from dVal
     */
    fp16_t& operator=(const double& dVal);

    /**
     * @ingroup fp16_t math evaluation operator
     * @param [in] iVal float object to be converted to fp16_t
     * @brief   Override basic evaluation operator to convert float to fp16_t
     * @return  Return fp16_t result from iVal
     */
    fp16_t& operator=(const int8_t& iVal);

    /**
     * @ingroup fp16_t math evaluation operator
     * @param [in] uiVal uint8_t object to be converted to fp16_t
     * @brief   Override basic evaluation operator to convert uint8_t to fp16_t
     * @return  Return fp16_t result from uiVal
     */
    fp16_t& operator=(const uint8_t& uiVal);

    /**
     * @ingroup fp16_t math evaluation operator
     * @param [in] iVal int16_t object to be converted to fp16_t
     * @brief   Override basic evaluation operator to convert int16_t to fp16_t
     * @return  Return fp16_t result from iVal
     */
    fp16_t& operator=(const int16_t& iVal);

    /**
     * @ingroup fp16_t math evaluation operator
     * @param [in] uiVal uint16_t object to be converted to fp16_t
     * @brief   Override basic evaluation operator to convert uint16_t to fp16_t
     * @return  Return fp16_t result from uiVal
     */
    fp16_t& operator=(const uint16_t& uiVal);

    /**
     * @ingroup fp16_t math evaluation operator
     * @param [in] iVal int32_t object to be converted to fp16_t
     * @brief   Override basic evaluation operator to convert int32_t to fp16_t
     * @return  Return fp16_t result from iVal
     */
    fp16_t& operator=(const int32_t& iVal);

    /**
     * @ingroup fp16_t math evaluation operator
     * @param [in] uiVal uint32_t object to be converted to fp16_t
     * @brief   Override basic evaluation operator to convert uint32_t to fp16_t
     * @return  Return fp16_t result from uiVal
     */
    fp16_t& operator=(const uint32_t& uiVal);

    /**
     * @ingroup fp16_t math conversion
     * @brief   Override convert operator to convert fp16_t to float/fp32
     * @return  Return float/fp32 value of fp16_t
     */
    operator float() const;

    /**
     * @ingroup fp16_t math conversion
     * @brief   Override convert operator to convert fp16_t to double/fp64
     * @return  Return double/fp64 value of fp16_t
     */
    operator double() const;

    /**
     * @ingroup fp16_t math conversion
     * @brief   Override convert operator to convert fp16_t to int8_t
     * @return  Return int8_t value of fp16_t
     */
    operator int8_t() const;

    /**
     * @ingroup fp16_t math conversion
     * @brief   Override convert operator to convert fp16_t to uint8_t
     * @return  Return uint8_t value of fp16_t
     */
    operator uint8_t() const;

    /**
     * @ingroup fp16_t conversion
     * @brief   Override convert operator to convert fp16_t to int16_t
     * @return  Return int16_t value of fp16_t
     */
    operator int16_t() const;

    /**
     * @ingroup fp16_t math conversion
     * @brief   Override convert operator to convert fp16_t to uint16_t
     * @return  Return uint16_t value of fp16_t
     */
    operator uint16_t() const;

    /**
     * @ingroup fp16_t math conversion
     * @brief   Override convert operator to convert fp16_t to int32_t
     * @return  Return int32_t value of fp16_t
     */
    operator int32_t() const;

    /**
     * @ingroup fp16_t math conversion
     * @brief   Override convert operator to convert fp16_t to int64_t
     * @return  Return int64_t value of fp16_t
     */
    operator uint32_t() const;

    /**
     * @ingroup fp16_t judgment method
     * @param [in] fp fp16_t object to be judgement
     * @brief   whether a fp16_t is inifinite
     * @return  Returns 1:+INF -1:-INF 0:not INF
     */
    int IsInf() const;

    /**
     * @ingroup fp16_t math conversion
     * @brief   Convert fp16_t to float/fp32
     * @return  Return float/fp32 value of fp16_t
     */
    float ToFloat();

    /**
     * @ingroup fp16_t math conversion
     * @brief   Convert fp16_t to double/fp64
     * @return  Return double/fp64 value of fp16_t
     */
    double ToDouble();

    /**
     * @ingroup fp16_t math conversion
     * @brief   Convert fp16_t to int8_t
     * @return  Return int8_t value of fp16_t
     */
    int8_t ToInt8();

    /**
     * @ingroup fp16_t math conversion
     * @brief   Convert fp16_t to uint8_t
     * @return  Return uint8_t value of fp16_t
     */
    uint8_t ToUInt8();

    /**
     * @ingroup fp16_t conversion
     * @brief   Convert fp16_t to int16_t
     * @return  Return int16_t value of fp16_t
     */
    int16_t ToInt16();

    /**
     * @ingroup fp16_t math conversion
     * @brief   Convert fp16_t to uint16_t
     * @return  Return uint16_t value of fp16_t
     */
    uint16_t ToUInt16();

    /**
     * @ingroup fp16_t math conversion
     * @brief   Convert fp16_t to int32_t
     * @return  Return int32_t value of fp16_t
     */
    int32_t ToInt32();

    /**
     * @ingroup fp16_t math conversion
     * @brief   Convert fp16_t to int64_t
     * @return  Return int64_t value of fp16_t
     */
    uint32_t ToUInt32();
};

std::ostream &operator<<(std::ostream &os, const fp16_t &fp);
}; // namespace AsdOps

#endif // COMMON_FP16_T_H
