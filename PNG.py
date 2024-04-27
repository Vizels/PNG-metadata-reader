import zlib
import cv2
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

    def parse(self):
        with open(self.file, "rb") as image:
            data = bytearray(image.read())
        self.header = data[self.HEADER_START:self.HEADER_END]
        print(self.header)

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
                    if chunk.keyword.startswith("exif:"):
                        chunk = chunks.eXIf("eXIf", size, chunk_data, crc)
                case "sRGB":
                    chunk = chunks.sRGB(name, size, chunk_data, crc)
                case other:
                    chunk = chunks.Chunk(name, size, chunk_data, crc)
            
            self.chunks.append(chunk)
            i += size + 12
        
        prev = ""
        for chunk in self.chunks:
            if prev != chunk.name:
                prev = chunk.name
                print("======================")
                print(prev)
                print("======================")
            print(chunk)

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
    
    def mergeIDAT(self):
        data = bytearray([])
        for chunk in self.chunks:
            if chunk.name == "IDAT":
                data += chunk.data
        new_crc = zlib.crc32(data)
        merged_chunk = chunks.Chunk("IDAT", len(data), data, new_crc.to_bytes(4, byteorder="big"))
        self.chunks = [chunk for chunk in self.chunks if chunk.name != "IDAT"]
        self.chunks.insert(-1, merged_chunk)

    def showPLTE(self):
        for chunk in self.chunks:
            if chunk.name == "PLTE":
                fig, ax = plt.subplots(figsize=(12, 12))
                colors = chunk.palette
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

    def fourierTransform(self):
        image = cv2.imread(self.file, cv2.IMREAD_GRAYSCALE)
        # Step 2: Perform Fourier Transform
        f_transform = np.fft.fft2(image)

        # Step 3: Shift the zero frequency component
        f_transform_shifted = np.fft.fftshift(f_transform)

        # Step 4: Visualize the spectrum (optional)
        spectrum_magnitude = np.abs(f_transform_shifted)
        spectrum_log = np.log(spectrum_magnitude + 1)  # Apply log for better visualization

        plt.imshow(spectrum_log, cmap='gray')
        plt.title('Fourier Spectrum')
        plt.colorbar()
        plt.show()
