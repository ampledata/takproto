#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# constants.py from https://github.com/snstac/takproto
#
# Copyright Sensors & Signals LLC https://www.snstac.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""TAKProto Constants."""

from enum import Enum

DEFAULT_PROTO_HEADER = bytearray(b"\xbf")
DEFAULT_MESH_HEADER = bytearray(b"\xbf\x01\xbf")
DEFAULT_XML_HEADER = bytearray(b"<?xml")

W3C_XML_DATETIME: str = "%Y-%m-%dT%H:%M:%S.%fZ"
ISO_8601_UTC: str = "%Y-%m-%dT%H:%M:%SZ"


class TAKProtoVer(Enum):
    """Enumerator for TAK Protocol Versions."""

    XML = 0
    MESH = 1
    STREAM = 2
