# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Operations for sequence"""

from math import log
from mindspore.ops.primitive import Primitive, prim_attr_register


class ScalarDiv(Primitive):
    r"""
    Computes the quotient of dividing the first input scalar by the second input scalar element-wise.

    .. math::

        out_{i} = \frac{x_i}{y_i}

    .. note::
        The inputs can be constant/variable value. Usage is the same as '/' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, the type of scalar is float.

    Raises:
        TypeError: If `x` and `y` are not scalar.
        ValueError: If `y` is 0.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarDiv"""

    def __call__(self, x, y):
        if y == 0:
            raise ValueError('The divisor could not be zero. But the divisor is zero now.')
        return x / y


class ScalarFloordiv(Primitive):
    r"""
    Computes the quotient of dividing the first input scalar by the second input scalar element-wise.

    .. math::

        out_{i} = \frac{x_i}{y_i}

    .. note::
        The inputs can be constant/variable value. Usage is the same as '//' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, the type of scalar is float.

    Raises:
        TypeError: If `x` and `y` are not scalar.
        ValueError: If `y` is 0.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarFloordiv"""
        self.init_prim_io_names(inputs=['x', 'y'], outputs=['output'])

    def __call__(self, x, y):
        if y == 0:
            raise ValueError('The divisor could not be zero. But the divisor is zero now.')
        return x // y


class ScalarAdd(Primitive):
    r"""
    Adds two input scalar.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '+' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, and the data type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarAdd"""

    def __call__(self, x, y):
        return x + y


class ScalarPow(Primitive):
    r"""
    Pow two input scalar.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '+' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, and the data type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarPow"""

    def __call__(self, x, y):
        return pow(x, y)


class ScalarLog(Primitive):
    r"""
    Log input scalar.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '+' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, and the data type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarAdd"""

    def __call__(self, x):
        return log(x)


class ScalarUadd(Primitive):
    r"""
    UAdds input scalar.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '+' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, and the data type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarAdd"""

    def __call__(self, x):
        return x


class ScalarUsub(Primitive):
    r"""
    usub input scalar.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '+' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, and the data type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarUsub"""

    def __call__(self, x):
        return -x


class ScalarSub(Primitive):
    r"""
    Subtracts the second input Scalar from the first input Scalar.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '-' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, and the data type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarSub"""

    def __call__(self, x, y):
        return x - y


class ScalarMul(Primitive):
    r"""
    Muls two input scalar.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '+' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, and the data type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarMul"""

    def __call__(self, x, y):
        return x * y


class scalar_eq(Primitive):
    r"""
    Computes the equivalence between two Scalars.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '==' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, the type of scalar is bool.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarEq"""

    def __call__(self, x, y):
        return x == y


class scalar_gt(Primitive):
    r"""
    Compare the value of the input scalars :math:`x,y`, and the output result is a bool value.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '>' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, the type of scalar is bool.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize scalar_gt"""

    def __call__(self, x, y):
        return x > y


class scalar_lt(Primitive):
    r"""
    Computes the boolean value of :math:`x < y`.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '<' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, the type of scalar is bool.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize scalar_lt"""

    def __call__(self, x, y):
        return x < y


class scalar_ge(Primitive):
    r"""
    Compare the value of the input scalars :math:`x,y`, and the output result is a bool value.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '>=' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, the type of scalar is bool.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize scalar_ge"""

    def __call__(self, x, y):
        return x >= y


class scalar_le(Primitive):
    r"""
    Compare the value of the input scalars :math:`x,y`, and the output result is a bool value.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '<=' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, the type of scalar is bool.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize scalar_le"""

    def __call__(self, x, y):
        return x <= y


class ScalarMod(Primitive):
    r"""
    Computes the remainder of dividing the first input scalar by the second input scalar element-wise.

    .. math::

        out_{i} = x_{i} \text{ % } y_{i}

    .. note::
        The inputs can be constant/variable value. Usage is the same as '%' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.
        - **y** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, the type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarMod"""

    def __call__(self, x, y):
        if y == 0:
            raise ValueError('Cannot perform modulo operation on zero.')
        return x % y


class ScalarBool(Primitive):
    r"""
    Computes the input scalar true or false.

    .. note::
        The inputs can be constant/variable value.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar.

    Outputs:
        Scalar, the type is bool.

    Raises:
        TypeError: If `x` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarBool"""


class bool_not(Primitive):
    r"""
    Returns bool_not `not` of bool input.

    .. note::
        The inputs can be constant/variable value. Usage is the same as 'not' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar, the type can be bool.

    Outputs:
        Scalar, the type is bool.

    Raises:
        TypeError: If `x` are not bool scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize bool_not"""

    def __call__(self, x):
        return not x


class bit_and(Primitive):
    r"""
    Returns bitwise `and` of two scalars.

    .. math::

        out_{i} = x_{i} \text{ % } y_{i}

    .. note::
        The inputs can be constant/variable value. Usage is the same as '%' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar, the type can be int or bool.
        - **y** (Scalar) - A constant or variable scalar, the type can be int or bool.

    Outputs:
        Scalar, the type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarMod"""


class bit_or(Primitive):
    r"""
    Returns bitwise `or` of two scalars.

    .. note::
        The inputs can be constant/variable value. Usage is the same as '|' in Python.
        This primitive only have 'CPU' implementation, for other platform, it runs using heterogeneous.

    Inputs:
        - **x** (Scalar) - A constant or variable scalar, the type can be int or bool.
        - **y** (Scalar) - A constant or variable scalar, the type can be int or bool.

    Outputs:
        Scalar, the type is the one with higher precision or higher digits among the two inputs.

    Raises:
        TypeError: If `x` and `y` are not scalar.

    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    """
    @prim_attr_register
    def __init__(self):
        """Initialize ScalarMod"""
