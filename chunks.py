import datetime

class Chunk:
    def __init__(self, name, size, data, crc):
        self.name = name
        self.size = size
        self.data = data
        self.crc = crc

    def __str__(self):
        return f"Chunk: {self.name} Size: {self.size} CRC: {int.from_bytes(self.crc, byteorder='big')}"

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
        return f"Width: {self.width}\nHeight: {self.height}\nBit Depth: {self.bit_depth}\nColor Type: {self.color_type}\nCompression Method: {self.compression_method}\nFilter Method: {self.filter_method}\nInterlace Method: {self.interlace_method}"

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
        return f"Number of colors: {len(self.palette)}\nPalette: {self.palette}"

    def __repr__(self):
        return self.__str__()


class sRGB(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.rendering_intent = data[0]
        self.VALUES = ["Perceptual", "Relative Colorimetric", "Saturation", "Absolute Colorimetric"]

    def __str__(self):
        return f"Rendering Intent: {self.rendering_intent} ({ self.VALUES[self.rendering_intent] if self.rendering_intent < 4 else ''})"

    def __repr__(self):
        return self.__str__()

class tRNS(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.transparency = [int(value) for value in data]

    def __str__(self):
        return f"Transparency: {self.transparency}"

    def __repr__(self):
        return self.__str__()

class gAMA(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.gamma = int.from_bytes(data, byteorder="big")/100000

    def __str__(self):
        return f"Gamma: {self.gamma}"

    def __repr__(self):
        return self.__str__()

class pHYs(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.pixels_per_unit_x = int.from_bytes(data[0:4], byteorder="big")
        self.pixels_per_unit_y = int.from_bytes(data[4:8], byteorder="big")
        self.unit_specifier = data[8]

    def __str__(self):
        ppu_X = f"Pixels per unit, X axis: {self.pixels_per_unit_x}"
        ppu_Y = f"Pixels per unit, Y axis: {self.pixels_per_unit_y}"
        unit_spec = f"Unit Specifier: {self.unit_specifier}"
        return f"{ppu_X}\n{ppu_Y}\n{unit_spec}{' (meter)' if self.unit_specifier == 1 else '( unknown)'}"

    def __repr__(self):
        return self.__str__()

class tIME(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.year = int.from_bytes(data[0:2], byteorder="big")
        self.month = int.from_bytes(data[2:3], byteorder="big")
        self.day = int.from_bytes(data[3:4], byteorder="big")
        self.hour = int.from_bytes(data[4:5], byteorder="big")
        self.minute = int.from_bytes(data[5:6], byteorder="big")
        self.second = int.from_bytes(data[6:7], byteorder="big")
        self.date = datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)

    def __str__(self):
        return f"{self.date}"

    def __repr__(self):
        return self.__str__()

class bKGD(Chunk):
    def __init__(self, name, size, data, crc):
        super().__init__(name, size, data, crc)
        self.value_label = ""
        if len(data) == 6:
            self.background = (int.from_bytes(data[0:2], byteorder="big"),
                               int.from_bytes(data[2:4], byteorder="big"),
                               int.from_bytes(data[4:6], byteorder="big"))
            self.value_label = "RGB"
        elif len(data) == 2:
            self.background = int.from_bytes(data[:], byteorder="big")
            self.value_label = "Gray"
        elif len(data) == 1:
            self.background = int.from_bytes(data[:], byteorder="big")
            self.value_label = "Palette Index"

    def __str__(self):
        if self.value_label == "RGB":
            return f"Background: {self.background} (R, G, B)"
        elif self.value_label == "Gray":
            return f"Background: {self.background} (Gray)"
        elif self.value_label == "Palette Index":
            return f"Background: {self.background} (Palette Index)"

    def __repr__(self):
        return self.__str__()
