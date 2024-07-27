import pyrebase
import requests

# Firebase configuration
config = {
  "apiKey": "AIzaSyATnRiTlsK0DbEpymmBwG0YCULvwYKJ4ho",
  "authDomain": "safezone-8496c.firebaseapp.com",
  "databaseURL": "https://safezone-8496c-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "safezone-8496c",
  "storageBucket": "safezone-8496c.appspot.com",
  "messagingSenderId": "689818781895",
  "appId": "1:689818781895:web:622a7572bd9d4d6e85d6e2"
}

# REST API configuration
api_url = "https://your-rest-api-endpoint.com/upload"  

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Function to fetch data
def fetch_data():
    try:
        data = db.child("sensorData").get()
        if data.val():
            mq3_value = data.val().get("MQ3")
            mq135_value = data.val().get("MQ135")
            return mq3_value, mq135_value
        else:
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Function to upload data to REST API
def upload_data(mq3_value, mq135_value):
    try:
        payload = {
            "MQ3": mq3_value,
            "MQ135": mq135_value
        }
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            print("Data successfully uploaded to REST API")
        else:
            print(f"Failed to upload data: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred while uploading data: {e}")

# Fetch data and store in variables
mq3_data, mq135_data = fetch_data()

# Optional: print fetched data
print(f"MQ3 Data: {mq3_data}")
print(f"MQ135 Data: {mq135_data}")

# Save to a file if needed (for testing or debugging purposes)
with open("data.txt", "w") as file:
    file.write(f"MQ3 Data: {mq3_data}\n")
    file.write(f"MQ135 Data: {mq135_data}\n")

# Upload data to REST API
if mq3_data is not None and mq135_data is not None:
    upload_data(mq3_data, mq135_data)
else:
    print("No data to upload")
