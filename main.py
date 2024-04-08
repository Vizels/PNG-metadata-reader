HEADER_START = 0x00

with open("image.png", "rb") as image:
    file = image.read()
    f = bytearray(file)
    print(f[0:10])

    f[0] = 0xAA
    print(f[0:10])
    
#   b = bytearray(f)
#   print b[0]


