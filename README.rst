.. image:: ./docs/pytak_logo-256x264.png
    :alt: PyTAK Logo

takproto: TAK Protocol Python Module
************************************

``takproto`` is a Python module to encode & decode 'TAK Protocol Payload - Version 1' 
Protocol Buffer based Cursor on Target (CoT) messages.

From the ATAK source:

    Version 1 of the TAK Protocol Payload is a Google Protocol Buffer based
    payload.  Each Payload consists of one (and only one)
    atakmap::commoncommo::v1::TakMessage message which is serialized using
    Google protocol buffers version 3.

    Source: https://github.com/deptofdefense/AndroidTacticalAssaultKit-CIV/blob/master/commoncommo/core/impl/protobuf/protocol.txt

``takproto`` is a fork & complete re-write of @dB-SPL's 
`takprotobuf <https://github.com/dB-SPL/takprotobuf>`_.
Absolute credit goes to them for their initial implementation. 

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


Usage
=====

The `takproto` module exports two functions:


xml2proto()
-----------

Given a string which contains either a CoT message in XML or the path to an XML file 
containing a CoT message, the function ``xml2proto()`` will return a ``bytearray`` containing 
the binary protobuf::

    import takproto

    cot = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
    <event version='2.0' uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' type='a-f-G-E-V-C' time='2020-02-08T18:10:44.000Z' start='2020-02-08T18:10:44.000Z' stale='2020-02-08T18:11:11.000Z' how='h-e'>
        <point lat='43.97957317' lon='-66.07737696' hae='26.767999' ce='9999999.0' le='9999999.0' />
        <detail>
            <uid Droid='Eliopoli HQ'/>
            <contact callsign='Eliopoli HQ' endpoint='192.168.1.10:4242:tcp'/>
            <__group name='Yellow' role='HQ'/><status battery='100'/>
            <takv platform='WinTAK-CIV' device='LENOVO 20QV0007US' os='Microsoft Windows 10 Home' version='1.10.0.137'/>
            <track speed='0.00000000' course='0.00000000'/>
        </detail>
    </event>
    """

    buf = takproto.xml2proto(cot)
    print(buf)

Would return the CoT XML encoded as TAK Protocol Version 1 Mesh::
    
    bytearray(b'\xbf\x01\xbf\x12\xff\x01\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xa2\xc7\xb8\x82.8\xa0\xa2\xc7\xb8\x82.@\x98\xf5\xc8\xb8\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\x82\x01\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00')

Additionally, calling xml2proto with the `takproto.TAKProtoVer.STREAM` flag would return a stream-ready protobuf::

    buf = takproto.xml2proto(cot, takproto.TAKProtoVer.STREAM)
    print(buf)

Would return the CoT XML encoded as TAK Protocol Version 1 Stream::

    bytearray(b'\xbf\x9f\x02\x12\xff\x01\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xa2\xc7\xb8\x82.8\xa0\xa2\xc7\xb8\x82.@\x98\xf5\xc8\xb8\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\x82\x01\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00')


parse_proto()
-------------

Given a bytearray containing a version 1 protobuf, ``parse_proto()`` will return an 
instance of the protobuf class. You can then access the contents as an object::

    import takproto
   
    pb = bytearray(b'\xbf\x01\xbf\x12\xff\x01\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xa2\xc7\xb8\x82.8\xa0\xa2\xc7\xb8\x82.@\x98\xf5\xc8\xb8\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\x82\x01\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00')

    cot = parse_proto(pb)
 
This method of calling parse_proto would return an object containing the data from the 
protobuf. If you were to ``print(cot)``, you would see::

    cotEvent {
        type: "a-f-G-E-V-C"
        uid: "aa0b0312-b5cd-4c2c-bbbc-9c4c70216261"
        sendTime: 1581203444000
        startTime: 1581203444000
        staleTime: 1581203471000
        how: "h-e"
        lat: 43.97957317
        lon: -66.07737696
        hae: 26.767999
        ce: 9999999.0
        le: 9999999.0
        detail {
            contact {
            endpoint: "192.168.1.10:4242:tcp"
            callsign: "Eliopoli HQ"
            }
            group {
            name: "Yellow"
            role: "HQ"
            }
            status {
            battery: 100
            }
            takv {
            device: "LENOVO 20QV0007US"
            platform: "WinTAK-CIV"
            os: "Microsoft Windows 10 Home"
            version: "1.10.0.137"
            }
            track {
            }
        }
    }

Object attributes can be accessed by calling them in a Pythonic manner::

    print(cot.cotEvent.detail.contact.callsign)
    "Eliopoli HQ"


Additional Examples
-------------------

For additional examples using this module, see the `tests/` directory.


What's the difference between the TAK Protocol formats?
=======================================================

Originally the TAK Products spoke Cursor on Target (CoT) encoded as plain XML. Later versions 
of the TAK Products added support for sending CoT as Google Protobuf, which TPC named 'TAK Protocol Version 1'.

Out of the box, TAK Products such as ATAK and WinTAK configured for 'Mesh SA' will send 
TAK Protocol Version 1 Mesh formatted CoT. This format utizes a static payload header of 
the format `191 1 191 <payload>`.

TAK Products configured for connecting to a TAK Server will send TAK Protocol Version 1 Stream 
formatted CoT. This format utizes a dynamic payload header of the format `191 <varint payload length> <payload>`.
This header format is required for specifying the size of the payload within the TCP packet.

The `takproto` module supports encoding and decoding all 3 formats of CoT messages.

.. image:: ./docs/takproto_chart.png
    :alt: TAK Protocol chart


Source
======
Github: https://github.com/snstac/takproto


Authors
=======
* Greg Albrecht https://www.snstac.com/
* Delta Bravo-15 https://github.com/db-SPL


Copyright
=========
* Copyright Sensors & Signals LLC https://www.snstac.com
* Copyright 2020 Delta Bravo-15 <deltabravo15ga@gmail.com>


Style
=====
Python Black, otherwise Google, then PEP-8.


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
