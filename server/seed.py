from config import db, app  # Import app and db
from models.agent import Agent
from models.buyer import Buyer
from models.property import Property
from models.booking import Booking
from datetime import datetime

# Function to seed the database
def seed_database():
    # Clear existing data (optional)
    db.drop_all()  # Uncomment if you want to drop all tables before seeding
    db.create_all()  # Create tables

    # Create agents
    agent1 = Agent(username='agent_one', email='agent1@example.com', phone='1234567890', password_hash='password1')
    agent2 = Agent(username='agent_two', email='agent2@example.com', phone='0987654321', password_hash='password2')

    # Create buyers
    buyer1 = Buyer(name='buyer_one', email='buyer1@example.com', phone='1234567890', password_hash='password1')
    buyer2 = Buyer(name='buyer_two', email='buyer2@example.com', phone='0987654321', password_hash='password2')

    # Create properties
    property1 = Property(agent_id=1, title='Cozy Cottage', description='A lovely cottage in the countryside.', location='123 Cottage Lane', price=250000.00)
    property2 = Property(agent_id=2, title='Urban Apartment', description='A modern apartment in the city.', location='456 City Street', price=300000.00)

    # Create bookings
    booking1 = Booking(buyer_id=1, property_id=1, booking_date=datetime.now())
    booking2 = Booking(buyer_id=2, property_id=2, booking_date=datetime.now())

    # Add all to session
    db.session.add_all([agent1, agent2, buyer1, buyer2, property1, property2, booking1, booking2])

    # Commit the session
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()
