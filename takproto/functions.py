#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# constants.py from https://github.com/snstac/takproto
#
# Copyright Sensors & Signals LLC https://www.snstac.com
# Copyright 2020 Delta Bravo-15 <deltabravo15ga@gmail.com>
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

"""TAKProto Functions for manipulating TAK Protocol Version 1 messages."""

import re
import xml.etree.ElementTree as ET

from datetime import datetime
from io import BytesIO
from typing import Optional, Union

import delimited_protobuf as dpb

from takproto.constants import (
    ISO_8601_UTC,
    W3C_XML_DATETIME,
    DEFAULT_MESH_HEADER,
    DEFAULT_PROTO_HEADER,
    DEFAULT_XML_HEADER,
    TAKProtoVer,
)
from takproto.proto import TakMessage


def parse_proto(msg: bytearray) -> Optional[TakMessage]:
    """Parse TAK Protocol Version 1 Mesh & Stream message."""
    parsed = None
    if msg[:3] == DEFAULT_MESH_HEADER:
        parsed = parse_mesh(msg)
    elif msg[0] in DEFAULT_PROTO_HEADER:
        parsed = parse_stream(msg)
    elif msg[:5] == DEFAULT_XML_HEADER:
        parsed = xml2message(msg)
    return parsed


def parse_mesh(msg):
    """Parse TAK Protocol Version 1 Mesh message."""
    msg = msg[3:]
    protobuf = TakMessage()
    protobuf.ParseFromString(bytes(msg))
    return protobuf


def parse_stream(msg) -> TakMessage:
    """Parse TAK Protocol Version 1 Stream message."""
    bio = BytesIO(msg[1:])
    msg = dpb.read(bio, TakMessage)
    return msg


def format_time(time: str) -> int:
    """Format timestamp as microseconds."""
    try:
        s_time = datetime.strptime(time + "+0000", ISO_8601_UTC + "%z")
    except ValueError:
        s_time = datetime.strptime(time + "+0000", W3C_XML_DATETIME + "%z")
    return int(s_time.timestamp() * 1000)


def xml2message(
    xml: bytearray,
) -> (
    TakMessage
):  # NOQA pylint: disable=too-many-locals,too-many-branches,too-many-statements
    """Convert plain XML CoT to Protobuf."""
    event = ET.fromstring(xml)
    tak_message = TakMessage()
    tak_control = tak_message.takControl
    new_event = tak_message.cotEvent

    # If this is a GeoChat message, extract the sender's UID from the event UID and
    # place it in takControl.contactUid
    uid = event.get("uid")
    if uid and "GeoChat." in uid:
        tak_control.contactUid = uid.split(".")[1]

    base_attribs = ["type", "access", "qos", "opex", "uid", "how"]
    for attrib in base_attribs:
        val = event.get(attrib)
        if val:
            setattr(new_event, attrib, val)

    # TAK protobuf times are expressed as miliseconds since 1970-01-01 00:00:00 UTC
    # Convert time, start, and stale, from ISO time format to miliseconds since epoch
    time_attribs = ["time", "start", "stale"]
    for attrib in time_attribs:
        val = event.get(attrib)
        if val:
            if attrib == "time":
                attrib = "send"
            setattr(new_event, f"{attrib}Time", format_time(val))

    # If the event element includes a point child, write the attributes
    point = event.find("point")
    if point is not None:
        attribs = ["lat", "lon", "hae", "ce", "le"]
        for attrib in attribs:
            val = point.get(attrib)
            if val:
                setattr(new_event, attrib, float(val))

    detail = event.find("detail")
    if detail is not None:
        # If the XML includes a <detail> element, create new_event.detail
        new_detail = new_event.detail

        # The new_event.detail field of a TAK protobuf is structured differently
        # from CoT XML. new_event.detail may only contain xmlDetail, contact,
        # __group, precisionlocation, status, takv, and track. xmlDetail should
        # contain an XML string with any data that does not adhere to the other
        # strongly-typed fields. See more information about each field below.

        # If this is a GeoChat message, write the contents of <detail> in xmlDetail.
        if uid and "GeoChat." in uid:
            pattern = "<detail>(.*?)</detail>"
            target = ET.tostring(detail).decode("utf-8")
            re_search = re.search(pattern, target)
            if re_search:
                xmldetailstr = re_search.group(1)
                new_detail.xmlDetail = xmldetailstr
        else:
            # Add unknown elements to xmlDetail field.
            known_elem = [
                "contact",
                "__group",
                "precisionlocation",
                "status",
                "takv",
                "track",
            ]
            for elem in detail.iterfind("*"):
                if elem.tag not in known_elem:
                    new_detail.xmlDetail += ET.tostring(elem).strip().decode()

        contact = detail.find("contact")
        if contact is not None:
            attribs = ["endpoint", "callsign"]
            for attrib in attribs:
                attrib_val = contact.get(attrib)
                if attrib_val:
                    setattr(new_detail.contact, attrib, attrib_val)

        group = detail.find("__group")  # pylint: disable=protected-access
        if group is not None:
            attribs = ["name", "role"]
            for attrib in attribs:
                attrib_val = group.get(attrib)
                if attrib_val:
                    setattr(new_detail.group, attrib, attrib_val)

        prec_loc = detail.find("precisionlocation")
        if prec_loc is not None:
            attribs = ["geopointsrc", "altsrc"]
            for attrib in attribs:
                attrib_val = prec_loc.get(attrib)
                if attrib_val:
                    setattr(new_detail.precisionLocation, attrib, attrib_val)

        status = detail.find("status")
        if status is not None:
            battery = status.get("battery")
            if battery:
                new_detail.status.battery = int(battery)

        takv = detail.find("takv")
        if takv is not None:
            attribs = ["device", "platform", "os", "version"]
            for attrib in attribs:
                attrib_val = takv.get(attrib)
                if attrib_val:
                    setattr(new_detail.takv, attrib, attrib_val)

        # The fields in track are double-precision floating-point numbers.
        # We can use Python's native float, since that is actually 64-bit
        # floating-point.
        track = detail.find("track")
        if track is not None:
            attribs = ["speed", "course"]
            for attrib in attribs:
                attrib_val = track.get(attrib)
                if attrib_val:
                    setattr(new_detail.track, attrib, float(attrib_val))

    return tak_message


def xml2proto(xml: str, protover: Optional[TAKProtoVer] = None):
    """Convert TAK XML COT to TAK Protobuf COT."""
    tak_message = xml2message(xml)
    output = msg2proto(tak_message, protover)
    return output


def msg2proto(msg, protover: Optional[TAKProtoVer] = None) -> bytearray:
    """Convert a TakMessage into a TAK Protocol Version 1 protobuf."""
    protover = protover or TAKProtoVer.MESH

    output_ba = bytearray()
    header_ba = bytearray()
    proto_ba = bytearray()

    if protover == TAKProtoVer.MESH:
        header_ba = DEFAULT_MESH_HEADER
        proto_ba = bytearray(msg.SerializeToString())
    elif protover == TAKProtoVer.STREAM:
        header_ba = DEFAULT_PROTO_HEADER
        output_io = BytesIO()
        dpb.write(output_io, msg)
        proto_ba = bytearray(output_io.getvalue())
    else:
        raise ValueError(f"Unsupported TAKProtoVer: {protover}")

    output_ba = header_ba + proto_ba
    return output_ba
