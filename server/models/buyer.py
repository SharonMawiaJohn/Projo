from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

class Buyer(db.Model, SerializerMixin):
    __tablename__ = 'buyers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    _password_hash = Column(String(128), nullable=False)  


    # Relationships
    bookings = relationship('Booking', back_populates='buyer')

    def __repr__(self):
        return f'Buyer {self.name}, ID {self.id}'  


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
        }

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
