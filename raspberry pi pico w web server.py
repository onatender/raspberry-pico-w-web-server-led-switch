import network
import usocket as socket
from machine import Pin

# Wi-Fi Bağlantı Bilgileri
SSID = "SSID_HERE"
PASSWORD = "PW_HERE"

# LED Bağlantısı (GPIO Pin 15 örnek olarak seçildi)
led = Pin(15, Pin.OUT)
integrated_led = Pin(25,Pin.OUT)
integrated_led.on()
# Wi-Fi Bağlantısı
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Wi-Fi'ye bağlanıyor...")
    while not wlan.isconnected():
        pass

    print("Bağlandı!")

    print("IP Adresi:", wlan.ifconfig()[0])

# HTML Arayüzü
html = """<!DOCTYPE html>
<html>
<head>
    <title>LED Kontrol</title>
</head>
<body>
    <h1>LED Kontrol</h1>
    <p>LED Durumu: <strong>{}</strong></p>
    <a href="/?led=on"><button style="font-size:24px">Aç</button></a>
    <a href="/?led=off"><button style="font-size:24px">Kapat</button></a>
</body>
</html>
"""

# Web Sunucusu
def web_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Web sunucusu başlatıldı, IP:", addr)

    while True:
        cl, addr = s.accept()
        print("Yeni bağlantı:", addr)
        request = cl.recv(1024)
        request = str(request)

        # LED Kontrolü
        if "/?led=on" in request:
            led.value(1)
        elif "/?led=off" in request:
            led.value(0)

        # LED Durumu
        led_state = "Açık" if led.value() else "Kapalı"
        
        # HTML Yanıtını Gönderme
        response = html.format(led_state)
        cl.send("HTTP/1.1 200 OK\n")
        cl.send("Content-Type: text/html\n")
        cl.send("Connection: close\n\n")
        cl.sendall(response)
        cl.close()

# Bağlan ve Sunucuyu Başlat
connect_wifi()
web_server()
