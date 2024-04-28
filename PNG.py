import zlib
import cv2
import math
import colorsys
import numpy as np
import matplotlib.pyplot as plt
import chunks

class PNG:
    def __init__(self, file):
        self.file = file
        self.chunks = []
        self.HEADER_START = 0
        self.HEADER_END = 8
        self.parse()

    def printData(self):
        prev = ""
        for chunk in self.chunks:
            if prev != chunk.name:
                prev = chunk.name
                print("======================")
                print(prev)
                print("======================")
            print(chunk)

    def parse(self):
        with open(self.file, "rb") as image:
            data = bytearray(image.read())
        self.header = data[self.HEADER_START:self.HEADER_END]

        i = self.HEADER_END

        while i < len(data):
            size = int.from_bytes(data[i:i+4], byteorder="big")
            name = data[i+4:i+8].decode("utf-8")
            chunk_data = data[i+8:i+8+size]
            crc = data[i+8+size:i+12+size]
            
            match name:
                case "IHDR":
                    chunk = chunks.IHDR(name, size, chunk_data, crc)
                case "PLTE":
                    chunk = chunks.PLTE(name, size, chunk_data, crc)
                case "tEXt":
                    chunk = chunks.tEXt(name, size, chunk_data, crc)
                case "sRGB":
                    chunk = chunks.sRGB(name, size, chunk_data, crc)
                case "tRNS":
                    chunk = chunks.tRNS(name, size, chunk_data, crc)
                case "gAMA":
                    chunk = chunks.gAMA(name, size, chunk_data, crc)
                case "pHYs":
                    chunk = chunks.pHYs(name, size, chunk_data, crc)
                case "tIME":
                    chunk = chunks.tIME(name, size, chunk_data, crc)
                case "bKGD":
                    chunk = chunks.bKGD(name, size, chunk_data, crc)
                case other:
                    chunk = chunks.Chunk(name, size, chunk_data, crc)
            
            self.chunks.append(chunk)
            i += size + 12

    def isChunkCritical(self, chunk):
        return chunk.name[0].isupper()

    def anonimizeFile(self):
        self.chunks = [chunk for chunk in self.chunks if self.isChunkCritical(chunk)]

    def saveFile(self, filename, anonimize=False):
        with open(filename, "wb") as image:
            image.write(self.header)
            for chunk in self.chunks:
                if anonimize and not self.isChunkCritical(chunk):
                    continue
                image.write(chunk.size.to_bytes(4, byteorder="big"))
                image.write(chunk.name.encode("utf-8"))
                image.write(chunk.data)
                image.write(chunk.crc)
    
    def _calculateCRC(self, name, data):
        new_crc = zlib.crc32(name.encode()+data)
        return new_crc.to_bytes(4, byteorder="big")
    

    def merge_IDAT(self):
        data = bytearray()
        insertion_index = None
        for chunk in self.chunks:
            if chunk.name == "IDAT":
                data += chunk.data
                if insertion_index is None:
                    insertion_index = self.chunks.index(chunk)
        if insertion_index is None:
            return
        merged_chunk = chunks.Chunk("IDAT", len(data), data, self._calculateCRC("IDAT", data))
        self.chunks = [chunk for chunk in self.chunks if chunk.name != "IDAT"]
        self.chunks.insert(insertion_index, merged_chunk)
        
    def merge_tEXt(self):
        data = bytearray()
        insertion_index = None
        for chunk in self.chunks:
            if chunk.name == "tEXt":
                data += chunk.data+b'\x00'
                if insertion_index is None:
                    insertion_index = self.chunks.index(chunk)
        if insertion_index is None:
            return
        merged_chunk = chunks.tEXt("tEXt", len(data), data, self._calculateCRC("tEXt", data))
        self.chunks = [chunk for chunk in self.chunks if chunk.name != "tEXt"]
        self.chunks.insert(insertion_index, merged_chunk)

    def showPLTE(self):
        colors = []
        for chunk in self.chunks:
            if chunk.name == "PLTE":
                colors.extend(chunk.palette)

        colors = sorted([color for color in colors], key=lambda x: colorsys.rgb_to_hls(*x))
        # Convert colors to RGB values
        rgb_colors = [[x/255 for x in color] for color in colors]


        labels = [f"{color}" for color in colors]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

        # Plot the 'spectrum' bar plot
        ax1.bar(labels, height=1, color=rgb_colors, width=1)
        ax1.set_title("Palette colors")
        ax1.set_xticks([])
        ax1.set_yticks([])

        # Plot the 'rectangles' grid of colors
        num_cols = math.ceil(len(colors) ** 0.5)
        num_rows = math.ceil(len(colors) / num_cols)
        for i in range(len(colors)):
            col = i % num_cols
            row = num_rows - i // num_cols
            rect = plt.Rectangle((col, row), 1, 1, color=rgb_colors[i])
            ax2.add_patch(rect)
            # Determine contrast color based on background
            # contrast_color = 'white' if sum(color) / 3 < 128 else 'black'
            # ax2.text(col + 0.5, row + 0.5, f"{color}", ha='center', va='center', color=contrast_color, fontsize=8)
        ax2.set_xlim(0, num_cols)
        ax2.set_ylim(0, num_rows)
        ax2.set_aspect('equal')
        ax2.axis('off')

        plt.tight_layout()
        plt.show()

    def fourierTransform(self):
        image = cv2.imread(self.file, cv2.IMREAD_GRAYSCALE)
        f_transform = np.fft.fft2(image)
        f_transform_shifted = np.fft.fftshift(f_transform)
        spectrum_magnitude = np.abs(f_transform_shifted)
        spectrum_log = np.log(spectrum_magnitude + 1)

        inverse_transform = np.fft.ifft2(f_transform).real

        # Plot the results
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6))
        ax1.imshow(image, cmap='gray')
        ax1.set_title('Original Image')
        ax1.axis('off')
        ax2.imshow(spectrum_log, cmap='gray')
        ax2.set_title('Fourier Spectrum')
        ax2.axis('off')
        ax3.imshow(inverse_transform, cmap='gray')
        ax3.set_title('Inverse Transform')
        ax3.axis('off')
        plt.tight_layout()
        plt.show()
