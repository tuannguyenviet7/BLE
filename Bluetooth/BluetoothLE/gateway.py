import asyncio
from bleak import BleakClient
import pyrebase


firebaseConfig = {
    "apiKey": "AIzaSyA3o246DuYXOqYMIhqVn_YOXql92H_B-Ls",
    "authDomain": "dht11-gw.firebaseapp.com",
    "databaseURL": "https://dht11-gw-default-rtdb.asia-southeast1.firebasedatabase.app",
    "storageBucket": "dht11-gw.firebasestorage.app",
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

# Địa chỉ MAC của HM-10
HMSolf_MAC = "9C:1D:58:8C:29:30"
HMSolf_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"  

async def connect_and_send_data():
    async with BleakClient(HMSolf_MAC) as client:
        print(f"🔗 Kết nối với {HMSolf_MAC} thành công!")

        while True:
            try:
                data = await client.read_gatt_char(HMSolf_UUID)
                data_str = data.decode("utf-8").strip()
                print(f"📩 Nhận: {data_str}")

                # Gửi dữ liệu lên Firebase
                try:
                    temperature, humidity = map(float, data_str.split(","))
                    payload = {
                        "temperature": temperature,
                        "humidity": humidity,
                    }
                    db.child("sensor_data").push(payload)
                    print(f"✅ Đã gửi lên Firebase: {payload}")

                except ValueError:
                    print("⚠️ Dữ liệu không hợp lệ:", data_str)

            except Exception as e:
                print(f"❌ Lỗi đọc dữ liệu: {e}")
            await asyncio.sleep(2)  


asyncio.run(connect_and_send_data())
