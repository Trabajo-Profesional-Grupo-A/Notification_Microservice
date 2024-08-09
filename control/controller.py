from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from control.routers import notification

app = FastAPI(
    title="Notifications API", description="This is the API for the companies service."
)

origins = ["*"]
app.include_router(notification.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
