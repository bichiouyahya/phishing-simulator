from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()
class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)

    emails = relationship("EmailSend", back_populates="target")

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    emails = relationship("EmailSend", back_populates="campaign")

class EmailSend(Base):
    __tablename__ = "email_sends"

    id = Column(Integer, primary_key=True, index=True)

    target_id = Column(Integer, ForeignKey("targets.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))

    token = Column(String, unique=True, index=True)
    sent_at = Column(DateTime, default=datetime.utcnow)

    target = relationship("Target", back_populates="emails")
    campaign = relationship("Campaign", back_populates="emails")
    events = relationship("Event", back_populates="email")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    email_id = Column(Integer, ForeignKey("email_sends.id"))

    event_type = Column(String)  # opened, clicked, submitted
    timestamp = Column(DateTime, default=datetime.utcnow)

    ip_address = Column(String)
    user_agent = Column(String)

    email = relationship("EmailSend", back_populates="events")


class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)

    email_id = Column(Integer, ForeignKey("email_sends.id"))

    email = Column(String)
    password = Column(String)

    timestamp = Column(DateTime, default=datetime.utcnow)

    email_send = relationship("EmailSend")