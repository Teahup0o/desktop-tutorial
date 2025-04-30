# steg_custom.py
from PIL import Image
import math

def encode_lsb(img: Image.Image, payload: bytes) -> Image.Image:
    if len(payload) > 65535:
        raise ValueError("Payload trop gros")
    full = len(payload).to_bytes(2, "big") + payload
    bits = "".join(f"{b:08b}" for b in full)
    nb_required_px = math.ceil(len(bits) / 3)
    if nb_required_px > img.width * img.height:
        raise ValueError("Image trop petite")

    pixels = img.load()
    h, w = img.height, img.width
    idx = 0
    for y in range(h):
        for x in range(w):
            if idx >= len(bits):
                return img
            r, g, b = pixels[x, y]
            r = (r & 0xFE) | int(bits[idx]); idx += 1
            if idx < len(bits):
                g = (g & 0xFE) | int(bits[idx]); idx += 1
            if idx < len(bits):
                b = (b & 0xFE) | int(bits[idx]); idx += 1
            pixels[x, y] = (r, g, b)
    return img

def decode_lsb(img: Image.Image) -> bytes:
    pixels = img.load()
    bits = [(c & 1) for y in range(img.height) for x in range(img.width) for c in pixels[x, y]]
    length = int("".join(map(str, bits[:16])), 2)
    data_bits = bits[16:16 + length*8]
    return bytes(int("".join(map(str, data_bits[i:i+8])), 2) for i in range(0, len(data_bits), 8))
