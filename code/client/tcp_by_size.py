import socket
import struct
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import socket

from loguru import logger

SIZE_HEADER_FORMAT = "000000000"  # n digits for data size + one delimiter
size_header_size = len(SIZE_HEADER_FORMAT)
TCP_DEBUG = True


def recv_by_size(sock, return_type="string"):
    str_size = b""
    data_len = 0
    while len(str_size) < size_header_size:
        _d = sock.recv(size_header_size - len(str_size))
        if len(_d) == 0:
            str_size = b""
            break
        str_size += _d
    data = b""
    str_size = str_size.decode()
    if str_size != "":
        data_len = int(str_size[:size_header_size])
        while len(data) < data_len:
            _d = sock.recv(data_len - len(data))
            if len(_d) == 0:
                data = b""
                break
            data += _d

    if TCP_DEBUG and len(str_size) > 0:
        data_to_print = data[:150]
        if type(data_to_print) == bytes:
            try:
                data_to_print = data_to_print.decode()
            except (UnicodeDecodeError, AttributeError):
                pass
        logger.debug(f"\nReceive({str_size})>>>{data_to_print}")

    if data_len != len(data):
        data = b""  # Partial data is like no data !
    if return_type == "string":
        return data.decode()
    return data


def send_with_size(sock, data, public_key):
    try:
        print(type(data))
        data = data.encode()
        print(type(data))
        data = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except:
        pass
    print('ok')
    print(type(data))
    if type(data) != bytes:
        len_data = str(len(bytes(data.encode('utf-8')))).zfill(size_header_size)
    else:
        len_data = str(len(data)).zfill(size_header_size)

    len_data = len_data.encode()
    if type(data) != bytes:
        data = data.encode()
    data = len_data + data
    sock.send(data)

    if TCP_DEBUG and len(len_data) > 0:
        data = data[:100]
        if type(data) == bytes:
            try:
                data = data.decode()
            except (UnicodeDecodeError, AttributeError):
                pass
        logger.debug(f"\nSend({len_data})>>>{data}")
