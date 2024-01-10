#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

"""A Python module to encode & decode 'TAK Protocol Payload - Version 1' Protocol Buffer based Cursor on Target (CoT) messages.

:author: Greg Albrecht <gba@snstac.com>
:copyright: Copyright Sensors & Signals LLC https://www.snstac.com
:license: MIT License
:source: <https://github.com/snstac/takproto>
"""

__version__ = "2.1.0-beta1"

# Python 3.6 test/build work-around:
try:
    from .functions import (  # NOQA
        xml2proto,
        parse_proto,
        parse_mesh,
        parse_stream,
        format_time,
    )
    from .constants import TAKProtoVer  # NOQA
except ImportError:
    import warnings

    warnings.warn(
        "Unable to import required modules, ignoring (Python 3.6 build work-around)."
    )

__author__ = "Greg Albrecht <gba@snstac.com>"
__copyright__ = "Copyright Sensors & Signals LLC https://www.snstac.com"
__license__ = "MIT License"
__source__ = "https://github.com/snstac/takproto"
