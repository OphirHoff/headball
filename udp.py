import socket
UDP_DEBUG = False

def __log(prefix, data, addr, max_to_print=100):
    if not UDP_DEBUG:
        return
    data_to_log = data[:max_to_print]
    if type(data_to_log) == bytes:
        try:
            data_to_log = data_to_log.decode()
        except (UnicodeDecodeError, AttributeError):
            pass
    print(f"\n{prefix}[{addr}]({len(data)})>>>{data_to_log}")

def send_msg(sock, data, addr):
    if len(data) == 0:
        return
    if type(data) != bytes:
        data = data.encode()
    try:
        sock.sendto(data, addr)
        __log("Sent", data, addr)
    except Exception as err:
        pass

def recv_msg(sock, size=1024):
    try:
        data, addr = sock.recvfrom(size)
        __log("Receive", data, addr)
        return data, addr
    except socket.timeout:
        return False, False
    except Exception as e:
        return False, False