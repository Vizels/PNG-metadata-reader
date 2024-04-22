class Chunk:
    def __init__(self, name, size, data, crc):
        self.name = name
        self.size = size
        self.data = data
        self.crc = crc

    def __str__(self):
        return f"Chunk: {self.name} Size: {self.size} CRC: {self.crc}\n"

    def __repr__(self):
        return f"Chunk: {self.name} Size: {self.size} CRC: {self.crc}\n"
    
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
        return f"IHDR Chunk\nWidth: {self.width}\nHeight: {self.height}\nBit Depth: {self.bit_depth}\nColor Type: {self.color_type}\nCompression Method: {self.compression_method}\nFilter Method: {self.filter_method}\nInterlace Method: {self.interlace_method}\n"

    def __repr__(self):
        return f"IHDR Chunk\nWidth: {self.width}\nHeight: {self.height}\nBit Depth: {self.bit_depth}\nColor Type: {self.color_type}\nCompression Method: {self.compression_method}\nFilter Method: {self.filter_method}\nInterlace Method: {self.interlace_method}\n"

class PNG:
    def __init__(self, file):
        self.file = file
        self.chunks = []
        self.HEADER_START = 0
        self.HEADER_END = 8
        self.parse()

    def parse(self):
        with open(self.file, "rb") as image:
            data = bytearray(image.read())
            header = data[self.HEADER_START:self.HEADER_END]
            print(header)

            i = self.HEADER_END

            while i < len(data):
                size = int.from_bytes(data[i:i+4], byteorder="big")
                name = data[i+4:i+8].decode("utf-8")
                chunk_data = data[i+8:i+8+size]
                crc = data[i+8+size:i+12+size]
                
                if name == "IHDR":
                    chunk = IHDR(name, size, chunk_data, crc)
                else:
                    chunk = Chunk(name, size, chunk_data, crc)
                
                self.chunks.append(chunk)
                i += size + 12
            
            print(self.chunks)
            print(self.chunks[0])

test = PNG("image.png")
