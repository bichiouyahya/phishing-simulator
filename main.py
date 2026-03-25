import secrets
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.utils.mailer import send_email
from app.database import SessionLocal, engine
from app.models import Base, EmailSend, Event, Credential, Target, Campaign

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Phishing Simulator Running"}


@app.get("/track", response_class=HTMLResponse)
def track(request: Request, token: str):
    db = SessionLocal()

    email = db.query(EmailSend).filter(EmailSend.token == token).first()

    if not email:
        return {"error": "Invalid token"}

    event = Event(
        email_id=email.id,
        event_type="clicked",
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    db.add(event)
    db.commit()

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"token": token}
    )


@app.get("/setup-test")
def setup_test():
    db = SessionLocal()

    target = Target(
    	email="example@test.com",
    	name="Test User"
    )

    db.add(target)
    db.commit()
    db.refresh(target)

    campaign = Campaign(
        name="Fake Login"
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    token = secrets.token_urlsafe(16)

    email = EmailSend(
        target_id=target.id,
        campaign_id=campaign.id,
        token=token
    )
    db.add(email)
    db.commit()

    return {
        "message": "Test data created",
        "token": token
    }


@app.post("/submit")
def submit(token: str = Form(...), email: str = Form(...), password: str = Form(...)):
    db = SessionLocal()

    email_record = db.query(EmailSend).filter(EmailSend.token == token).first()

    if not email_record:
        return {"error": "Invalid token"}

    cred = Credential(
        email_id=email_record.id,
        email=email,
        password=password
    )

    db.add(cred)

    event = Event(
        email_id=email_record.id,
        event_type="submitted",
        ip_address="unknown",
        user_agent="unknown"
    )

    db.add(event)
    db.commit()

    print("Captured credentials:")
    print("Email:", email)
    print("Password:", password)

    return {"message": "Login failed"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    db = SessionLocal()

    emails = db.query(EmailSend).all()

    data = []

    for email in emails:
        click_event = db.query(Event).filter(
            Event.email_id == email.id,
            Event.event_type == "clicked"
        ).first()

        credential = db.query(Credential).filter(
            Credential.email_id == email.id
        ).first()

        data.append({
            "email": email.target.email,
            "clicked": click_event is not None,
            "submitted": credential is not None,
            "ip": click_event.ip_address if click_event else "N/A",
            "user_agent": click_event.user_agent if click_event else "N/A"
        })

    total_sent = len(emails)
    total_clicked = sum(1 for d in data if d["clicked"])
    total_submitted = sum(1 for d in data if d["submitted"])
    click_rate = (total_clicked / total_sent * 100) if total_sent > 0 else 0
    submit_rate = (total_submitted / total_sent * 100) if total_sent > 0 else 0

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "data": data,
            "total_sent": total_sent,
            "total_clicked": total_clicked,
            "total_submitted": total_submitted,
	    "click_rate": round(click_rate, 2),
	    "submit_rate": round(submit_rate, 2)
        }
    )


@app.get("/send-test")
def send_test():
    db = SessionLocal()

    target = db.query(Target).first()
    campaign = db.query(Campaign).first()

    token = secrets.token_urlsafe(16)

    email_record = EmailSend(
        target_id=target.id,
        campaign_id=campaign.id,
        token=token
    )

    db.add(email_record)
    db.commit()

    link = f"http://127.0.0.1:8000/track?token={token}"

    html = f"""
    <h2>Account Notification</h2>
    <p>We noticed a login attempt from a new device.</p>
    <p>Please confirm your account activity:</p>
    <p><a href="{link}">Review Activity</a></p>
    <p>If this was not you, please secure your account.</p>
    """

    send_email(target.email, "Urgent Security Alert", html)

    return {"message": "Email sent", "link": link}