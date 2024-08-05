from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import errors
from control.models.models import DeviceTokenRequest

DB_URI = "mongodb+srv://nencinoza:4VxMOntx1i2W8uQm@users.6jjtd5n.mongodb.net/?retryWrites=true&w=majority&appName=users"

client = MongoClient(DB_URI, server_api=ServerApi('1'))
db = client.notifications
collection = db.device_tokens
collection.create_index([('email', 1)], unique=True)

def post_device_token(device_token: DeviceTokenRequest):
    """
    Post device token for a user.
    """
    try:
        request_device_token = dict(device_token)
        collection.insert_one(request_device_token)
    except Exception as e:
        raise ValueError(str(e))

def get_device_token(email: str):
    """
    Get device token for a user by email.
    """
    try:
        dict = collection.find_one({"email": email})
        if dict is None:
            print("No device token found")
            return None
        return dict.get("device_token")
    except Exception as e:
        raise ValueError(str(e))

def delete_device_token(email: str):
    """
    Delete a device token for a user by email.
    """
    try:
        result = collection.delete_one({"email": email})
        return result.deleted_count
    except Exception as e:
        raise ValueError(str(e))
