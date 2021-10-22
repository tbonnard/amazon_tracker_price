from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    items = relationship("Item", back_populates="user")


class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    price_limit = db.Column(db.Float, nullable=False)
    product_title = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="items")
