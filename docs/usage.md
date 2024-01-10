
The TAKProto Python module exports two functions:

1. `xml2proto()`: Convert CoT XML to TAK Protocol - Version 1 Protobuf.
2. `parse_proto()`: Parse a TAK Protocol - Version 1 Protobuf into a Python object.


# xml2proto()

Given a `bytes` CoT XML message (or the path to an file containing a CoT XML message), `xml2proto()` returns a `bytearray` containing a TAK Protocol - Version 1 Protobuf.

## UDP Multicast (Mesh SA)

```py
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
```

By default, `xml2proto()` returns data as TAK Protocol - Version 1 Protobuf in Mesh SA format (UDP Multicast): 

```py
bytearray(b'\xbf\x01\xbf\x12\xff\x01\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xa2\xc7\xb8\x82.8\xa0\xa2\xc7\xb8\x82.@\x98\xf5\xc8\xb8\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\x82\x01\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00')
```

# TCP Unicast (TAK Server)

Calling `xml2proto()` with the `takproto.TAKProtoVer.STREAM` ENUM parameter returns data as TAK Protocol - Version 1 Protobuf in Stream format (TCP Unicast):

```py
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

buf = takproto.xml2proto(cot, takproto.TAKProtoVer.STREAM)
print(buf)
```

Would return the CoT XML encoded as TAK Protocol - Version 1 Protobuf (Stream TCP Unicast format for TAK Server connections):

```py
bytearray(b'\xbf\x9f\x02\x12\xff\x01\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xa2\xc7\xb8\x82.8\xa0\xa2\xc7\xb8\x82.@\x98\xf5\xc8\xb8\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\x82\x01\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00')
```

# parse_proto()

Given a `bytearray` TAK Protocol - Version 1 Protobuf, `parse_proto()` returns an instance of the Protobuf class. You can then access the contents as an object:

```py
import takproto

pb = bytearray(b'\xbf\x01\xbf\x12\xff\x01\n\x0ba-f-G-E-V-C*$aa0b0312-b5cd-4c2c-bbbc-9c4c702162610\xa0\xa2\xc7\xb8\x82.8\xa0\xa2\xc7\xb8\x82.@\x98\xf5\xc8\xb8\x82.J\x03h-eQ3\x98T\xa7b\xfdE@Y}*~\xbe\xf3\x84P\xc0aW\\\x1c\x95\x9b\xc4:@i\x00\x00\x00\xe0\xcf\x12cAq\x00\x00\x00\xe0\xcf\x12cAz\x82\x01\x12$\n\x15192.168.1.10:4242:tcp\x12\x0bEliopoli HQ\x1a\x0c\n\x06Yellow\x12\x02HQ*\x02\x08d2F\n\x11LENOVO 20QV0007US\x12\nWinTAK-CIV\x1a\x19Microsoft Windows 10 Home"\n1.10.0.137:\x00')

cot = parse_proto(pb)
```

This method of calling `parse_proto` would return an object containing the data from the Protobuf. 

If you were to `print(cot)`, you would see:

```json
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
```

Object attributes can be accessed by calling them in a Pythonic manner:

```py
print(cot.cotEvent.detail.contact.callsign)
"Eliopoli HQ"
```