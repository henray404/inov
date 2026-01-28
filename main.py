import tinytuya
import time
import requests
import json

DEVICE_ID = 'a3658e534d4fad4173ijbi' 
LOCAL_KEY = "jBM'#B$OGU/aN_Ud"
IP_ADDRESS = '192.168.223.41'  
VERSION = 3.5

last_known_state = {
    'ph': 0.0,
    'orp': 0,
    'tds': 0,
    'temp': 0.0
}

def connect_device():
    print(f"Menghubungkan ke {IP_ADDRESS} (v{VERSION})...")
    try:
        d = tinytuya.OutletDevice(DEVICE_ID, IP_ADDRESS, LOCAL_KEY)
        d.set_version(VERSION)
        d.set_socketPersistent(True)
        print("Terhubung!")
        return d
    except Exception as e:
        print(f"Gagal connect: {e}")
        return None

def kirim_ke_api(state):
    try:
        url = "http://localhost:8000/submit-data"
        payload = {
            "ph": state['ph'],
            "orp": state['orp'],
            "tds": state['tds'],
            "temp": state['temp'],
            "turbidity": 0 
        }
        # Un-comment baris bawah ini kalau server API sudah jalan
        # requests.post(url, json=payload, timeout=1)
    except:
        pass 

def process_data(data):
    global last_known_state # Izinkan fungsi ini update memori global

    if 'dps' not in data: return
    dps = data['dps']

    # 1. Cek pH (ID 126)
    if '106' in dps:
        last_known_state['ph'] = float(dps['106']) / 100.0
        
    # 2. Cek ORP (ID 131)
    if '131' in dps:
        last_known_state['orp'] = int(dps['131'])
        
    # 3. Cek TDS (ID 106)
    if '111' in dps:
        last_known_state['tds'] = int(dps['111'])
        
    # 4. Cek Temp (ID 8)
    if '8' in dps:
        last_known_state['temp'] = float(dps['8']) / 10.0

    print(f"DATA GABUNGAN -> pH: {last_known_state['ph']} | ORP: {last_known_state['orp']} mV | TDS: {last_known_state['tds']} | Temp: {last_known_state['temp']} C")
    

def main():
    device = connect_device()
    
    try:
        print(" Memancing data awal...")
        payload = device.status()
        if payload: process_data(payload)
    except:
        pass

    while True:
        try:
            payload = device.status()
            if payload:
                process_data(payload)
            
            time.sleep(2) 
            
        except Exception as e:
            print(f"Error Loop: {e}")
            time.sleep(5)
            device = connect_device()

if __name__ == "__main__":
    main()