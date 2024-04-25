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

from mindspore.common import dtype as mstype
from mindspore.ops.auto_generate.pyboost_inner_prim import *


def add(input, other, alpha=1):
    r"""
    Adds scaled other value to input Tensor.
    
    .. math::
    
        out_{i} = input_{i} + alpha \times other_{i}
    
    Note:
        - When the two inputs have different shapes,
          they must be able to broadcast to a common shape.
        - The two inputs and alpha comply with the implicit type conversion rules to make the data types
          consistent.
    
    Args:
        input (Union[Tensor, number.Number, bool]): The first input is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        other (Union[Tensor, number.Number, bool]): The second input, is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        alpha (number.Number): A scaling factor applied to `other`, default 1.
    
    Returns:
        Tensor, the shape is the same as the one of the input `input`, `other` after broadcasting,
        and the data type is the one with higher precision or higher digits among the two inputs and alpha.
    
    Raises:
        TypeError: If the type of `input`, `other`, or `alpha` is not one of the following: Tensor, number.Number, bool.
        TypeError: If `alpha` is of type float but `input` and `other` are not of type float.
        TypeError: If `alpha` is of type bool but `input` and `other` are not of type bool.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore import Tensor
        >>> from mindspore.ops.extend import add
        >>> x = Tensor(1, mindspore.int32)
        >>> y = Tensor(np.array([4, 5, 6]).astype(np.float32))
        >>> alpha = 0.5
        >>> output = add(x, y, alpha)
        >>> print(output)
        [3. 3.5 4.]
        >>> # the data type of x is int32, the data type of y is float32,
        >>> # alpha is a float, and the output is the data format of higher precision float32.
        >>> print(output.dtype)
        Float32
    """
    return add_impl(input, other, alpha)


def sub(input, other, alpha=1):
    r"""
    Subtracts scaled other value from input Tensor.
    
    .. math::
    
        out_{i} = input_{i} - alpha \times other_{i}
    
    Note:
        - When the two inputs have different shapes,
          they must be able to broadcast to a common shape.
        - The two inputs and alpha comply with the implicit type conversion rules to make the data types
          consistent.
    
    Args:
        input (Union[Tensor, number.Number, bool]): The first input is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        other (Union[Tensor, number.Number, bool]): The second input, is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        alpha (number.Number): A scaling factor applied to `other`, default 1.
    
    Returns:
        Tensor, the shape is the same as the one of the input `input`, `other` after broadcasting,
        and the data type is the one with higher precision or higher digits among the two inputs and alpha.
    
    Raises:
        TypeError: If the type of `input`, `other`, or `alpha` is not one of the following: Tensor, number.Number, bool.
        TypeError: If `alpha` is of type float but `input` and `other` are not of type float.
        TypeError: If `alpha` is of type bool but `input` and `other` are not of type bool.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore import Tensor
        >>> from mindspore.ops.extend import sub
        >>> x = Tensor(np.array([4, 5, 6]).astype(np.float32))
        >>> y = Tensor(1, mindspore.int32)
        >>> alpha = 0.5
        >>> output = sub(x, y, alpha)
        >>> print(output)
        [3.5 4.5 5.5]
        >>> # the data type of x is float32, the data type of y is int32,
        >>> # alpha is a float, and the output is the data format of higher precision float32.
        >>> print(output.dtype)
        Float32
    """
    return sub_impl(input, other, alpha)

