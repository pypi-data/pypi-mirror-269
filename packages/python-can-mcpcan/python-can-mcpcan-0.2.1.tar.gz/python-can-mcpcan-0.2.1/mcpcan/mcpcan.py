"""
To Support the MCP-Can analyzer interface. The device will appear
as a serial port, for example "/dev/ttyUSB0" on Linux machines
or "COM1" on Windows.

"""

import logging
import io
import utils
from time import time
from typing import Optional

import can
from can import BusABC, Message, CanProtocol

logger = logging.getLogger(__name__)

try:
    import serial
    import serial.tools.list_ports
    from serial.tools.list_ports_common import ListPortInfo
except ImportError:
    logger.warning(
        "You won't be able to use the mcpcan backend without "
        "the serial module installed!"
    )
    serial = None


class MCPcanBus(BusABC):
    """
    Enable basic can communication over d10 mcp2518 can interface.
    """

    BITRATE = {
        5000: 1,
        10000: 2,
        20000: 3,
        31250: 4,
        33000: 5,
        40000: 6,
        50000: 7,
        80000: 8,
        100000: 9,
        125000: 10,
        200000: 11,
        250000: 12,
        500000: 13,
        1000000: 14,
    }

    FDBITRATE = {
        67233864: 0,
        33804432: 1,
        50581648: 2,
        67358864: 3,
        100913296: 4,
        134467728: 5,
        201576592: 6,
        268685456: 7,
        34054432: 8,
        67608864: 9,
        101163296: 10,
        134717728: 11,
        168272160: 12,
        218603808: 13,
        268935456: 14,
        336044320: 15,
        68108864: 16,
        135217728: 17,
        # CAN20
        5000: 18,  # 1
        10000: 19,
        20000: 20,
        25000: 21,
        31250: 22,
        33000: 23,
        40000: 24,
        50000: 25,
        80000: 26,
        83300: 27,
        95000: 28,
        100000: 29,
        125000: 30,
        200000: 31,
        250000: 32,
        500000: 33,  # 16
        666000: 34,
        800000: 35,
        1000000: 36,
    }

    def __init__(
        self,
        channel: str,
        baudrate: int = 250000,
        timeout: float = 0.1,
        bitrate: int = 500000,
        fd: bool = False,
        data_bitrate: Optional[int] = None,
        can_filters: Optional[can.typechecking.CanFilters] = None,
        *args,
        **kwargs,
    ):
        """
        :param str channel:
            The serial device to open. For example "/dev/ttyS1" or
            "/dev/ttyUSB0" on Linux or "COM1" on Windows systems.

        :param baudrate:
            The default (250000) matches required baudrate

        :param float timeout:
            Timeout for the serial device in seconds (default 0.1).

        :param bitrate
            CAN bus arbitration bitrate, selected from available list.

        :param fd:
            If CAN-FD frames should be supported.

        :param data_bitrate:
            Which bitrate to use for data bitrate in CAN FD.

        :param can_filters:
            An iterable of dictionaries each containing a "can_id",
            a "can_mask", and an optional "extended" key.

            #>>> [{"can_id": 0x11, "can_mask": 0x21, "extended": False}]

            A filter matches, when
            ``<received_can_id> & can_mask == can_id & can_mask``.
            If ``extended`` is set as well, it only matches messages where
            ``<received_is_extended> == extended``. Else it matches every
            messages based only on the arbitration ID and mask.

            Only 2 hardware filters for MCP2515 and 32 for MCP2518FD.
            If filter count is more than the above it will default to software filter.

        :raises can.CanInitializationError: If the given parameters are invalid.
        :raises can.CanInterfaceNotImplementedError: If the serial module is not installed.
        """

        if serial is None:
            raise can.CanInterfaceNotImplementedError(
                "the serial module is not installed"
            )

        if not channel:
            raise can.CanInitializationError("Must specify a serial port.")

        self.channel_info = "Serial interface: " + channel
        self._can_protocol = CanProtocol.CAN_FD if fd else CanProtocol.CAN_20
        self.is_fd = fd
        self.mcp18fd = False
        self.flag = True
        self.fw_ver = 0
        self.is_connected = False  # v2.1
        tries = 3  # set number of retries if serial is spotty
        ctype = ""

        # helper:
        ports: list[ListPortInfo] = serial.tools.list_ports.comports()
        for port in ports:
            if channel in port[0] and "SER=MFD" in port[2]:
                self.mcp18fd = True
        for n in range(tries):
            try:
                self.ser = serial.serial_for_url(
                    channel, baudrate=baudrate, timeout=timeout, rtscts=False
                )
                ctype = self._get_device()  # get device hardware version
                if ctype == "DT2518":
                    self.is_connected = True
                    self.flush_input_buffer()
                    break
                else:
                    self.ser.close()
                    if n == (tries - 1):
                        raise can.CanInitializationError("Cannot initialized mcpcan.")
            except ValueError as error:
                raise can.CanInitializationError(
                    "Could not create the serial device"
                ) from error

        # initially set filter to false
        self._is_filtered = False

        if data_bitrate and fd and self.mcp18fd:
            # calculate fdbitrate
            fdbitrate = (int(data_bitrate / bitrate) << 24) | bitrate
            # setup can bitrate
            if fdbitrate in MCPcanBus.FDBITRATE:
                self._set_bitrate(MCPcanBus.FDBITRATE[fdbitrate])
            else:
                raise can.CanInitializationError(
                    "Bitrate and dbitrate combination not allowed!"
                )
        else:
            self._set_bitrate(MCPcanBus.FDBITRATE[bitrate])

        super().__init__(channel=channel, can_filters=can_filters, *args, **kwargs)

    def _get_device(self):
        """
        Identify mcp device. Called only during interface creation.
        """
        # close can
        if self.serial_write_read("C") != None:
            # get mcp type
            self.flush_input_buffer()
            str_msg = "V"
            device = self.serial_write_read(str_msg).strip().decode()
            logger.debug("get device type: %s", device)
            if device == 'DT2518':
                str_msg = "v"
                self.fw_ver = int(self.serial_write_read(str_msg).strip().decode())
                logger.debug("get device fw version: %d", self.fw_ver)
                # open can
                if self.serial_write_read("O") != None:
                    return device
            else:
                self.ser.close()
                raise can.CanInitializationError("Device not supported!")

    def _set_bitrate(self, bitrate) -> None:
        """
        Set CAN interface bitrate.

        :bitrate:

            CAN bus bit rate

        """
        # close can
        if self.serial_write_read("C") != None:
            # set can bitrate
            self.flush_input_buffer()
            smsg = "S" + utils.int_to_full_byte_str(bitrate)
            if self.serial_write_read(smsg) != None:
                # open can
                if self.serial_write_read("O") != None:
                    logger.debug("set can bitrate: %X", bitrate)
                    return
        logger.error("failed setting bitrate: %X", bitrate)
        raise can.CanInitializationError("Could not set device bitrate")

    def shutdown(self):
        """
        Close the serial interface.
        """
        super().shutdown()
        logger.info(
            "send hardware reset upon shutdown and be ready for the next session"
        )
        if self.is_connected:
            self._write("H")  # hardware reset
            self.ser.close()
            self.is_connected = False

    def flush_input_buffer(self):
        self.ser.reset_input_buffer()

    def serial_write_read(self, smsg):
        try:
            self._write(smsg)
            stime = time()
            while not self.ser.in_waiting and time() - stime < 10:
                pass
            if self.ser.in_waiting:
                rmsg = self.ser.read()
                while chr(rmsg[-1]) != '\r':
                    rmsg += self.ser.read()
                return rmsg
            else:
                raise can.CanTimeoutError()
        except serial.PortNotOpenError as error:
            raise can.CanOperationError(
                "writing to or reading from a closed port"
            ) from error
        except serial.SerialTimeoutException as error:
            raise can.CanTimeoutError() from error

    def _write(self, smsg: str) -> None:
        try:
            self.ser.write((smsg + "\r").encode())
        except serial.PortNotOpenError as error:
            raise can.CanOperationError("writing to closed port") from error
        except serial.SerialTimeoutException as error:
            raise can.CanTimeoutError() from error

    def send(self, msg, timeout=None):
        """
        Send a message over the serial device.

        :param can.Message msg:
            Message to send.

        :param timeout:
            This parameter will be ignored. The timeout value of the channel is
            used instead.
        """

        if not self.is_fd and msg.dlc > 8:
            self.ser.close()
            raise can.CanOperationError(
                "CAN2.0 does not support message dlc is greater than 8 bytes"
            )

        # prepare message
        if msg.is_remote_frame:
            if msg.is_extended_id:
                smsg = "R"
            else:
                smsg = "r"
        else:
            if msg.is_extended_id:
                smsg = "T"
            else:
                smsg = "t"
        # apppend msg id
        if msg.is_extended_id:
            smsg += utils.int_to_full_byte_str(
                utils.high_byte(utils.high_word(msg.arbitration_id))
            )
            smsg += utils.int_to_full_byte_str(
                utils.low_byte(utils.high_word(msg.arbitration_id))
            )
            smsg += utils.int_to_full_byte_str(
                utils.high_byte(utils.low_word(msg.arbitration_id))
            )
            smsg += utils.int_to_full_byte_str(
                utils.low_byte(utils.low_word(msg.arbitration_id))
            )
        else:
            smsg += utils.int_to_half_byte_str(
                utils.high_byte(utils.low_word(msg.arbitration_id))
            )
            smsg += utils.int_to_full_byte_str(
                utils.low_byte(utils.low_word(msg.arbitration_id))
            )
        # integrate fdf to dlc and append msg len (dlc)
        if msg.is_fd and self.fw_ver > 1:
            fd_dlc = msg.dlc | 0x80
        else:
            fd_dlc = msg.dlc
        smsg += utils.int_to_full_byte_str(fd_dlc)
        if not msg.is_remote_frame:
            # append msg data
            for i in range(msg.dlc):
                smsg += utils.int_to_full_byte_str(msg.data[i])
        # send msg to serial
        logger.debug("sending: %s", smsg)
        self._write(smsg)

    def _recv_internal(self, timeout):
        """
        Read a message from the serial device.

        :param timeout:

            .. warning::
                This parameter will be ignored. The timeout value of the
                channel is used.

        :returns:
            Received message and filter status
            - self._is_filtered is True if filtering has taken place in hardware.

        :rtype:
            can.Message, bool
        """
        try:
            # ser.read can return an empty string
            # or raise a SerialException
            if self.ser.in_waiting:
                rmsg = self.ser.read()
                if chr(rmsg[0]) not in ['t', 'T', 'r', 'R']:
                    return None, True
                while chr(rmsg[-1]) != '\r':
                    rmsg += self.ser.read()
            else:
                return None, True
            rmsg = rmsg.decode()
            if rmsg[0] in ['t', 'T']:
                if not utils.validate_rmsg(rmsg):
                    return None, True
        except serial.PortNotOpenError as error:
            raise can.CanOperationError("reading from closed port") from error
        except serial.SerialException:
            return None, True
        if len(rmsg) == 0:
            return None, True

        match rmsg[0]:
            case "t":
                time_stamp = time()
                is_extended = False
                is_remote = False
                msg_id = utils.parse_std_id(rmsg)
                msg_len = utils.parse_full_byte(
                    rmsg[utils.OFFSET_STD_PKT_LEN], rmsg[utils.OFFSET_STD_PKT_LEN + 1]
                )
                msg_data = []
                for i in range(msg_len):
                    msg_data.append(
                        utils.parse_full_byte(
                            rmsg[utils.OFFSET_STD_PKT_DATA + i * 2],
                            rmsg[utils.OFFSET_STD_PKT_DATA + i * 2 + 1],
                        )
                    )
            case "T":
                time_stamp = time()
                is_extended = True
                is_remote = False
                msg_id = utils.parse_ext_id(rmsg)
                msg_len = utils.parse_full_byte(
                    rmsg[utils.OFFSET_EXT_PKT_LEN], rmsg[utils.OFFSET_EXT_PKT_LEN + 1]
                )
                msg_data = []
                for i in range(msg_len):
                    msg_data.append(
                        utils.parse_full_byte(
                            rmsg[utils.OFFSET_EXT_PKT_DATA + i * 2],
                            rmsg[utils.OFFSET_EXT_PKT_DATA + i * 2 + 1],
                        )
                    )
            case "r":
                time_stamp = time()
                is_extended = False
                is_remote = True
                msg_id = utils.parse_std_id(rmsg)
                msg_len = utils.parse_full_byte(
                    rmsg[utils.OFFSET_STD_PKT_LEN], rmsg[utils.OFFSET_STD_PKT_LEN + 1]
                )
                msg_data = []
            case "R":
                time_stamp = time()
                is_extended = True
                is_remote = True
                msg_id = utils.parse_ext_id(rmsg)
                msg_len = utils.parse_full_byte(
                    rmsg[utils.OFFSET_EXT_PKT_LEN], rmsg[utils.OFFSET_EXT_PKT_LEN + 1]
                )
                msg_data = []
            case _:
                self.flush_input_buffer()
                # self.flag = True
                return None, self._is_filtered
        # frame the msg
        msg = Message(
            timestamp=time_stamp,
            arbitration_id=msg_id,
            is_extended_id=is_extended,
            is_remote_frame=is_remote,
            dlc=msg_len,
            data=msg_data,
        )
        # self.flag = True
        logger.debug("recv message: %s", str(msg))
        return msg, self._is_filtered

    def _apply_filters(self, filters) -> None:
        """
        Apply filtering to all messages received by this Bus.

        All messages that match at least one filter are returned.
        If `filters` is `None` or a zero length sequence, all
        messages are matched.

        Calling without passing any filters will reset the applied
        filters to `None`.

        :param filters:
            A iterable of dictionaries each containing a "can_id",
            a "can_mask", and an optional "extended" key.

            >>> [{"can_id": 0x11, "can_mask": 0x21, "extended": False}]

            A filter matches, when
            ``<received_can_id> & can_mask == can_id & can_mask``.
            If ``extended`` is set as well, it only matches messages where
            ``<received_is_extended> == extended``. Else it matches every
            messages based only on the arbitration ID and mask.
        """
        if filters is None:
            return

        # Only up to two filters is allowed for 2515 and 32 for 2518fd
        if self.mcp18fd and len(filters) < 33:
            self._set_filter_2518fd(filters)
        else:
            logger.warning("Only up to 32 filters for 2518fd is allowed.")
            # fallback to software filtering:
            self._is_filtered = False

    def _set_filter_2518fd(self, filters):
        # set data
        for i, filt in enumerate(filters):
            smsg = "W"
            smsg += utils.int_to_full_byte_str(i)
            if "extended" in filt:
                smsg += "1"
            else:
                smsg += "0"
            smsg += utils.int_to_full_byte_str(
                utils.high_byte(utils.high_word(filt["can_id"]))
            )
            smsg += utils.int_to_full_byte_str(
                utils.low_byte(utils.high_word(filt["can_id"]))
            )
            smsg += utils.int_to_full_byte_str(
                utils.high_byte(utils.low_word(filt["can_id"]))
            )
            smsg += utils.int_to_full_byte_str(
                utils.low_byte(utils.low_word(filt["can_id"]))
            )
            smsg += utils.int_to_full_byte_str(
                utils.high_byte(utils.high_word(filt["can_mask"]))
            )
            smsg += utils.int_to_full_byte_str(
                utils.low_byte(utils.high_word(filt["can_mask"]))
            )
            smsg += utils.int_to_full_byte_str(
                utils.high_byte(utils.low_word(filt["can_mask"]))
            )
            smsg += utils.int_to_full_byte_str(
                utils.low_byte(utils.low_word(filt["can_mask"]))
            )
            logger.debug("write filtermask%d: %s", i, smsg)
            # send to device
            self._write(smsg)
        self._is_filtered = True

    def fileno(self):
        try:
            return self.ser.fileno()
        except io.UnsupportedOperation as exception:
            logger.debug(
                "fileno is not implemented using current CAN bus: %s", str(exception)
            )
            return -1
