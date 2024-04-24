import chunks

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
                chunk = chunks.IHDR(name, size, chunk_data, crc)
            elif name == "tEXt":
                chunk = chunks.tEXt(name, size, chunk_data, crc)
            else:
                chunk = chunks.Chunk(name, size, chunk_data, crc)
            
            self.chunks.append(chunk)
            i += size + 12
        
        prev = ""
        for chunk in self.chunks:
            if prev != chunk.name:
                prev = chunk.name
                print(prev)
                print("======================")
            print(chunk)
