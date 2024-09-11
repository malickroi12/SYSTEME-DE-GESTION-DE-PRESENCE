import qrcode
from qrcode.constants import ERROR_CORRECT_L , ERROR_CORRECT_Q
import time

students = []

with open('students.txt') as f:
    students = f.read().splitlines()


for student in students :
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(student) #ajouter la donnée
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save(f"photos/{student.split('-')[0]}.png")




