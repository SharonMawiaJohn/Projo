from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float
from config import db

class Property(db.Model):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(255), nullable=True)

    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)

    # Relationships
    agent = relationship('Agent', back_populates='properties')
    bookings = relationship('Booking', back_populates='property')

    def __repr__(self):
        return f'<Property {self.title}, ID {self.id}, Price {self.price}>'

    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'price': self.price,
        }

