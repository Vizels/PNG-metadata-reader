HEADER_START = 0
HEADER_END = 8

with open("image.png", "rb") as image:
    file = image.read()
    data = bytearray(file)
    print(data[HEADER_START:HEADER_END])

    data[0] = 0xAA
    print(data[HEADER_START:HEADER_END])


