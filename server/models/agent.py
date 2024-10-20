from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt

class Agent(db.Model, SerializerMixin):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    image = Column(String(255), nullable=True)
    _password_hash = Column(String, nullable=False)

    # Relationships
    properties = relationship('Property', back_populates='agent')

    def __repr__(self):
        return f'<Agent {self.username}, ID {self.id}>'

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password)

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
