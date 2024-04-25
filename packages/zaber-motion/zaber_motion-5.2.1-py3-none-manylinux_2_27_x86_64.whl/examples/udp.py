import socket
import threading
import time

from zaber_motion import Library, LogOutputMode
from zaber_motion.ascii import Connection, Transport

Library.set_log_output(LogOutputMode.STDOUT)

HOST = "localhost"
PORT = 5000
DEVICE_ADDRESS = 1

transport = Transport.open()
connection = Connection.open_custom(transport)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def loop_read():
  try:
    while True:
      message = transport.read()
      data = str.encode(message)
      udp_socket.send(data)
  except Exception as err:
    transport.close_with_error(str(err))

def loop_write():
  try:
    while True:
      data, addr = udp_socket.recvfrom(1024)
      message = data.decode()
      transport.write(message)
  except Exception as err:
    transport.close_with_error(str(err))

udp_socket.connect((HOST, PORT))
with udp_socket:
  thread_read = threading.Thread(target=loop_read, daemon=True)
  thread_read.start()
  thread_write = threading.Thread(target=loop_write, daemon=True)
  thread_write.start()

  while True:
    reply = connection.generic_command("tools echo Hello", DEVICE_ADDRESS)
    print(reply.data)
    time.sleep(1)
