README – Vaizdo stebėjimo kameros prototipas

Sistema sudaryta iš ESP32-CAM vaizdo kameros modulio, Raspberry Pi Zero 2W įrenginio, Motion programos, Bash scenarijaus ir Flask galerijos.

ESP32-CAM pateikia JPEG kadrą per /capture adresą. Raspberry Pi Zero 2W įrenginyje Motion programa aptinka vaizdo pokyčius. Aptikus judesį paleidžiamas Bash scenarijus, kuris iš ESP32-CAM paima vieną JPEG kadrą ir išsaugo jį motion_pics kataloge. Flask galerija naršyklėje rodo išsaugotus kadrus.

------------------------------------------------------------
1. Reikalingi failai
------------------------------------------------------------

ESP32-CAM pusėje:

esp32_cam_minimal_capture.ino
- ESP32-CAM programinis kodas.
- Naudojamas Wi-Fi prisijungimui ir JPEG kadro pateikimui per /capture adresą.

Raspberry Pi Zero 2W pusėje:

/etc/motion/motion.conf
- Motion programos konfigūracija.
- Nurodo ESP32-CAM /capture adresą, judesio aptikimo parametrus ir Bash scenarijaus paleidimą.

/home/roruck/iotcam/capture_event_frame.sh
- Bash scenarijus.
- Aptikus judesį paima vieną JPEG kadrą iš ESP32-CAM ir išsaugo jį motion_pics kataloge.
- Kadrai saugomi ne dažniau kaip kas 10 sekundžių.

/home/roruck/iotcam/gallery_app.py
- Flask galerijos programa.
- Nuskaito motion_pics katalogą ir rodo išsaugotus JPEG kadrus naršyklėje.

/home/roruck/iotcam/motion_pics/
- Katalogas, kuriame saugomi judesio metu išsaugoti JPEG kadrai.

------------------------------------------------------------
2. Reikalingos programos
------------------------------------------------------------

Raspberry Pi Zero 2W įrenginyje įdiegiamos reikalingos programos:

sudo apt update
sudo apt install -y motion curl python3-flask

motion – naudojama judesio aptikimui.
curl – naudojamas JPEG kadrui paimti iš ESP32-CAM /capture adreso.
python3-flask – naudojamas naršyklinės galerijos paleidimui.

------------------------------------------------------------
3. Katalogų sukūrimas
------------------------------------------------------------

Sukuriamas projekto katalogas:

mkdir -p /home/USER/iotcam

Sukuriamas JPEG kadrų saugojimo katalogas:

mkdir -p /home/roruck/iotcam/motion_pics

------------------------------------------------------------
4. Failų įkėlimas
------------------------------------------------------------

Motion konfigūracijos failas įkeliamas į:

/etc/motion/motion.conf

Bash scenarijus įkeliamas į:

/home/roruck/iotcam/capture_event_frame.sh

Flask galerijos failas įkeliamas į:

/home/roruck/iotcam/gallery_app.py

ESP32-CAM kodas įkeliamas į ESP32-CAM modulį naudojant Arduino IDE:

esp32_cam_minimal_capture.ino

------------------------------------------------------------
5. ESP32-CAM adresas
------------------------------------------------------------

motion.conf ir capture_event_frame.sh failuose turi būti nurodytas realus ESP32-CAM /capture adresas.

Naudotas adresas:

http://192.168.18.24/capture

Jeigu ESP32-CAM IP adresas pasikeičia, šis adresas turi būti pakeistas abiejuose failuose:

motion.conf faile:

netcam_url http://192.168.18.24/capture

capture_event_frame.sh faile:

URL="http://192.168.18.24/capture"

------------------------------------------------------------
6. Vykdymo teisių suteikimas Bash scenarijui
------------------------------------------------------------

Bash scenarijui suteikiamos vykdymo teisės:

chmod +x /home/roruck/iotcam/capture_event_frame.sh

------------------------------------------------------------
7. Motion paleidimas
------------------------------------------------------------

Motion programa paleidžiama komanda:

sudo systemctl start motion

Po motion.conf pakeitimų Motion perkraunamas:

sudo systemctl restart motion

Motion programa naudoja /etc/motion/motion.conf konfigūraciją.
Aptikus judesį ji paleidžia capture_event_frame.sh scenarijų.

------------------------------------------------------------
8. Flask galerijos paleidimas
------------------------------------------------------------

Flask galerija paleidžiama komanda:

python3 /home/roruck/iotcam/gallery_app.py

Galerija pasiekiama Raspberry Pi naršyklėje:

http://127.0.0.1:8080

------------------------------------------------------------
9. Sistemos veikimo principas
------------------------------------------------------------

1. ESP32-CAM prisijungia prie Wi-Fi tinklo.
2. ESP32-CAM pateikia JPEG kadrą per /capture adresą.
3. Motion programa Raspberry Pi Zero 2W įrenginyje gauna kadrus iš ESP32-CAM.
4. Motion aptinka vaizdo pokyčius pagal pasikeitusių pikselių kiekį.
5. Aptikus judesį paleidžiamas capture_event_frame.sh scenarijus.
6. Scenarijus paima vieną JPEG kadrą iš ESP32-CAM ir išsaugo jį motion_pics kataloge.
7. Naujas kadras saugomas ne dažniau kaip kas 10 sekundžių.
8. Flask galerija atsinaujina kas 10 sekundžių ir rodo išsaugotus kadrus naršyklėje.

------------------------------------------------------------
10. Galutinis reikalingų failų rinkinys
------------------------------------------------------------

esp32_cam_minimal_capture.ino
motion.conf
capture_event_frame.sh
gallery_app.py
motion_pics/
