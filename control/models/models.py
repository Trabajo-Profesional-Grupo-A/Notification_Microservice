# models.py
"""
This module is dedicated for all the pydantic models the API will use.
"""
from pydantic import BaseModel


class DeviceTokenRequest(BaseModel):
    """
    DeviceTokenRequest response model.
    """
    email: str
    device_token: str

