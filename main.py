HEADER_START = 0x00

with open("image.png", "rb") as image:
    file = image.read()
    data = bytearray(file)
    print(data[0:10])

    data[0] = 0xAA
    print(data[0:10])


