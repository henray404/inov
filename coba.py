import tinytuya
import time
import json

DEVICE_ID = 'a3658e534d4fad4173ijbi'      # ID dari API Explorer
LOCAL_KEY = "jBM'#B$OGU/aN_Ud"     # Key dari API Explorer
IP_ADDRESS = '192.168.223.41'                  # Hasil Scan Barusan
VERSION = 3.5                                  # Hasil Scan Barusan

print(f"🎯 Menarget IP: {IP_ADDRESS} dengan Protokol v{VERSION}...")

try:
    # Inisialisasi Device
    d = tinytuya.OutletDevice(DEVICE_ID, IP_ADDRESS, LOCAL_KEY)
    d.set_version(VERSION) 
    d.set_socketPersistent(True)  # Wajib untuk v3.4/3.5 biar gak diputus

    print("⏳ Sedang melakukan handshake...")
    
    while True:
        # Kita pakai d.status() untuk memancing data keluar
        payload = d.status()
        
        if 'Error' in payload:
            print(f" Error: {payload}")
        elif 'dps' in payload:
            print(json.dumps(payload['dps'], indent=4))
            break 
        else:
            print("Menunggu data DPS...")
            
        time.sleep(2)

except Exception as e:
    print(f"CRITICAL ERROR: {e}")