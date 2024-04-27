class Chunk:
    def __init__(self, name, size, data, crc):
        self.name = name
        self.size = size
        self.data = data
        self.crc = crc

    def __str__(self):
        return f"Chunk: {self.name} Size: {self.size} CRC: {int.from_bytes(self.crc)}"

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


class PLTE(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.palette = [(int(data[i:i+3][0]), int(data[i:i+3][1]), int(data[i:i+3][2])) for i in range(0, len(data), 3)]

    def __str__(self):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 10))
        colors = self.palette
        num_cols = int(len(colors) ** 0.5) + 1
        num_rows = int(len(colors) / num_cols) + 1
        for i, color in enumerate(colors):
            col = i % num_cols
            row = i // num_cols
            rect = plt.Rectangle((col, row), 1, 1, color=[x/255 for x in color])
            ax.add_patch(rect)
            # Determine contrast color based on background
            contrast_color = 'white' if sum(color) / 3 < 128 else 'black'
            ax.text(col + 0.5, row + 0.5, f"{color}", ha='center', va='center', color=contrast_color)
        ax.set_xlim(0, num_cols)
        ax.set_ylim(0, num_rows)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.title("Palette colors")
        plt.show()
        return f"Palette: {self.palette}"

    def __repr__(self):
        return self.__str__()


class sRGB(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.rendering_intent = data[0]

    def __str__(self):
        return f"Rendering Intent: {self.rendering_intent}"

    def __repr__(self):
        return self.__str__()
