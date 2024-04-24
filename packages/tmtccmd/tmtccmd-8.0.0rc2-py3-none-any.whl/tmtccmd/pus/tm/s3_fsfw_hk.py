# -*- coding: utf-8 -*-
"""PUS Service 3 components
"""
from __future__ import annotations
from abc import abstractmethod
import struct
from deprecated.sphinx import deprecated

from spacepackets.ecss.tm import CdsShortTimestamp, PusTelemetry
from tmtccmd.tmtc.tm_base import PusTmInfoBase, PusTmBase
from .s3_hk_base import (  # noqa: F401
    Service3Base,
    ObjectIdU32,
)
from typing import Tuple, List


# TODO: Implement custom reader class, unittest it.
class Service3FsfwTm(Service3Base, PusTmBase, PusTmInfoBase):
    """This class encapsulates the format of Service 3 telemetry
    This class was written to handle Service 3 telemetry coming from the on-board software
    based on the Flight Software Framework (FSFW). A custom class can be defined, but should then
    implement Service3Base.
    """

    # Minimal packet contains SID, which consists of object ID(4) and set ID(4)
    DEFAULT_MINIMAL_PACKET_SIZE = 8
    # Minimal structure report contains SID (8), reporting status(1), validity flag (1),
    # collection interval as float (4) and number of parameters(1)
    STRUCTURE_REPORT_FIXED_HEADER_SIZE = DEFAULT_MINIMAL_PACKET_SIZE + 7

    @deprecated(version="8.0.0", reason="deprecated TM API")
    def __init__(
        self,
        subservice_id: int,
        time: CdsShortTimestamp,
        hk_data: bytearray,
        custom_hk_handling: bool = False,
        ssc: int = 0,
        apid: int = -1,
        minimum_reply_size: int = DEFAULT_MINIMAL_PACKET_SIZE,
        minimum_structure_report_header_size: int = STRUCTURE_REPORT_FIXED_HEADER_SIZE,
        packet_version: int = 0b000,
        space_time_ref: int = 0b0000,
        destination_id: int = 0,
    ):
        """Service 3 packet class representation which can be built from a raw bytearray
        :param subservice_id:
        :param time:
        :param hk_data:
        :param custom_hk_handling:  Can be used if a custom HK format is used which does not
                                    use a 8 byte structure ID (SID).
        :param minimum_reply_size:
        :param minimum_structure_report_header_size:
        """
        Service3Base.__init__(self, object_id=0, custom_hk_handling=custom_hk_handling)
        source_data = bytearray()
        source_data.extend(struct.pack("!I", self.object_id.obj_id))
        source_data.extend(struct.pack("!I", self.set_id))
        if subservice_id == 25 or subservice_id == 26:
            source_data.extend(hk_data)
        pus_tm = PusTelemetry(
            service=3,
            subservice=subservice_id,
            time_provider=time,
            seq_count=ssc,
            source_data=source_data,
            apid=apid,
            packet_version=packet_version,
            space_time_ref=space_time_ref,
            destination_id=destination_id,
        )
        PusTmBase.__init__(self, pus_tm=pus_tm)
        PusTmInfoBase.__init__(self, pus_tm=pus_tm)
        self.__init_without_base(
            instance=self,
            custom_hk_handling=custom_hk_handling,
            minimum_reply_size=minimum_reply_size,
            minimum_structure_report_header_size=minimum_structure_report_header_size,
            check_tm_data_size=False,
        )

    @staticmethod
    def __init_without_base(
        instance: Service3FsfwTm,
        custom_hk_handling: bool,
        check_tm_data_size: bool,
        minimum_reply_size: int = DEFAULT_MINIMAL_PACKET_SIZE,
        minimum_structure_report_header_size: int = STRUCTURE_REPORT_FIXED_HEADER_SIZE,
    ):
        instance.custom_hk_handling = custom_hk_handling
        if instance.custom_hk_handling:
            return
        tm_data = instance.tm_data
        if len(tm_data) < 8:
            raise ValueError(
                "Invalid Service 3 packet, is too short. Detected TM data length:"
                f" {len(tm_data)}"
            )
        instance.min_hk_reply_size = minimum_reply_size
        instance.hk_structure_report_header_size = minimum_structure_report_header_size
        instance.object_id = ObjectIdU32.from_bytes(tm_data[0:4])
        instance.set_id = struct.unpack("!I", tm_data[4:8])[0]
        if instance.subservice == 25 or instance.subservice == 26:
            if len(tm_data) > 8:
                instance._param_length = len(tm_data[8:])
        instance.set_packet_info("Housekeeping Packet")

    @classmethod
    def __empty(cls) -> Service3FsfwTm:
        return cls(
            subservice_id=0,
            time=CdsShortTimestamp.from_now(),
            hk_data=bytearray(),
        )

    @classmethod
    def unpack(
        cls,
        raw_telemetry: bytes,
        custom_hk_handling: bool,
    ) -> Service3FsfwTm:
        service_3_tm = cls.__empty()
        service_3_tm.pus_tm = PusTelemetry.unpack(
            data=raw_telemetry, time_reader=CdsShortTimestamp.empty()
        )
        service_3_tm.__init_without_base(
            instance=service_3_tm,
            custom_hk_handling=custom_hk_handling,
            check_tm_data_size=True,
        )
        return service_3_tm

    @abstractmethod
    def append_telemetry_content(self, content_list: list):
        super().append_telemetry_content(content_list=content_list)
        content_list.append(self.object_id.as_hex_string)
        content_list.append(hex(self.set_id))
        content_list.append(int(self._param_length))

    @abstractmethod
    def append_telemetry_column_headers(self, header_list: list):
        super().append_telemetry_column_headers(header_list=header_list)
        header_list.append("Object ID")
        header_list.append("Set ID")
        header_list.append("HK data size")

    def get_hk_definitions_list(self) -> Tuple[List, List]:
        tm_data = self.tm_data
        if len(tm_data) < self.hk_structure_report_header_size:
            raise ValueError(
                "Service3TM: handle_filling_definition_arrays: Invalid structure"
                f" report from {self.object_id.as_hex_string}, is shorter than"
                f" {self.hk_structure_report_header_size}"
            )
        definitions_header = [
            "Object ID",
            "Set ID",
            "Report Status",
            "Is valid",
            "Collection Interval (s)",
            "Number Of IDs",
        ]
        reporting_enabled = tm_data[8]
        set_valid = tm_data[9]
        collection_interval_seconds = struct.unpack("!f", tm_data[10:14])[0] / 1000.0
        num_params = tm_data[14]
        if len(tm_data) < self.hk_structure_report_header_size + num_params * 4:
            raise ValueError(
                "Service3TM: handle_filling_definition_arrays: Invalid structure"
                f" report from {self.object_id.as_hex_string}, is shorter than"
                f" {self.hk_structure_report_header_size + num_params * 4}"
            )

        parameters = []
        counter = 1
        for array_index in range(
            self.hk_structure_report_header_size,
            self.hk_structure_report_header_size + 4 * num_params,
            4,
        ):
            parameter = struct.unpack("!I", tm_data[array_index : array_index + 4])[0]
            definitions_header.append("Pool ID " + str(counter))
            parameters.append(str(hex(parameter)))
            counter = counter + 1
        if reporting_enabled == 1:
            status_string = "On"
        else:
            status_string = "Off"
        if set_valid:
            valid_string = "Yes"
        else:
            valid_string = "No"
        definitions_content = [
            self.object_id.as_hex_string,
            self._set_id,
            status_string,
            valid_string,
            collection_interval_seconds,
            num_params,
        ]
        definitions_content.extend(parameters)
        return definitions_header, definitions_content
