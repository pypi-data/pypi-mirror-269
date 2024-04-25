"""
    Support functions for mcpcan module 
"""

import can.typechecking

OFFSET_PKT_ID = 1
OFFSET_STD_PKT_LEN = 4
OFFSET_STD_PKT_DATA = 6
OFFSET_EXT_PKT_LEN = 9
OFFSET_EXT_PKT_DATA = 11
OFFSET_NUM_DATA = 1
OFFSET_EXT_DATA = 3
OFFSET_FILT_DATA = 4
OFFSET_MASK_DATA = 12

def int_to_full_byte_str(num: int) -> str:
    num = min(num, 255)
    return f"{num:02X}"


def int_to_half_byte_str(num: int) -> str:
    num = min(num, 15)
    return f"{num:X}"


def bytearray_to_str(data: can.typechecking.CanData) -> str:
    if not isinstance(data, can.typechecking.CanData):
        raise (can.CanOperationError("invalid data type..."))
    x = ""
    for i in data:
        x += f"{i:02X}"
    return x

def validate_rmsg(msg: str) -> bool:
    offset = 0
    if msg[0] == 'T':
        offset = 5
    if len(msg) < (6 + offset):
        return False
    msglen = (parse_full_byte(msg[4+offset], msg[5+offset]) * 2) + (6 + offset)
    if len(msg)-1 == msglen:
        return True
    else:
        return False

def parse_nibble(X: str) -> int:
    return int(X, 16)


def parse_full_byte(H: str, L: str) -> int:
    return int(H + L, 16)


def parse_std_id(msg: str) -> int:
    can_id = 0
    for i in range(3):
        can_id += parse_nibble(msg[OFFSET_PKT_ID + i]) << 8 - i * 4
    return can_id & 0x7FF


def parse_ext_id(msg: str) -> int:
    can_id = 0
    for i in range(8):
        can_id += parse_nibble(msg[OFFSET_PKT_ID + i]) << 28 - i * 4
    return can_id & 0x1FFFFFFF


def low_byte(num: int) -> int:
    return num & 0xFF


def high_byte(num: int) -> int:
    return (num >> 8) & 0xFF


def low_word(num: int) -> int:
    return num & 0xFFFF


def high_word(num: int) -> int:
    return (num >> 16) & 0xFFFF
