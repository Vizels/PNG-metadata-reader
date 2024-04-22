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
                chunk = Chunk(name, size, chunk_data, crc)
                self.chunks.append(chunk)
                i += size + 12
            
            print(self.chunks)
            print(self.chunks[1].data)

test = PNG("image.png")
