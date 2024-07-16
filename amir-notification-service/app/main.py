import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from sqlmodel import SQLModel, Session, create_engine
from app.models.notification_model import Notification
from app.crud.notification_crud import create_notification, get_notification
from app.deps import get_session
from app.settings import GMAIL_USERNAME, GMAIL_PASSWORD, GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT, DATABASE_URL
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create the database engine
engine = create_engine(str(DATABASE_URL)) if DATABASE_URL else None

# Create the database and tables
def create_db_and_tables():
    if engine:
        SQLModel.metadata.create_all(engine)
    else:
        logging.warning("DATABASE_URL is not set; skipping database creation.")

# Context manager for lifespan
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    create_db_and_tables()
    yield

# Initialize the FastAPI app
app = FastAPI(lifespan=lifespan, title="Notification Service", version="0.1.0")

# Function to send email
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = GMAIL_USERNAME
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(GMAIL_SMTP_SERVER, GMAIL_SMTP_PORT)
        server.starttls()
        server.login(GMAIL_USERNAME, str(GMAIL_PASSWORD))
        text = msg.as_string()
        server.sendmail(GMAIL_USERNAME, to_email, text)
        server.quit()
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        return False

@app.get("/")
def read_root():
    return {"Hello": "Mehjabeen Amir"}

@app.post("/notifications/", response_model=Notification)
def create_new_notification(notification: Notification, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    new_notification = create_notification(notification, session)
    background_tasks.add_task(send_email, notification.email, "New Notification", f"Your notification has been created: {notification.content}")
    return new_notification

@app.get("/notifications/{notification_id}", response_model=Notification)
def get_single_notification(notification_id: int, session: Session = Depends(get_session)):
    notification = get_notification(notification_id, session)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification
