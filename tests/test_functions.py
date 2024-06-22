#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Sensors & Signals LLC
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
#
# Author:: Greg Albrecht <gba@snstac.com>
# Copyright:: Copyright 2023 Sensors & Signals LLC
# License:: Apache License, Version 2.0
#

"""TAKProto Module Tests."""

from datetime import datetime, timezone
import unittest

import takproto


class TestFunctions(unittest.TestCase):

    def test_format_timestamp1(self):
        """Test formatting timestamp to and from Protobuf format 1."""
        t_time = "2020-02-08T18:10:44.000000Z"
        t_ts = 1581185444000
        ts = takproto.format_time(t_time)
        self.assertEqual(ts, t_ts)

    def test_format_timestamp2(self):
        """Test formatting timestamp to and from Protobuf format 2."""
        t_time = "2020-02-08T18:10:44.000000Z"
        t_ts = 1581185444000
        t_ts2 = t_ts / 1000
        time2 = datetime.fromtimestamp(t_ts2, timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        self.assertEqual(time2, t_time)

    def test_format_timestamp_without_subseconds1(self):
        """Test formatting timestamp to and from Protobuf format 1."""
        t_time = "2020-02-08T18:10:44Z"
        t_ts = 1581185444000
        ts = takproto.format_time(t_time)
        self.assertEqual(ts, t_ts)

    def test_format_timestamp_without_subseconds2(self):
        """Test formatting timestamp to and from Protobuf format 2."""
        t_time = "2020-02-08T18:10:44Z"
        t_ts = 1581185444000
        t_ts2 = t_ts / 1000
        time2 = datetime.fromtimestamp(t_ts2, timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        self.assertEqual(time2, t_time)

    def test_xml2proto_default(self):
        """Test encoding XML string as Protobuf bytearray."""
        t_xml = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        <event version='2.0' uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' type='a-f-G-E-V-C' time='2020-02-08T18:10:44.000Z' start='2020-02-08T18:10:44.000Z' stale='2020-02-08T18:11:11.000Z' how='h-e'><point lat='43.97957317' lon='-66.07737696' hae='26.767999' ce='9999999.0' le='9999999.0' /><detail><uid Droid='Eliopoli HQ'/><contact callsign='Eliopoli HQ' endpoint='192.168.1.10:4242:tcp'/><__group name='Yellow' role='HQ'/><status battery='100'/><takv platform='WinTAK-CIV' device='LENOVO 20QV0007US' os='Microsoft Windows 10 Home' version='1.10.0.137'/><track speed='0.00000000' course='0.00000000'/><another test="1"/></detail></event>
        """

        t_ba = bytearray(
            b'\xbf\x01\xbf\x12\xb0\x02\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xd1\xfc\xaf\x82.8\xa0\xd1\xfc\xaf\x82.@\x98\xa4\xfe\xaf\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\xb3\x01\n/<uid Droid="Eliopoli HQ" /><another test="1" />\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00'
        )

        buf = takproto.xml2proto(t_xml)

        print("Generated: ")
        print(takproto.parse_proto(bytes(buf)))
        print(buf)

        print("Expected: ")
        print(takproto.parse_proto(bytes(t_ba)))
        print(t_ba)

        self.assertEqual(bytes(buf), bytes(t_ba))

    def test_xml2proto_mesh(self):
        """Test encoding CoT XML string as TAK Protocol Version 1 Mesh Protobuf."""
        t_xml = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        <event version='2.0' uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' type='a-f-G-E-V-C' time='2020-02-08T18:10:44.000Z' start='2020-02-08T18:10:44.000Z' stale='2020-02-08T18:11:11.000Z' how='h-e'><point lat='43.97957317' lon='-66.07737696' hae='26.767999' ce='9999999.0' le='9999999.0' /><detail><uid Droid='Eliopoli HQ'/><contact callsign='Eliopoli HQ' endpoint='192.168.1.10:4242:tcp'/><__group name='Yellow' role='HQ'/><status battery='100'/><takv platform='WinTAK-CIV' device='LENOVO 20QV0007US' os='Microsoft Windows 10 Home' version='1.10.0.137'/><track speed='0.00000000' course='0.00000000'/><another test="1"/></detail></event>
        """

        t_ba = bytearray(
            b'\xbf\x01\xbf\x12\xb0\x02\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xd1\xfc\xaf\x82.8\xa0\xd1\xfc\xaf\x82.@\x98\xa4\xfe\xaf\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\xb3\x01\n/<uid Droid="Eliopoli HQ" /><another test="1" />\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00'
        )

        buf = takproto.xml2proto(t_xml, takproto.TAKProtoVer.MESH)

        self.assertEqual(bytes(buf), bytes(t_ba))

    def test_parse_proto_mesh(self):
        """Test deserializing TAK Protocol Version 1 Mesh bytes to TakMessage Protobuf."""
        t_ba = bytearray(
            b'\xbf\x01\xbf\x12\xb0\x02\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xd1\xfc\xaf\x82.8\xa0\xd1\xfc\xaf\x82.@\x98\xa4\xfe\xaf\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\xb3\x01\n/<uid Droid="Eliopoli HQ" /><another test="1" />\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00'
        )

        parsed = takproto.parse_proto(t_ba)
        cot_event = parsed.cotEvent

        self.assertEqual(cot_event.type, "a-f-G-E-V-C")
        self.assertEqual(cot_event.uid, "aa0b0312-b5cd-4c2c-bbbc-9c4c70216261")
        self.assertEqual(
            cot_event.detail.xmlDetail,
            '<uid Droid="Eliopoli HQ" /><another test="1" />',
        )
        self.assertEqual(cot_event.detail.contact.callsign, "Eliopoli HQ")

    def test_xml2proto_stream(self):
        """Test encoding CoT XML string as TAK Protocol Version 1 Stream Protobuf."""
        t_xml = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        <event version='2.0' uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' type='a-f-G-E-V-C' time='2020-02-08T18:10:44.000Z' start='2020-02-08T18:10:44.000Z' stale='2020-02-08T18:11:11.000Z' how='h-e'><point lat='43.97957317' lon='-66.07737696' hae='26.767999' ce='9999999.0' le='9999999.0' /><detail><uid Droid='Eliopoli HQ'/><contact callsign='Eliopoli HQ' endpoint='192.168.1.10:4242:tcp'/><__group name='Yellow' role='HQ'/><status battery='100'/><takv platform='WinTAK-CIV' device='LENOVO 20QV0007US' os='Microsoft Windows 10 Home' version='1.10.0.137'/><track speed='0.00000000' course='0.00000000'/><another test="1"/></detail></event>
        """

        t_ba = bytearray(
            b'\xbf\xb3\x02\x12\xb0\x02\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xd1\xfc\xaf\x82.8\xa0\xd1\xfc\xaf\x82.@\x98\xa4\xfe\xaf\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\xb3\x01\n/<uid Droid="Eliopoli HQ" /><another test="1" />\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00'
        )

        buf = takproto.xml2proto(t_xml, takproto.TAKProtoVer.STREAM)

        self.assertEqual(bytes(buf), bytes(t_ba))

    def test_parse_proto_stream(self):
        """Test deserializing TAK Protocol Version 1 Stream bytes to TakMessage Protobuf."""
        t_ba = bytearray(
            b'\xbf\xb3\x02\x12\xb0\x02\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xd1\xfc\xaf\x82.8\xa0\xd1\xfc\xaf\x82.@\x98\xa4\xfe\xaf\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\xb3\x01\n/<uid Droid="Eliopoli HQ" /><another test="1" />\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00'
        )

        parsed = takproto.parse_proto(t_ba)
        cot_event = parsed.cotEvent

        self.assertEqual(cot_event.type, "a-f-G-E-V-C")
        self.assertEqual(cot_event.uid, "aa0b0312-b5cd-4c2c-bbbc-9c4c70216261")
        self.assertEqual(
            cot_event.detail.xmlDetail,
            '<uid Droid="Eliopoli HQ" /><another test="1" />',
        )
        self.assertEqual(cot_event.detail.contact.callsign, "Eliopoli HQ")

    def test_parse_proto_xml(self):
        """Test deserializing CoT XML bytes to TakMessage Protobuf."""
        t_xml = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
        <event version='2.0' uid='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' type='a-f-G-E-V-C' time='2020-02-08T18:10:44.000Z' start='2020-02-08T18:10:44.000Z' stale='2020-02-08T18:11:11.000Z' how='h-e'><point lat='43.97957317' lon='-66.07737696' hae='26.767999' ce='9999999.0' le='9999999.0' /><detail><uid Droid='Eliopoli HQ'/><contact callsign='Eliopoli HQ' endpoint='192.168.1.10:4242:tcp'/><__group name='Yellow' role='HQ'/><status battery='100'/><takv platform='WinTAK-CIV' device='LENOVO 20QV0007US' os='Microsoft Windows 10 Home' version='1.10.0.137'/><track speed='0.00000000' course='0.00000000'/><another test="1"/></detail></event>
        """

        t_ba = bytearray(t_xml, encoding="utf-8")

        parsed = takproto.parse_proto(t_ba)
        print(parsed)
        print(type(parsed))
        cot_event = parsed.cotEvent

        self.assertEqual(cot_event.type, "a-f-G-E-V-C")
        self.assertEqual(cot_event.uid, "aa0b0312-b5cd-4c2c-bbbc-9c4c70216261")
        self.assertEqual(
            cot_event.detail.xmlDetail,
            '<uid Droid="Eliopoli HQ" /><another test="1" />',
        )
        self.assertEqual(cot_event.detail.contact.callsign, "Eliopoli HQ")
