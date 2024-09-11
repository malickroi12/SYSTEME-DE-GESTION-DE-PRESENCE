import cv2
import numpy as np
from pyzbar.pyzbar import decode
import mysql.connector as msqlc
from datetime import date, datetime



#temps
now = datetime.now()
ctime = now.strftime("%H:%M:%S")

#date
day = date.today()
nday = day.strftime("%d-%m-%Y")


try:
    bd = msqlc.connect(
        host = "localhost",
        port = 3325,
        user = "root",
        passwd = "",
        database = "qrcode"
    )
except Exception:
    print("erreur de connexion à la base de données")


cursor = bd.cursor()
query = "INSERT INTO presence ( noms, heure, date ) VALUES ( %s,%s ,%s )"


cap = cv2.VideoCapture(0)
cap.set(3, 640) #largeur
cap.set(4, 480) #hauteur

#liste des étudiants autorisés
with open('students.txt') as f:
    students = f.read().splitlines()


while True:

    ret, img = cap.read()

    for params in decode(img):
        print(params.data)
        datas = params.data.decode('utf-8')

        if datas in students:
            statut = "AUTORISE"
            couleur = (0, 255, 0) #verte
            val = (datas, str(ctime), str(nday))
            cursor.execute(query, val)
            bd.commit()
        else:
            statut = "INTRUS"
            couleur = (0, 0, 255)  # rouge

        pts = np.array([params.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, couleur, 5)
        pts2 = params.rect

        cv2.putText(img, statut, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9,couleur,2)


    cv2.imshow("show qr", img)
    cv2.waitKey(2)
