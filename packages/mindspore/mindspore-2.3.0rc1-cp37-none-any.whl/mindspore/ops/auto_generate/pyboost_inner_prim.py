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

from mindspore.common._stub_tensor import _convert_stub
from mindspore.ops.auto_generate.gen_arg_handler import *
from mindspore._c_expression import ArgMaxWithValuePrim_
from mindspore._c_expression import ArgMinWithValuePrim_
from mindspore._c_expression import BroadcastToPrim_
from mindspore._c_expression import ConcatPrim_
from mindspore._c_expression import ReduceAnyPrim_
from mindspore._c_expression import SoftmaxPrim_


class _PyboostArgMaxWithValuePrim(ArgMaxWithValuePrim_):
    def __call__(self, input, axis, keep_dims):

        return _convert_stub(super().__call__(input, axis, keep_dims))


argmax_with_value_impl = _PyboostArgMaxWithValuePrim()


class _PyboostArgMinWithValuePrim(ArgMinWithValuePrim_):
    def __call__(self, input, axis, keep_dims):

        return _convert_stub(super().__call__(input, axis, keep_dims))


argmin_with_value_impl = _PyboostArgMinWithValuePrim()


class _PyboostBroadcastToPrim(BroadcastToPrim_):
    def __call__(self, input, shape):

        return _convert_stub(super().__call__(input, shape))


broadcast_to_impl = _PyboostBroadcastToPrim()


class _PyboostConcatPrim(ConcatPrim_):
    def __call__(self, tensors, axis):

        return _convert_stub(super().__call__(tensors, axis))


concat_impl = _PyboostConcatPrim()


class _PyboostReduceAnyPrim(ReduceAnyPrim_):
    def __call__(self, x, axis, keep_dims):

        return _convert_stub(super().__call__(x, axis, keep_dims))


reduce_any_impl = _PyboostReduceAnyPrim()


class _PyboostSoftmaxPrim(SoftmaxPrim_):
    def __call__(self, input, axis):

        return _convert_stub(super().__call__(input, axis))


softmax_impl = _PyboostSoftmaxPrim()
