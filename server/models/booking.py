from sqlalchemy import Column, Integer, ForeignKey, Date, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from config import db

class Booking(db.Model, SerializerMixin):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey('buyers.id'), nullable=False)
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)
    booking_date = Column(Date, nullable=False)
    
    # Relationships
    buyer = relationship('Buyer', back_populates='bookings')
    property = relationship('Property', back_populates='bookings')

    def __repr__(self):
        return f'<Booking ID {self.id}, Buyer ID {self.buyer_id}, Property ID {self.property_id}, Status {self.status}>'

    def to_dict(self):
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'property_id': self.property_id,
            'booking_date': self.booking_date,
            'buyer': self.buyer.to_dict() if self.buyer else None,
            'property': self.property.to_dict() if self.property else None,
        }
