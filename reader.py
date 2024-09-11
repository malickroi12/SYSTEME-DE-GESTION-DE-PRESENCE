import cv2
from pyzbar.pyzbar import decode

img = cv2.imread("photos/yt.png")

code = decode(img)

print(code)

