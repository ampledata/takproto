.. image:: ./docs/pytak_logo-256x264.png
    :alt: PyTAK Logo

takproto: TAK Protocol Python Module
************************************

``takproto`` is a Python module to encode & decode TAK Protocol Cursor on Target (CoT) messages.

Documentation
=============

See `PyTAK documentation <https://pytak.rtfd.io/>`_ for instructions on getting 
started with PyTAK, examples, configuration & troubleshooting options.

License
=======
Copyright Sensors & Signals LLC https://www.snstac.com

Copyright 2020 Delta Bravo-15 <deltabravo15ga@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Origin
======

``takproto`` is a fork & complete re-write of @dB-SPL's 
`takprotobuf <https://github.com/dB-SPL/takprotobuf>`_.

Notable differences between the original ``takprotobuf`` & this module ``takproto``:

1. Rebuild proto files using `Protocol Buffers v21 <https://protobuf.dev/>`_.
2. Added support for encoding & decoding plain XML, Mesh & Stream TAK Protocol formats.
3. Remove dependency on ``untangle`` module, allowing compatibility with Python 3.6 
   through 3.10. Unfortunately many single-board computers (i.e. Raspberry Pi) still 
   ship with Python 3.6, this change allows ``takproto`` to run on those systems.
4. Added ``xmlDetails`` detection for supporting undefined Protobuf elements in XML.
5. > 90% test coverage with **new** Unit Tests.
6. PEP-8 & Black style, linting, documentation & formatting of code.

As much as possible @db-SPL's licensing terms were honored in this fork.
