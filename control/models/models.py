# models.py
"""
This module is dedicated for all the pydantic models the API will use.
"""
from pydantic import BaseModel
from typing import List

class DeviceTokenRequest(BaseModel):
    """
    DeviceTokenRequest response model.
    """
    email: str
    device_token: str

class NotificationRequest(BaseModel):
    email_receivers: List[str]
    title: str
    body: str
    data: dict
