class Chunk:
    def __init__(self, name, size, data, crc):
        self.name = name
        self.size = size
        self.data = data
        self.crc = crc

    def __str__(self):
        return f"Chunk: {self.name} Size: {self.size} CRC: {self.crc}"

    def __repr__(self):
        return self.__str__()

class IHDR(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.width = int.from_bytes(data[0:4], byteorder="big")
        self.height = int.from_bytes(data[4:8], byteorder="big")
        self.bit_depth = data[8]
        self.color_type = data[9]
        self.compression_method = data[10]
        self.filter_method = data[11]
        self.interlace_method = data[12]

    def __str__(self):
        return f"IHDR Chunk\nWidth: {self.width}\nHeight: {self.height}\nBit Depth: {self.bit_depth}\nColor Type: {self.color_type}\nCompression Method: {self.compression_method}\nFilter Method: {self.filter_method}\nInterlace Method: {self.interlace_method}"

    def __repr__(self):
        return self.__str__()


class tEXt(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.keyword = data[:data.index(0)].decode("utf-8")
        self.value = data[data.index(0)+1:].decode("utf-8")

    def __str__(self):
        return f"{self.keyword} : {self.value}"

    def __repr__(self):
        return self.__str__()

class eXIf(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.keyword = data[len('exif:'):data.index(0)].decode("utf-8")
        self.value = data[data.index(0)+1:].decode("utf-8")
        
    def __str__(self):
        return f"{self.keyword} : {self.value}"

    def __repr__(self):
        return self.__str__()
