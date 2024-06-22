#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Makefile from https://github.com/soulmachine/delimited-protobuf
#
# Copyright Frank Dai https://github.com/soulmachine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""A read/write library for length-delimited protobuf messages"""

from __future__ import absolute_import

from typing import BinaryIO, Optional, Type, TypeVar

from google.protobuf.internal.decoder import _DecodeVarint
from google.protobuf.internal.encoder import _EncodeVarint
from google.protobuf.message import Message

T = TypeVar("YourProtoClass", bound=Message)


def _read_varint(stream: BinaryIO, offset: int = 0) -> int:
    """Read a varint from the stream."""
    if offset > 0:
        stream.seek(offset)
    buf: bytes = stream.read(1)
    if buf == b"":
        return 0  # reached EOF
    while (buf[-1] & 0x80) >> 7 == 1:  # while the MSB is 1
        new_byte = stream.read(1)
        if new_byte == b"":
            raise EOFError("unexpected EOF")
        buf += new_byte
    varint, _ = _DecodeVarint(buf, 0)
    return varint


def read(stream: BinaryIO, proto_class_name: Type[T]) -> Optional[T]:
    """
    Read a single length-delimited message from the given stream.

    Similar to:
      * [`CodedInputStream`](https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/io/coded_stream.h#L66)
      * [`parseDelimitedFrom()`](https://github.com/protocolbuffers/protobuf/blob/master/java/core/src/main/java/com/google/protobuf/Parser.java)
    """
    size = _read_varint(stream)
    if size == 0:
        return None
    buf = stream.read(size)
    msg = proto_class_name()
    msg.ParseFromString(buf)
    return msg


def write(stream: BinaryIO, msg: T):
    """
    Write a single length-delimited message to the given stream.

    Similar to:
      * [`CodedOutputStream`](https://github.com/protocolbuffers/protobuf/blob/master/src/google/protobuf/io/coded_stream.h#L47)
      * [`MessageLite#writeDelimitedTo`](https://github.com/protocolbuffers/protobuf/blob/master/java/core/src/main/java/com/google/protobuf/MessageLite.java#L126)
    """
    assert stream is not None
    _EncodeVarint(stream.write, msg.ByteSize())
    stream.write(msg.SerializeToString())
