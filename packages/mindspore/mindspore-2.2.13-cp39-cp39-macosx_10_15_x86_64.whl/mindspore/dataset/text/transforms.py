# Copyright 2020-2022 Huawei Technologies Co., Ltd
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
"""
The module text.transforms is inherited from _c_dataengine
and is implemented based on ICU4C and cppjieba in C++.
It's a high performance module to process NLP text.
Users can use Vocab to build their own dictionary,
use appropriate tokenizers to split sentences into different tokens,
and use Lookup to find the index of tokens in Vocab.

.. Note::
    A constructor's arguments for every class in this module must be saved into the
    class attributes (self.xxx) to support save() and load().

Examples:
    >>> import mindspore.dataset as ds
    >>> import mindspore.dataset.text as text
    >>>
    >>> # Create a dataset for text sentences saved as line data in a file
    >>> text_file_list = ["/path/to/text_file_dataset_file"] # contains 1 or multiple text files
    >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list, shuffle=False)
    >>>
    >>> # Tokenize sentences to unicode characters
    >>> tokenizer = text.UnicodeCharTokenizer()
    >>> # Load vocabulary from list
    >>> vocab = text.Vocab.from_list(word_list=['深', '圳', '欢', '迎', '您'])
    >>> # Use Lookup operation to map tokens to ids
    >>> lookup = text.Lookup(vocab=vocab)
    >>> text_file_dataset = text_file_dataset.map(operations=[tokenizer, lookup])
    >>> # if text line in dataset_file is:
    >>> # 深圳欢迎您
    >>> # then the output will be:
    >>> # {'text': array([0, 1, 2, 3, 4], dtype=int32)}
"""
import json
import os
import re
import platform
import numpy as np

import mindspore._c_dataengine as cde
from mindspore.common import dtype as mstype

from .utils import JiebaMode, NormalizeForm, to_str, SPieceTokenizerOutType, SPieceTokenizerLoadType, SentencePieceVocab
from .validators import check_add_token, check_lookup, check_jieba_add_dict, check_to_vectors, \
    check_jieba_add_word, check_jieba_init, check_with_offsets, check_unicode_script_tokenizer, \
    check_wordpiece_tokenizer, check_regex_replace, check_regex_tokenizer, check_basic_tokenizer, check_ngram, \
    check_pair_truncate, check_to_number, check_bert_tokenizer, check_python_tokenizer, check_slidingwindow, \
    check_sentence_piece_tokenizer, check_truncate
from ..core.datatypes import mstype_to_detype
from ..core.validator_helpers import replace_none
from ..transforms.py_transforms_util import Implementation
from ..transforms.transforms import TensorOperation
from ..transforms.validators import invalidate_callable


class TextTensorOperation(TensorOperation):
    """
    Base class of Text Tensor Ops
    """

    def __init__(self):
        super().__init__()
        self.implementation = Implementation.C

    def parse(self):
        raise NotImplementedError("TextTensorOperation has to implement parse() method.")


DE_C_INTER_JIEBA_MODE = {
    JiebaMode.MIX: cde.JiebaMode.DE_JIEBA_MIX,
    JiebaMode.MP: cde.JiebaMode.DE_JIEBA_MP,
    JiebaMode.HMM: cde.JiebaMode.DE_JIEBA_HMM
}

DE_C_INTER_SENTENCEPIECE_LOADTYPE = {
    SPieceTokenizerLoadType.FILE: cde.SPieceTokenizerLoadType.DE_SPIECE_TOKENIZER_LOAD_KFILE,
    SPieceTokenizerLoadType.MODEL: cde.SPieceTokenizerLoadType.DE_SPIECE_TOKENIZER_LOAD_KMODEL
}

DE_C_INTER_SENTENCEPIECE_OUTTYPE = {
    SPieceTokenizerOutType.STRING: cde.SPieceTokenizerOutType.DE_SPIECE_TOKENIZER_OUTTYPE_KString,
    SPieceTokenizerOutType.INT: cde.SPieceTokenizerOutType.DE_SPIECE_TOKENIZER_OUTTYPE_KINT
}


class AddToken(TextTensorOperation):
    """
    Add token to beginning or end of sequence.

    Args:
        token (str): The token to be added.
        begin (bool, optional): Choose the position where the token is inserted. If True,
            the token will be inserted at the beginning of the sequence. Otherwise, it will
            be inserted at the end of the sequence. Default: ``True``.

    Raises:
        TypeError: If `token` is not of type string.
        TypeError: If `begin` is not of type bool.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>>
        >>> dataset = ds.NumpySlicesDataset(data={"text": [['a', 'b', 'c', 'd', 'e']]})
        >>> # Data before
        >>> # |           text            |
        >>> # +---------------------------+
        >>> # | ['a', 'b', 'c', 'd', 'e'] |
        >>> # +---------------------------+
        >>> add_token_op = text.AddToken(token='TOKEN', begin=True)
        >>> dataset = dataset.map(operations=add_token_op)
        >>> # Data after
        >>> # |           text            |
        >>> # +---------------------------+
        >>> # | ['TOKEN', 'a', 'b', 'c', 'd', 'e'] |
        >>> # +---------------------------+

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_add_token
    def __init__(self, token, begin=True):
        super().__init__()
        self.token = token
        self.begin = begin

    def parse(self):
        return cde.AddTokenOperation(self.token, self.begin)


class JiebaTokenizer(TextTensorOperation):
    """
    Use Jieba tokenizer to tokenize Chinese strings.

    Note:
        The dictionary files used by Hidden Markov Model segment and Max Probability segment can be
        obtained through the `cppjieba GitHub <https://github.com/yanyiwu/cppjieba/tree/master/dict>`_ .
        Please ensure the validity and integrity of these files.

    Args:
        hmm_path (str): Path to the dictionary file used by Hidden Markov Model segment.
        mp_path (str): Path to the dictionary file used by Max Probability segment.
        mode (JiebaMode, optional): The desired segment algorithms. See :class:`~.text.JiebaMode`
            for details on optional values. Default: ``JiebaMode.MIX`` .
        with_offsets (bool, optional): Whether to output the start and end offsets of each
            token in the original string. Default: ``False`` .

    Raises:
        TypeError: If `hmm_path` is not of type str.
        TypeError: If `mp_path` is not of type str.
        TypeError: If `mode` is not of type :class:`~.text.JiebaMode` .
        TypeError: If `with_offsets` is not of type bool.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>> from mindspore.dataset.text import JiebaMode
        >>>
        >>> text_file_list = ["/path/to/text_file_dataset_file"]
        >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
        >>>
        >>> # 1) If with_offsets=False, return one data column {["text", dtype=str]}
        >>> jieba_hmm_file = "/path/to/jieba/hmm/file"
        >>> jieba_mp_file = "/path/to/jieba/mp/file"
        >>> tokenizer_op = text.JiebaTokenizer(jieba_hmm_file, jieba_mp_file, mode=JiebaMode.MP, with_offsets=False)
        >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op)
        >>>
        >>> # 2) If with_offsets=True, return three columns {["token", dtype=str], ["offsets_start", dtype=uint32],
        >>> #                                                ["offsets_limit", dtype=uint32]}
        >>> tokenizer_op = text.JiebaTokenizer(jieba_hmm_file, jieba_mp_file, mode=JiebaMode.MP, with_offsets=True)
        >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op, input_columns=["text"],
        ...                                           output_columns=["token", "offsets_start", "offsets_limit"])

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_jieba_init
    def __init__(self, hmm_path, mp_path, mode=JiebaMode.MIX, with_offsets=False):
        super().__init__()
        if not isinstance(mode, JiebaMode):
            raise TypeError("Wrong input type for mode, should be JiebaMode.")

        self.mode = mode
        self.__check_path__(hmm_path)
        self.hmm_path = hmm_path
        self.__check_path__(mp_path)
        self.mp_path = mp_path
        self.with_offsets = with_offsets
        self.words = []

    def __check_path__(self, model_path):
        """check model path"""
        if not os.path.exists(os.path.realpath(model_path)):
            raise ValueError(
                " jieba mode file {} is not exist.".format(model_path))

    def parse(self):
        jieba_tokenizer = cde.JiebaTokenizerOperation(self.hmm_path, self.mp_path,
                                                      DE_C_INTER_JIEBA_MODE.get(self.mode),
                                                      self.with_offsets)
        for word in self.words:
            jieba_tokenizer.add_word(word[0], word[1])
        return jieba_tokenizer

    @invalidate_callable
    @check_jieba_add_word
    def add_word(self, word, freq=None):
        """
        Add a specified word mapping to the Vocab of the tokenizer.

        Args:
            word (str): The word to be added to the Vocab.
            freq (int, optional): The frequency of the word to be added. The higher the word frequency,
                the greater the chance that the word will be tokenized. Default: ``None``, using the
                default word frequency.

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>> from mindspore.dataset.text import JiebaMode
            >>>
            >>> jieba_hmm_file = "/path/to/jieba/hmm/file"
            >>> jieba_mp_file = "/path/to/jieba/mp/file"
            >>> jieba_op = text.JiebaTokenizer(jieba_hmm_file, jieba_mp_file, mode=JiebaMode.MP)
            >>> sentence_piece_vocab_file = "/path/to/sentence/piece/vocab/file"
            >>> with open(sentence_piece_vocab_file, 'r') as f:
            ...     for line in f:
            ...         word = line.split(',')[0]
            ...         jieba_op.add_word(word)
            >>>
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>> text_file_dataset = text_file_dataset.map(operations=jieba_op, input_columns=["text"])
        """

        if freq is None:
            self.words.append((word, 0))
        else:
            self.words.append((word, freq))

    @invalidate_callable
    @check_jieba_add_dict
    def add_dict(self, user_dict):
        """
        Add the specified word mappings to the Vocab of the tokenizer.

        Args:
            user_dict (Union[str, dict[str, int]]): The word mappings to be added to the Vocab.
                If the input type is str, it means the path of the file storing the word mappings to be added.
                Each line of the file should contain two fields separated by a space, where the first field
                indicates the word itself and the second field should be a number indicating the word frequency.
                Invalid lines will be ignored and no error or warning will be returned.
                If the input type is dict[str, int], it means the dictionary storing the word mappings to be added,
                where the key name is the word itself and the key value is the word frequency.

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>> from mindspore.dataset.text import JiebaMode
            >>>
            >>> jieba_hmm_file = "/path/to/jieba/hmm/file"
            >>> jieba_mp_file = "/path/to/jieba/mp/file"
            >>> user_dict = {"男默女泪": 10}
            >>> jieba_op = text.JiebaTokenizer(jieba_hmm_file, jieba_mp_file, mode=JiebaMode.MP)
            >>> jieba_op.add_dict(user_dict)
            >>>
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>> text_file_dataset = text_file_dataset.map(operations=jieba_op, input_columns=["text"])
        """

        if isinstance(user_dict, str):
            self.__add_dict_py_file(user_dict)
        elif isinstance(user_dict, dict):
            for k, v in user_dict.items():
                self.add_word(k, v)
        else:
            raise TypeError("The type of user_dict must str or dict.")

    def __add_dict_py_file(self, file_path):
        """Add user defined word by file"""
        words_list = self.__parser_file(file_path)
        for data in words_list:
            if data[1] is None:
                freq = 0
            else:
                freq = int(data[1])
            self.add_word(data[0], freq)

    def __decode(self, data):
        """decode the dict file to utf8"""
        try:
            data = data.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError("user dict file must be utf8 format.")
        return data.lstrip('\ufeff')

    def __parser_file(self, file_path):
        """parser user defined word by file"""
        if not os.path.exists(file_path):
            raise ValueError(
                "user dict file {} is not exist.".format(file_path))
        real_file_path = os.path.realpath(file_path)
        file_dict = open(real_file_path, "r")
        data_re = re.compile('^\\s*([^\\s*]+?)\\s*([0-9]+)?\\s*$', re.U)
        words_list = []
        for item in file_dict:
            data = item.strip()
            if not isinstance(data, str):
                data = self.__decode(data)
            tmp = data_re.match(data)
            if not tmp:
                continue
            words = tmp.groups()
            words_list.append(words)
        file_dict.close()
        return words_list


class Lookup(TextTensorOperation):
    """
    Look up a word into an id according to the input vocabulary table.

    Args:
        vocab (Vocab): A vocabulary object.
        unknown_token (str, optional): Word is used for lookup. In case of the word is out of vocabulary (OOV),
            the result of lookup will be replaced with unknown_token. If the unknown_token is not specified or
            it is OOV, runtime error will be thrown. Default: ``None``, means no unknown_token is specified.
        data_type (mindspore.dtype, optional): The data type that lookup operation maps
            string to. Default: ``mstype.int32``.

    Raises:
        TypeError: If `vocab` is not of type text.Vocab.
        TypeError: If `unknown_token` is not of type string.
        TypeError: If `data_type` is not of type mindspore.dtype.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>> # Load vocabulary from list
        >>> vocab = text.Vocab.from_list(['深', '圳', '欢', '迎', '您'])
        >>> # Use Lookup operation to map tokens to ids
        >>> lookup = text.Lookup(vocab)
        >>>
        >>> text_file_list = ["/path/to/text_file_dataset_file"]
        >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
        >>> text_file_dataset = text_file_dataset.map(operations=[lookup])

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_lookup
    def __init__(self, vocab, unknown_token=None, data_type=mstype.int32):
        super().__init__()
        self.vocab = vocab
        self.unknown_token = unknown_token
        self.data_type = data_type

    def parse(self):
        return cde.LookupOperation(self.vocab.c_vocab, self.unknown_token, str(mstype_to_detype(self.data_type)))


class Ngram(TextTensorOperation):
    """
    Generate n-gram from a 1-D string Tensor.

    Refer to `N-gram <https://en.wikipedia.org/wiki/N-gram#Examples>`_
    for an overview of what n-gram is and how it works.

    Args:
        n (list[int]): n in n-gram, which is a list of positive integers. For example, if n=[4, 3], then the result
            would be a 4-gram followed by a 3-gram in the same tensor. If the number of words is not enough to make up
            for a n-gram, an empty string will be returned. For example, 3 grams on ["mindspore", "best"] will result in
            an empty string produced.
        left_pad (tuple, optional): Padding performed on left side of the sequence shaped like ("pad_token", pad_width).
            `pad_width` will be capped at n-1. For example, specifying left_pad=("_", 2) would pad left side of the
            sequence with "__". Default: ``('', 0)``.
        right_pad (tuple, optional): Padding performed on right side of the sequence shaped like
            ("pad_token", pad_width). `pad_width` will be capped at n-1. For example, specifying right_pad=("_", 2)
            would pad right side of the sequence with "__". Default: ``('', 0)``.
        separator (str, optional): Symbol used to join strings together. For example, if 2-gram is
            ["mindspore", "amazing"] with separator is ``"-"``, the result would be ["mindspore-amazing"].
            Default: ``' '``, which will use whitespace as separator.

    Raises:
        TypeError: If values of `n` not positive is not of type int.
        ValueError: If values of `n` not positive.
        ValueError: If `left_pad` is not a tuple of length 2.
        ValueError: If `right_pad` is not a tuple of length 2.
        TypeError: If `separator` is not of type string.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>> ngram_op = text.Ngram(3, separator="-")
        >>> output = ngram_op(["WildRose Country", "Canada's Ocean Playground", "Land of Living Skies"])
        >>> # output
        >>> # ["WildRose Country-Canada's Ocean Playground-Land of Living Skies"]
        >>>
        >>> # same ngram_op called through map
        >>> text_file_list = ["/path/to/text_file_dataset_file"]
        >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
        >>> text_file_dataset = text_file_dataset.map(operations=ngram_op)

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_ngram
    def __init__(self, n, left_pad=("", 0), right_pad=("", 0), separator=" "):
        super().__init__()
        self.ngrams = n
        self.left_pad = left_pad
        self.right_pad = right_pad
        self.separator = separator

    def parse(self):
        return cde.NgramOperation(self.ngrams, self.left_pad, self.right_pad, self.separator)


class PythonTokenizer:
    """
    Class that applies user-defined string tokenizer into input string.

    Args:
        tokenizer (Callable): Python function that takes a `str` and returns a list of `str` as tokens.

    Raises:
        TypeError: If `tokenizer` is not a callable Python function.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>>
        >>> def my_tokenizer(line):
        ...     return line.split()
        >>>
        >>> text_file_list = ["/path/to/text_file_dataset_file"]
        >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
        >>> text_file_dataset = text_file_dataset.map(operations=text.PythonTokenizer(my_tokenizer))

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_python_tokenizer
    def __init__(self, tokenizer):
        self.pyfunc = tokenizer
        self.tokenizer = np.vectorize(lambda x: np.array(tokenizer(x), dtype='U'), signature='()->(n)')
        self.random = False

    def __call__(self, in_array):
        if not isinstance(in_array, np.ndarray):
            raise TypeError("input should be a NumPy array. Got {}.".format(type(in_array)))
        if in_array.dtype.type is np.bytes_:
            in_array = to_str(in_array)
        try:
            tokens = self.tokenizer(in_array)
        except Exception as e:
            raise RuntimeError("Error occurred in Pyfunc [" + str(self.pyfunc.__name__) + "], error message: " + str(e))
        return tokens

    def to_json(self):
        json_obj = {}
        json_obj["tensor_op_name"] = self.pyfunc.__name__
        json_obj["python_module"] = self.__class__.__module__
        return json.dumps(json_obj)


class SentencePieceTokenizer(TextTensorOperation):
    """
    Tokenize scalar token or 1-D tokens to tokens by sentencepiece.

    Args:
        mode (Union[str, SentencePieceVocab]): SentencePiece model.
            If the input parameter is a file, it represents the path of SentencePiece mode to be loaded.
            If the input parameter is a SentencePieceVocab object, it should be constructed in advanced.
        out_type (SPieceTokenizerOutType): The type of output, it can be ``SPieceTokenizerOutType.STRING``,
            ``SPieceTokenizerOutType.INT``.

            - ``SPieceTokenizerOutType.STRING``, means output type of SentencePice Tokenizer is string.
            - ``SPieceTokenizerOutType.INT``, means output type of SentencePice Tokenizer is int.

    Raises:
        TypeError: If `mode` is not of type string or SentencePieceVocab.
        TypeError: If `out_type` is not of type SPieceTokenizerOutType.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>> from mindspore.dataset.text import SentencePieceModel, SPieceTokenizerOutType
        >>>
        >>> sentence_piece_vocab_file = "/path/to/sentence/piece/vocab/file"
        >>> vocab = text.SentencePieceVocab.from_file([sentence_piece_vocab_file], 5000, 0.9995,
        ...                                           SentencePieceModel.UNIGRAM, {})
        >>> tokenizer = text.SentencePieceTokenizer(vocab, out_type=SPieceTokenizerOutType.STRING)
        >>>
        >>> text_file_list = ["/path/to/text_file_dataset_file"]
        >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
        >>> text_file_dataset = text_file_dataset.map(operations=tokenizer)

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_sentence_piece_tokenizer
    def __init__(self, mode, out_type):
        super().__init__()
        self.mode = mode
        self.out_type = out_type

    def parse(self):
        self.mode = self.mode.c_sentence_piece_vocab if isinstance(self.mode, SentencePieceVocab) else self.mode
        return cde.SentencePieceTokenizerOperation(self.mode, DE_C_INTER_SENTENCEPIECE_OUTTYPE.get(self.out_type))


class SlidingWindow(TextTensorOperation):
    """
    Construct a tensor from given data (only support 1-D for now), where each element in the dimension axis
    is a slice of data starting at the corresponding position, with a specified width.

    Args:
        width (int): The width of the window. It must be an integer and greater than zero.
        axis (int, optional): The axis along which the sliding window is computed. Default: ``0``.

    Raises:
        TypeError: If `width` is not of type int.
        ValueError: If value of `width` is not positive.
        TypeError: If `axis` is not of type int.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>>
        >>> dataset = ds.NumpySlicesDataset(data=[[1, 2, 3, 4, 5]], column_names="col1")
        >>> # Data before
        >>> # |     col1     |
        >>> # +--------------+
        >>> # | [[1, 2, 3, 4, 5]] |
        >>> # +--------------+
        >>> dataset = dataset.map(operations=text.SlidingWindow(3, 0))
        >>> # Data after
        >>> # |     col1     |
        >>> # +--------------+
        >>> # |  [[1, 2, 3], |
        >>> # |   [2, 3, 4], |
        >>> # |   [3, 4, 5]] |
        >>> # +--------------+

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_slidingwindow
    def __init__(self, width, axis=0):
        super().__init__()
        self.width = width
        self.axis = axis

    def parse(self):
        return cde.SlidingWindowOperation(self.width, self.axis)


class ToNumber(TextTensorOperation):
    """
    Tensor operation to convert every element of a string tensor to a number.

    Strings are cast according to the rules specified in the following links, except that any strings which represent
    negative numbers cannot be cast to an unsigned integer type, rules links are as follows:
    https://en.cppreference.com/w/cpp/string/basic_string/stof,
    https://en.cppreference.com/w/cpp/string/basic_string/stoul.

    Args:
        data_type (mindspore.dtype): Type to be cast to. Must be a numeric type in mindspore.dtype.

    Raises:
        TypeError: If `data_type` is not of type mindspore.dtype.
        RuntimeError: If strings are invalid to cast, or are out of range after being cast.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>> from mindspore import dtype as mstype
        >>>
        >>> data = [["1", "2", "3"]]
        >>> dataset = ds.NumpySlicesDataset(data)
        >>> to_number_op = text.ToNumber(mstype.int8)
        >>> dataset = dataset.map(operations=to_number_op)

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_to_number
    def __init__(self, data_type):
        super().__init__()
        data_type = mstype_to_detype(data_type)
        self.data_type = str(data_type)

    def parse(self):
        return cde.ToNumberOperation(self.data_type)


class ToVectors(TextTensorOperation):
    """
    Look up a token into vectors according to the input vector table.

    Args:
        vectors (Vectors): A vectors object.
        unk_init (sequence, optional): Sequence used to initialize out-of-vectors (OOV) token.
            Default: ``None``, initialize with zero vectors.
        lower_case_backup (bool, optional): Whether to look up the token in the lower case. If ``False``,
            each token in the original case will be looked up; if ``True``, each token in the original
            case will be looked up first, if not found in the keys of the property stoi, the token in the
            lower case will be looked up. Default: ``False``.

    Raises:
        TypeError: If `unk_init` is not of type sequence.
        TypeError: If elements of `unk_init` is not of type float or int.
        TypeError: If `lower_case_backup` is not of type bool.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>>
        >>> # Load vectors from file
        >>> vectors = text.Vectors.from_file("/path/to/vectors/file")
        >>> # Use ToVectors operation to map tokens to vectors
        >>> to_vectors = text.ToVectors(vectors)
        >>>
        >>> text_file_list = ["/path/to/text_file_dataset_file"]
        >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
        >>> text_file_dataset = text_file_dataset.map(operations=[to_vectors])

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_to_vectors
    def __init__(self, vectors, unk_init=None, lower_case_backup=False):
        super().__init__()
        self.vectors = vectors
        self.unk_init = unk_init if unk_init is not None else []
        self.lower_case_backup = lower_case_backup

    def parse(self):
        return cde.ToVectorsOperation(self.vectors, self.unk_init, self.lower_case_backup)


class Truncate(TextTensorOperation):
    """
    Truncate the input sequence so that it does not exceed the maximum length.

    Args:
        max_seq_len (int): Maximum allowable length.

    Raises:
        TypeError: If `max_length_len` is not of type int.
        ValueError: If value of `max_length_len` is not greater than or equal to 0.
        RuntimeError: If the input tensor is not of dtype bool, int, float, double or str.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>>
        >>> dataset = ds.NumpySlicesDataset(data=[['a', 'b', 'c', 'd', 'e']], column_names=["text"], shuffle=False)
        >>> # Data before
        >>> # |           col1            |
        >>> # +---------------------------+
        >>> # | ['a', 'b', 'c', 'd', 'e'] |
        >>> # +---------------------------+
        >>> truncate = text.Truncate(4)
        >>> dataset = dataset.map(operations=truncate, input_columns=["text"])
        >>> # Data after
        >>> # |          col1          |
        >>> # +------------------------+
        >>> # |  ['a', 'b', 'c', 'd']  |
        >>> # +------------------------+

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_truncate
    def __init__(self, max_seq_len):
        super().__init__()
        self.max_seq_len = max_seq_len

    def parse(self):
        return cde.TruncateOperation(self.max_seq_len)


class TruncateSequencePair(TextTensorOperation):
    """
    Truncate a pair of 1-D string input so that their total length is less than the specified length.

    Args:
        max_length (int): The maximum total length of the output strings. If it is no less than the
            total length of the original pair of strings, no truncation is performed; otherwise, the
            longer of the two input strings is truncated until its total length equals this value.

    Raises:
        TypeError: If `max_length` is not of type int.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>>
        >>> dataset = ds.NumpySlicesDataset(data={"col1": [[1, 2, 3]], "col2": [[4, 5]]})
        >>> # Data before
        >>> # |   col1    |   col2    |
        >>> # +-----------+-----------|
        >>> # | [1, 2, 3] |  [4, 5]   |
        >>> # +-----------+-----------+
        >>> truncate_sequence_pair_op = text.TruncateSequencePair(max_length=4)
        >>> dataset = dataset.map(operations=truncate_sequence_pair_op)
        >>> # Data after
        >>> # |   col1    |   col2    |
        >>> # +-----------+-----------+
        >>> # |  [1, 2]   |  [4, 5]   |
        >>> # +-----------+-----------+

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_pair_truncate
    def __init__(self, max_length):
        super().__init__()
        self.max_length = max_length

    def parse(self):
        return cde.TruncateSequencePairOperation(self.max_length)


class UnicodeCharTokenizer(TextTensorOperation):
    """
    Unpack the Unicode characters in the input strings.

    Args:
        with_offsets (bool, optional): Whether to output the start and end offsets of each
            token in the original string. Default: ``False`` .

    Raises:
        TypeError: If `with_offsets` is not of type bool.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>>
        >>> text_file_list = ["/path/to/text_file_dataset_file"]
        >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
        >>>
        >>> # If with_offsets=False, default output one column {["text", dtype=str]}
        >>> tokenizer_op = text.UnicodeCharTokenizer(with_offsets=False)
        >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op)
        >>>
        >>> # If with_offsets=True, then output three columns {["token", dtype=str], ["offsets_start", dtype=uint32],
        >>> #                                                   ["offsets_limit", dtype=uint32]}
        >>> tokenizer_op = text.UnicodeCharTokenizer(with_offsets=True)
        >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op, input_columns=["text"],
        ...                                           output_columns=["token", "offsets_start", "offsets_limit"])

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_with_offsets
    def __init__(self, with_offsets=False):
        super().__init__()
        self.with_offsets = with_offsets

    def parse(self):
        return cde.UnicodeCharTokenizerOperation(self.with_offsets)


class WordpieceTokenizer(TextTensorOperation):
    """
    Tokenize the input text to subword tokens.

    Args:
        vocab (Vocab): Vocabulary used to look up words.
        suffix_indicator (str, optional): Prefix flags used to indicate subword suffixes. Default: ``'##'``.
        max_bytes_per_token (int, optional): The maximum length of tokenization, words exceeding this length will
                not be split. Default: ``100``.
        unknown_token (str, optional): The output for unknown words. When set to an empty string, the corresponding
                unknown word will be directly returned as the output. Otherwise, the set string will be returned as the
                output. Default: ``'[UNK]'``.
        with_offsets (bool, optional): Whether to output the start and end offsets of each
            token in the original string. Default: ``False`` .

    Raises:
        TypeError: If `vocab` is not of type :class:`mindspore.dataset.text.Vocab` .
        TypeError: If `suffix_indicator` is not of type str.
        TypeError: If `max_bytes_per_token` is not of type int.
        TypeError: If `unknown_token` is not of type str.
        TypeError: If `with_offsets` is not of type bool.
        ValueError: If `max_bytes_per_token` is negative.

    Supported Platforms:
        ``CPU``

    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.dataset.text as text
        >>>
        >>> text_file_list = ["/path/to/text_file_dataset_file"]
        >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
        >>>
        >>> vocab_list = ["book", "cholera", "era", "favor", "##ite", "my", "is", "love", "dur", "##ing", "the"]
        >>> vocab = text.Vocab.from_list(vocab_list)
        >>>
        >>> # If with_offsets=False, default output one column {["text", dtype=str]}
        >>> tokenizer_op = text.WordpieceTokenizer(vocab=vocab, unknown_token='[UNK]',
        ...                                        max_bytes_per_token=100, with_offsets=False)
        >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op)
        >>>
        >>> # If with_offsets=True, then output three columns {["token", dtype=str], ["offsets_start", dtype=uint32],
        >>> #                                                   ["offsets_limit", dtype=uint32]}
        >>> tokenizer_op = text.WordpieceTokenizer(vocab=vocab, unknown_token='[UNK]',
        ...                                       max_bytes_per_token=100, with_offsets=True)
        >>>
        >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op, input_columns=["text"],
        ...                                           output_columns=["token", "offsets_start", "offsets_limit"])

    Tutorial Examples:
        - `Illustration of text transforms
          <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
    """

    @check_wordpiece_tokenizer
    def __init__(self, vocab, suffix_indicator='##', max_bytes_per_token=100, unknown_token='[UNK]',
                 with_offsets=False):
        super().__init__()
        self.vocab = vocab
        self.suffix_indicator = suffix_indicator
        self.max_bytes_per_token = max_bytes_per_token
        self.unknown_token = unknown_token
        self.with_offsets = with_offsets

    def parse(self):
        return cde.WordpieceTokenizerOperation(self.vocab.c_vocab, self.suffix_indicator, self.max_bytes_per_token,
                                               self.unknown_token, self.with_offsets)


if platform.system().lower() != 'windows':
    DE_C_INTER_NORMALIZE_FORM = {
        NormalizeForm.NONE: cde.NormalizeForm.DE_NORMALIZE_NONE,
        NormalizeForm.NFC: cde.NormalizeForm.DE_NORMALIZE_NFC,
        NormalizeForm.NFKC: cde.NormalizeForm.DE_NORMALIZE_NFKC,
        NormalizeForm.NFD: cde.NormalizeForm.DE_NORMALIZE_NFD,
        NormalizeForm.NFKD: cde.NormalizeForm.DE_NORMALIZE_NFKD
    }


    class BasicTokenizer(TextTensorOperation):
        """
        Tokenize the input UTF-8 encoded string by specific rules.

        Note:
            `BasicTokenizer` is not supported on Windows platform yet.

        Args:
            lower_case (bool, optional): Whether to perform lowercase processing on the text. If True, will fold the
                text to lower case and strip accented characters. If False, will only perform normalization on the
                text, with mode specified by `normalization_form` . Default: ``False``.
            keep_whitespace (bool, optional): If True, the whitespace will be kept in the output. Default: ``False``.
            normalization_form (NormalizeForm, optional): The desired normalization form.
                See :class:`~.text.NormalizeForm` for details on optional values.
                Default: ``NormalizeForm.NFKC`` .
            preserve_unused_token (bool, optional): Whether to preserve special tokens. If True, will not split special
                tokens like '[CLS]', '[SEP]', '[UNK]', '[PAD]', '[MASK]'. Default: ``True``.
            with_offsets (bool, optional): Whether to output the start and end offsets of each
                token in the original string. Default: ``False`` .

        Raises:
            TypeError: If `lower_case` is not of type bool.
            TypeError: If `keep_whitespace` is not of type bool.
            TypeError: If `normalization_form` is not of type :class:`~.text.NormalizeForm` .
            TypeError: If `preserve_unused_token` is not of type bool.
            TypeError: If `with_offsets` is not of type bool.
            RuntimeError: If dtype of input Tensor is not str.

        Supported Platforms:
            ``CPU``

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>> from mindspore.dataset.text import NormalizeForm
            >>>
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>>
            >>> # 1) If with_offsets=False, default output one column {["text", dtype=str]}
            >>> tokenizer_op = text.BasicTokenizer(lower_case=False,
            ...                                    keep_whitespace=False,
            ...                                    normalization_form=NormalizeForm.NONE,
            ...                                    preserve_unused_token=True,
            ...                                    with_offsets=False)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op)
            >>> # 2) If with_offsets=True, then output three columns {["token", dtype=str],
            >>> #                                                     ["offsets_start", dtype=uint32],
            >>> #                                                     ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.BasicTokenizer(lower_case=False,
            ...                                    keep_whitespace=False,
            ...                                    normalization_form=NormalizeForm.NONE,
            ...                                    preserve_unused_token=True,
            ...                                    with_offsets=True)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op, input_columns=["text"],
            ...                                           output_columns=["token", "offsets_start", "offsets_limit"])

        Tutorial Examples:
            - `Illustration of text transforms
              <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
        """

        @check_basic_tokenizer
        def __init__(self, lower_case=False, keep_whitespace=False, normalization_form=NormalizeForm.NONE,
                     preserve_unused_token=True, with_offsets=False):
            super().__init__()
            if not isinstance(normalization_form, NormalizeForm):
                raise TypeError("Wrong input type for normalization_form, should be enum of 'NormalizeForm'.")

            self.lower_case = lower_case
            self.keep_whitespace = keep_whitespace
            self.normalization_form = DE_C_INTER_NORMALIZE_FORM.get(normalization_form)
            self.preserve_unused_token = preserve_unused_token
            self.with_offsets = with_offsets

        def parse(self):
            return cde.BasicTokenizerOperation(self.lower_case, self.keep_whitespace, self.normalization_form,
                                               self.preserve_unused_token, self.with_offsets)


    class BertTokenizer(TextTensorOperation):
        """
        Tokenizer used for Bert text process.

        Note:
            `BertTokenizer` is not supported on Windows platform yet.

        Args:
            vocab (Vocab): Vocabulary used to look up words.
            suffix_indicator (str, optional): Prefix flags used to indicate subword suffixes. Default: ``'##'``.
            max_bytes_per_token (int, optional): The maximum length of tokenization, words exceeding this length will
                not be split. Default: ``100``.
            unknown_token (str, optional): The output for unknown words. When set to an empty string, the corresponding
                unknown word will be directly returned as the output. Otherwise, the set string will be returned as the
                output. Default: ``'[UNK]'``.
            lower_case (bool, optional): Whether to perform lowercase processing on the text. If ``True``, will fold the
                text to lower case and strip accented characters. If ``False``, will only perform normalization on the
                text, with mode specified by `normalization_form` . Default: ``False``.
            keep_whitespace (bool, optional): If ``True``, the whitespace will be kept in the output.
                Default: ``False``.
            normalization_form (NormalizeForm, optional): The desired normalization form.
                See :class:`~.text.NormalizeForm` for details on optional values.
                Default: ``NormalizeForm.NFKC`` .
            preserve_unused_token (bool, optional): Whether to preserve special tokens. If ``True``,
                will not split special tokens like '[CLS]', '[SEP]', '[UNK]', '[PAD]', '[MASK]'.
                Default: ``True``.
            with_offsets (bool, optional): Whether to output the start and end offsets of each
                token in the original string. Default: ``False`` .

        Raises:
            TypeError: If `vocab` is not of type :class:`mindspore.dataset.text.Vocab` .
            TypeError: If `suffix_indicator` is not of type str.
            TypeError: If `max_bytes_per_token` is not of type int.
            ValueError: If `max_bytes_per_token` is negative.
            TypeError: If `unknown_token` is not of type str.
            TypeError: If `lower_case` is not of type bool.
            TypeError: If `keep_whitespace` is not of type bool.
            TypeError: If `normalization_form` is not of type :class:`~.text.NormalizeForm` .
            TypeError: If `preserve_unused_token` is not of type bool.
            TypeError: If `with_offsets` is not of type bool.

        Supported Platforms:
            ``CPU``

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>> from mindspore.dataset.text import NormalizeForm
            >>>
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>>
            >>> # 1) If with_offsets=False, default output one column {["text", dtype=str]}
            >>> vocab_list = ["床", "前", "明", "月", "光", "疑", "是", "地", "上", "霜", "举", "头", "望", "低",
            ...               "思", "故", "乡","繁", "體", "字", "嘿", "哈", "大", "笑", "嘻", "i", "am", "mak",
            ...               "make", "small", "mistake", "##s", "during", "work", "##ing", "hour", "😀", "😃",
            ...               "😄", "😁", "+", "/", "-", "=", "12", "28", "40", "16", " ", "I", "[CLS]", "[SEP]",
            ...               "[UNK]", "[PAD]", "[MASK]", "[unused1]", "[unused10]"]
            >>> vocab = text.Vocab.from_list(vocab_list)
            >>> tokenizer_op = text.BertTokenizer(vocab=vocab, suffix_indicator='##', max_bytes_per_token=100,
            ...                                   unknown_token='[UNK]', lower_case=False, keep_whitespace=False,
            ...                                   normalization_form=NormalizeForm.NONE, preserve_unused_token=True,
            ...                                   with_offsets=False)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op)
            >>> # 2) If with_offsets=True, then output three columns {["token", dtype=str],
            >>> #                                                     ["offsets_start", dtype=uint32],
            >>> #                                                     ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.BertTokenizer(vocab=vocab, suffix_indicator='##', max_bytes_per_token=100,
            ...                                   unknown_token='[UNK]', lower_case=False, keep_whitespace=False,
            ...                                   normalization_form=NormalizeForm.NONE, preserve_unused_token=True,
            ...                                   with_offsets=True)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op, input_columns=["text"],
            ...                                               output_columns=["token", "offsets_start",
            ...                                                               "offsets_limit"])

        Tutorial Examples:
            - `Illustration of text transforms
              <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
        """

        @check_bert_tokenizer
        def __init__(self, vocab, suffix_indicator='##', max_bytes_per_token=100, unknown_token='[UNK]',
                     lower_case=False, keep_whitespace=False, normalization_form=NormalizeForm.NONE,
                     preserve_unused_token=True, with_offsets=False):
            super().__init__()
            if not isinstance(normalization_form, NormalizeForm):
                raise TypeError("Wrong input type for normalization_form, should be enum of 'NormalizeForm'.")

            self.vocab = vocab
            self.suffix_indicator = suffix_indicator
            self.max_bytes_per_token = max_bytes_per_token
            self.unknown_token = unknown_token
            self.lower_case = lower_case
            self.keep_whitespace = keep_whitespace
            self.normalization_form = DE_C_INTER_NORMALIZE_FORM.get(normalization_form)
            self.preserve_unused_token = preserve_unused_token
            self.with_offsets = with_offsets

        def parse(self):
            return cde.BertTokenizerOperation(self.vocab.c_vocab, self.suffix_indicator, self.max_bytes_per_token,
                                              self.unknown_token, self.lower_case, self.keep_whitespace,
                                              self.normalization_form, self.preserve_unused_token, self.with_offsets)


    class CaseFold(TextTensorOperation):
        """
        Apply case fold operation on UTF-8 string tensor, which is aggressive that can convert more characters into
        lower case than :code:`str.lower` . For supported normalization forms, please refer to
        `ICU_Normalizer2 <https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/classicu_1_1Normalizer2.html>`_ .

        Note:
            CaseFold is not supported on Windows platform yet.

        Supported Platforms:
            ``CPU``

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>> case_op = text.CaseFold()
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>> text_file_dataset = text_file_dataset.map(operations=case_op)

        Tutorial Examples:
            - `Illustration of text transforms
              <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
        """

        def parse(self):
            return cde.CaseFoldOperation()


    class FilterWikipediaXML(TextTensorOperation):
        """
        Filter Wikipedia XML dumps to "clean" text consisting only of lowercase letters (a-z, converted from A-Z),
        and spaces (never consecutive).

        Note:
            FilterWikipediaXML is not supported on Windows platform yet.

        Supported Platforms:
            ``CPU``

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>>
            >>> replace_op = text.FilterWikipediaXML()
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>> text_file_dataset = text_file_dataset.map(operations=replace_op)

        Tutorial Examples:
            - `Illustration of text transforms
              <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
        """

        def parse(self):
            return cde.FilterWikipediaXMLOperation()


    class NormalizeUTF8(TextTensorOperation):
        """
        Normalize the input UTF-8 encoded strings.

        Note:
            NormalizeUTF8 is not supported on Windows platform yet.

        Args:
            normalize_form (NormalizeForm, optional): The desired normalization form.
                See :class:`~.text.NormalizeForm` for details on optional values.
                Default: ``NormalizeForm.NFKC`` .

        Raises:
            TypeError: If `normalize_form` is not of type :class:`~.text.NormalizeForm`.

        Supported Platforms:
            ``CPU``

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>> from mindspore.dataset.text import NormalizeForm
            >>>
            >>> normalize_op = text.NormalizeUTF8(normalize_form=NormalizeForm.NFC)
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>> text_file_dataset = text_file_dataset.map(operations=normalize_op)

        Tutorial Examples:
            - `Illustration of text transforms
              <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
        """

        def __init__(self, normalize_form=NormalizeForm.NFKC):
            super().__init__()
            if not isinstance(normalize_form, NormalizeForm):
                raise TypeError("Wrong input type for normalization_form, should be enum of 'NormalizeForm'.")

            normalize_form = replace_none(normalize_form, NormalizeForm.NFKC)
            self.normalize_form = DE_C_INTER_NORMALIZE_FORM.get(normalize_form)

        def parse(self):
            return cde.NormalizeUTF8Operation(self.normalize_form)


    class RegexReplace(TextTensorOperation):
        """
        Replace part of the input UTF-8 string with a difference text string using regular expressions.

        Note:
            RegexReplace is not supported on Windows platform yet.

        Args:
            pattern (str): The regular expression, used to mean the specific, standard textual syntax for
                representing patterns for matching text.
            replace (str): The string used to replace the matched elements.
            replace_all (bool, optional): Whether to replace all matched elements. If ``False``, only the
                first matched element will be replaced; otherwise, all matched elements will be replaced.
                Default: ``True``.

        Raises:
            TypeError: If `pattern` is not of type str.
            TypeError: If `replace` is not of type str.
            TypeError: If `replace_all` is not of type bool.

        Supported Platforms:
            ``CPU``

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>>
            >>> regex_replace = text.RegexReplace('apple', 'orange')
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>> text_file_dataset = text_file_dataset.map(operations=regex_replace)

        Tutorial Examples:
            - `Illustration of text transforms
              <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
        """

        @check_regex_replace
        def __init__(self, pattern, replace, replace_all=True):
            super().__init__()
            self.pattern = pattern
            self.replace = replace
            self.replace_all = replace_all

        def parse(self):
            return cde.RegexReplaceOperation(self.pattern, self.replace, self.replace_all)


    class RegexTokenizer(TextTensorOperation):
        """
        Tokenize a scalar tensor of UTF-8 string by regex expression pattern.

        See https://unicode-org.github.io/icu/userguide/strings/regexp.html for supported regex pattern.

        Note:
            RegexTokenizer is not supported on Windows platform yet.

        Args:
            delim_pattern (str): The pattern of regex delimiters.
                The original string will be split by matched elements.
            keep_delim_pattern (str, optional): The string matched by 'delim_pattern' can be kept as a token
                if it can be matched by 'keep_delim_pattern'. The default value is an empty str
                which means that delimiters will not be kept as an output token. Default: ``''``.
            with_offsets (bool, optional): Whether to output the start and end offsets of each
                token in the original string. Default: ``False`` .

        Raises:
            TypeError: If `delim_pattern` is not of type string.
            TypeError: If `keep_delim_pattern` is not of type string.
            TypeError: If `with_offsets` is not of type bool.

        Supported Platforms:
            ``CPU``

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>>
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>>
            >>> # 1) If with_offsets=False, default output is one column {["text", dtype=str]}
            >>> delim_pattern = r"[ |,]"
            >>> tokenizer_op = text.RegexTokenizer(delim_pattern, with_offsets=False)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op)
            >>>
            >>> # 2) If with_offsets=True, then output three columns {["token", dtype=str],
            >>> #                                                     ["offsets_start", dtype=uint32],
            >>> #                                                     ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.RegexTokenizer(delim_pattern, with_offsets=True)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op, input_columns=["text"],
            ...                                           output_columns=["token", "offsets_start", "offsets_limit"])

        Tutorial Examples:
            - `Illustration of text transforms
              <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
        """

        @check_regex_tokenizer
        def __init__(self, delim_pattern, keep_delim_pattern='', with_offsets=False):
            super().__init__()
            self.delim_pattern = delim_pattern
            self.keep_delim_pattern = keep_delim_pattern
            self.with_offsets = with_offsets

        def parse(self):
            return cde.RegexTokenizerOperation(self.delim_pattern, self.keep_delim_pattern, self.with_offsets)


    class UnicodeScriptTokenizer(TextTensorOperation):
        """
        Tokenize a scalar tensor of UTF-8 string based on Unicode script boundaries.

        Note:
            UnicodeScriptTokenizer is not supported on Windows platform yet.

        Args:
            keep_whitespace (bool, optional): Whether or not emit whitespace tokens. Default: ``False``.
            with_offsets (bool, optional): Whether to output the start and end offsets of each
                token in the original string. Default: ``False`` .

        Raises:
            TypeError: If `keep_whitespace` is not of type bool.
            TypeError: If `with_offsets` is not of type bool.

        Supported Platforms:
            ``CPU``

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>>
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>>
            >>> # 1) If with_offsets=False, default output one column {["text", dtype=str]}
            >>> tokenizer_op = text.UnicodeScriptTokenizer(keep_whitespace=True, with_offsets=False)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op)
            >>>
            >>> # 2) If with_offsets=True, then output three columns {["token", dtype=str],
            >>> #                                                     ["offsets_start", dtype=uint32],
            >>> #                                                     ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.UnicodeScriptTokenizer(keep_whitespace=True, with_offsets=True)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op, input_columns=["text"],
            ...                                           output_columns=["token", "offsets_start", "offsets_limit"])

        Tutorial Examples:
            - `Illustration of text transforms
              <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_

        """

        @check_unicode_script_tokenizer
        def __init__(self, keep_whitespace=False, with_offsets=False):
            super().__init__()
            keep_whitespace = replace_none(keep_whitespace, False)
            with_offsets = replace_none(with_offsets, False)
            self.keep_whitespace = keep_whitespace
            self.with_offsets = with_offsets

        def parse(self):
            return cde.UnicodeScriptTokenizerOperation(self.keep_whitespace, self.with_offsets)


    class WhitespaceTokenizer(TextTensorOperation):
        """
        Tokenize a scalar tensor of UTF-8 string on ICU4C defined whitespaces, such as: ' ', '\\\\t', '\\\\r', '\\\\n'.

        Note:
            WhitespaceTokenizer is not supported on Windows platform yet.

        Args:
            with_offsets (bool, optional): Whether to output the start and end offsets of each
                token in the original string. Default: ``False`` .

        Raises:
            TypeError: If `with_offsets` is not of type bool.

        Supported Platforms:
            ``CPU``

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>>
            >>> text_file_list = ["/path/to/text_file_dataset_file"]
            >>> text_file_dataset = ds.TextFileDataset(dataset_files=text_file_list)
            >>>
            >>> # 1) If with_offsets=False, default output one column {["text", dtype=str]}
            >>> tokenizer_op = text.WhitespaceTokenizer(with_offsets=False)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op)
            >>>
            >>> # 2) If with_offsets=True, then output three columns {["token", dtype=str],
            >>> #                                                   ["offsets_start", dtype=uint32],
            >>> #                                                   ["offsets_limit", dtype=uint32]}
            >>> tokenizer_op = text.WhitespaceTokenizer(with_offsets=True)
            >>> text_file_dataset = text_file_dataset.map(operations=tokenizer_op, input_columns=["text"],
            ...                                           output_columns=["token", "offsets_start", "offsets_limit"])

        Tutorial Examples:
            - `Illustration of text transforms
              <https://www.mindspore.cn/docs/en/r2.2/api_python/samples/dataset/text_gallery.html>`_
        """

        @check_with_offsets
        def __init__(self, with_offsets=False):
            super().__init__()
            self.with_offsets = with_offsets

        def parse(self):
            return cde.WhitespaceTokenizerOperation(self.with_offsets)
