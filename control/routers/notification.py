"""
This module contains the API endpoints for the notifications service.
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging


cred = credentials.Certificate("./tpp-grupoa-firebase-adminsdk-5jdgm-65be1e639d.json")
firebase_admin.initialize_app(cred)

from fastapi import (
    APIRouter,
    HTTPException,
)

from control.codes import (
    BAD_REQUEST,
    DEVICE_TOKEN_NOT_FOUND
)

from control.models.models import DeviceTokenRequest, NotificationRequest
from repository.notification_repository import get_device_token, post_device_token, delete_device_token

router = APIRouter(
    tags=["notifications"],
    prefix="/notifications",
)
origins = ["*"]

from repository.notification_repository import post_device_token, get_device_token, delete_device_token

@router.post("/device-token", response_model=DeviceTokenRequest)
def api_post_device_token(device_token_request: DeviceTokenRequest):
    """
    Post a device token
    """
    try:
        post_device_token(device_token_request)
        return device_token_request
    except Exception as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
    

@router.get("/device-token/{email}")
def api_get_device_token(email: str):
    """
    Get a device token
    """
    device_token = get_device_token(email)
    if device_token is None:
        raise HTTPException(status_code=DEVICE_TOKEN_NOT_FOUND, detail="Token not found")
    return {"token": device_token}


@router.delete("/device-token/{email}")
def api_delete_device_token(email: str):
    """
    Delete a device token
    """
    try:
        delete_device_token(email)
        return {"message": "Token deleted"}
    except Exception as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))



@router.post("/device-token/send")
def api_send_notification(notification_request: NotificationRequest):
    """
    Send a notification to a user's device
    """
    try:
        for email in notification_request.email_receivers:
            device_token = get_device_token(email)
            if device_token is None:
                raise HTTPException(status_code=DEVICE_TOKEN_NOT_FOUND, detail="Device token not found for the user")

            message = messaging.Message(
                notification=messaging.Notification(
                    title=notification_request.title,
                    body=notification_request.body,
                ),
                data=notification_request.data,
                token=device_token,
            )
            response = messaging.send(message)
        return {"message": "Notifications sent successfully", "response": response}
    except Exception as e:
        raise HTTPException(status_code=BAD_REQUEST, detail=str(e))
