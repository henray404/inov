import tinytuya

# Scan network
devices = tinytuya.deviceScan(verbose=True)

for dev in devices:
    print(f"Name: {dev['name']}")
    print(f"IP Address: {dev['ip']}")
    print(f"Device ID: {dev['id']}")
    print(f"Version: {dev['version']}") 

if not devices:
    print("TIDAK DITEMUKAN DEVICE APAPUN.")