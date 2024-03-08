#!/usr/bin/env python3
import serial
import sys

import random

from Crypto.Cipher import AES


if len(sys.argv) < 2:
  print("Usage: {0} [DEVICE]".format(sys.argv[0]))
  sys.exit(-1)

dev = serial.Serial(sys.argv[1], 115200)

print("started the encryption thing")

# run ten tests
for i in range(10):
  x = dev.readline()
  print("Flag 1 - Read something")
  print(x.decode()) # 
  print("Flag 2 - We've printed it")

  # generate random 128 bit key and random 128 bit data block
  key = bytes(random.getrandbits(8) for _ in range(16))
  data = bytes(random.getrandbits(8) for _ in range(16))

  print("Flag 3 - writing data")
  # send key and data to device
  a = 127
  dev.write(key)
  dev.write(data)

  print("Flag 4 - done writing data")


  x = dev.readline()
  print("Flag 5 - Read something")
  print(x.decode()) # 
  print("Flag 6 - We've printed it")

  sent_key = dev.read(16)
  sent_message = dev.read(16)
  print("Flag 7 - got data back")

  print(f"dev = ", end=" ")
  for i in range(16):
    val = hex(sent_key[i]).lstrip("0x").rstrip("L")
    print(f"{val} ", end=" ")
  print("")

  print(f"oth = ", end=" ")
  for i in range(16):
    val = hex(key[i]).lstrip("0x").rstrip("L")
    print(f"{val} ", end=" ")
  print("\n\n")

  print(f"dev = ", end=" ")
  for i in range(16):
    val = hex(sent_message[i]).lstrip("0x").rstrip("L")
    print(f"{val} ", end=" ")
  print("")

  print(f"oth = ", end=" ")
  for i in range(16):
    val = hex(data[i]).lstrip("0x").rstrip("L")
    print(f"{val} ", end=" ")
  print("\n")
  

  print("Flag 8 - done printing that now")
    
  print("Flag 9 - reading data")

  # read cipher text from device
  ciphertext_dev = dev.read(16)
  print("Flag 10 - done reading data")

  # generate reference cipher block
  cipher = AES.new(key, AES.MODE_ECB)
  ciphertext_rev = cipher.encrypt(data)

  print(f"dev = ", end=" ")
  for i in range(16):
    val = hex(ciphertext_dev[i]).lstrip("0x").rstrip("L")
    print(f"{val} ", end=" ")
  print("")

  print(f"oth = ", end=" ")
  for i in range(16):
    val = hex(ciphertext_rev[i]).lstrip("0x").rstrip("L")
    print(f"{val} ", end=" ")
  print("\n")

  # compare reference and response block byte-by-byte
  """for i in range(16):
    print(f"\n----\nround {i}")
    print(f"dev = {ciphertext_dev[i]}")
    print(f"oth = {ciphertext_rev[i]}")
    if ciphertext_dev[i] != ciphertext_rev[i]:
      pass"""
      #print("\n----\nround 1")
      #print(f"dev = {ciphertext_dev[i]}")
      #print(f"oth = {ciphertext_rev[i]}")
      #print("Error in encryption!\n")
  
  sys.exit(-1)
 
