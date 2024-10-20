from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from config import app, db, api, bcrypt, migrate
from models.agent import Agent
from models.buyer import Buyer
from models.property import Property
from models.booking import Booking

from datetime import datetime


# Initialize CORS
CORS(app)

# Root route
@app.route('/')
def index():
    return '<h1>Project Server</h1>'


class AgentListResource(Resource):
    def get(self):
        agents = Agent.query.all()
        return jsonify([agent.to_dict() for agent in agents])

api.add_resource(AgentListResource, '/agents')

@app.route('/agents', methods=['POST'])
def create_agent():
    data = request.get_json()
    required_fields = ['username', 'email', 'phone', 'password']
    
    # Validate required fields
    if not data or any(field not in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    new_agent = Agent(
        username=data['username'],
        email=data['email'],
        phone=data['phone'],
        password_hash=data['password']
    )

    db.session.add(new_agent)
    db.session.commit()
    
    return jsonify({"message": "Agent created successfully!"}), 201


@app.route('/agents/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def agentsbyId(id):
    agent = Agent.query.get(id)

    # Handle GET request
    if request.method == 'GET':
        if agent:
            return jsonify(agent.to_dict())
        return {'message': 'Agent not found'}, 404

    # Handle PATCH request
    elif request.method == 'PATCH':
        if not agent:
            return {'message': 'Agent not found'}, 404

        data = request.get_json()
        # Update fields if provided
        for key in ['username', 'email', 'phone', 'password']:
            if key in data:
                setattr(agent, key if key != 'password' else 'password_hash', data[key])

        db.session.commit()
        return {'message': 'Agent updated successfully!'}

    # Handle DELETE request
    elif request.method == 'DELETE':
        if not agent:
            return {'message': 'Agent not found'}, 404

        db.session.delete(agent)
        db.session.commit()
        return {'message': 'Agent deleted successfully!'}

####
# Routes for Buyers

@app.route('/buyers', methods=['GET', 'POST'])
def buyers():
    if request.method == 'GET':
        buyers = Buyer.query.all()
        return jsonify([buyer.to_dict() for buyer in buyers]), 200

    if request.method == 'POST':
        data = request.get_json()

        # Validate data
        if Buyer.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already in use'}), 400
        
        if not data or 'name' not in data or 'email' not in data or 'phone' not in data or 'password' not in data:
            return jsonify({'message': 'Missing required fields'}), 400

        if not data['password']:
            return jsonify({'message': 'Password must be non-empty.'}), 400
        
        # Create a new Buyer instance
        new_buyer = Buyer(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        
        new_buyer.set_password(data['password'])  # Set the password

        db.session.add(new_buyer)
        db.session.commit()
        
        return jsonify(new_buyer.to_dict()), 201  # Return the created buyer's data


@app.route('/buyers/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def buyerbyId(id):
    buyer = Buyer.query.get(id)

    # Handle GET request
    if request.method == 'GET':
        if buyer:
            return jsonify(buyer.to_dict())
        return {'message': 'Buyer not found'}, 404

    # Handle PATCH request
    if request.method == 'PATCH':
        if not buyer:
            return {'message': 'Buyer not found'}, 404

        data = request.get_json()
        if 'name' in data:
            buyer.name = data['name']
        if 'email' in data:
            buyer.email = data['email']
        if 'phone' in data:
            buyer.phone = data['phone']
        if 'password' in data:
            buyer.set_password(data['password'])  # Hash the password

        db.session.commit()
        return {'message': 'Buyer updated successfully!'}

    # Handle DELETE request
    if request.method == 'DELETE':
        if not buyer:
            return {'message': 'Buyer not found'}, 404

        db.session.delete(buyer)
        db.session.commit()
        return {'message': 'Buyer deleted successfully!'}

####
@app.route('/properties', methods=['GET', 'POST'])
def properties():
    if request.method == 'GET':
        properties = Property.query.all()
        property_list = [
            {
                "id": property.id,
                "title": property.title,
                "agent": Agent.query.get(property.agent_id).username if Agent.query.get(property.agent_id) else "Unknown",
                "location": property.location,
                "price": property.price
            } for property in properties
        ]
        return jsonify(property_list)

    if request.method == 'POST':
        data = request.get_json()

        # Check for required fields
        if not data or 'agent_id' not in data or 'title' not in data or 'description' not in data or 'location' not in data or 'price' not in data:
            return jsonify({"message": "Missing required fields"}), 400

        # Create a new Property instance
        new_property = Property(
            agent_id=data['agent_id'],
            title=data['title'],
            description=data['description'],
            location=data['location'],
            price=data['price'],
            image=data.get('image_url')  # Use 'image_url' for consistency
        )
        
        db.session.add(new_property)
        db.session.commit()
        
        return jsonify(new_property.to_dict()), 201


@app.route('/properties/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def propertybyId(id):
    property_item = Property.query.get(id)

    # Handle GET request
    if request.method == 'GET':
        if property_item:
            return jsonify(property_item.to_dict())
        return {'message': 'Property not found'}, 404

    # Handle PATCH request
    if request.method == 'PATCH':
        if not property_item:
            return {'message': 'Property not found'}, 404

        data = request.get_json()
        if 'title' in data:
            property_item.title = data['title']
        if 'description' in data:
            property_item.description = data['description']
        if 'location' in data:
            property_item.location = data['location']
        if 'price' in data:
            property_item.price = data['price']
        if 'image_url' in data:
            property_item.image_url = data['image_url']

        db.session.commit()
        return {'message': 'Property updated successfully!'}

    # Handle DELETE request
    if request.method == 'DELETE':
        if not property_item:
            return {'message': 'Property not found'}, 404

        db.session.delete(property_item)
        db.session.commit()
        return {'message': 'Property deleted successfully!'}

##Booking Routes

@app.route('/bookings', methods=['GET', 'POST'])
def manage_bookings():
    if request.method == 'GET':
        bookings = Booking.query.all()
        return jsonify([booking.to_dict() for booking in bookings])

    if request.method == 'POST':
        data = request.get_json()
        
        booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()

        new_booking = Booking(
            buyer_id=data['buyer_id'],
            property_id=data['property_id'],
            booking_date=booking_date,
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify(new_booking.to_dict()), 201


@app.route('/bookings/<int:booking_id>', methods=['GET', 'PATCH', 'DELETE'])
def bookingsbyId(booking_id):
    booking = Booking.query.get(booking_id)

    if request.method == 'GET':
        if booking:
            return jsonify(booking.to_dict())
        return {'message': 'Booking not found'}, 404

    if request.method == 'PATCH':
        if not booking:
            return {'message': 'Booking not found'}, 404

        data = request.get_json()
        if 'booking_date' in data:
            booking.booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()

        db.session.commit()
        return {'message': 'Booking updated successfully!'}

    if request.method == 'DELETE':
        if not booking:
            return {'message': 'Booking not found'}, 404

        db.session.delete(booking)
        db.session.commit()
        return {'message': 'Booking deleted successfully!'}


@app.route('/login', methods=['POST'])
def agentlogin():
    data = request.json
    agent = Agent.query.filter_by(email=data['email']).first()
    if agent and agent.authenticate(data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid email or password'}), 401



@app.route('/buyerlogin', methods=['POST'])
def buyerlogin():
    data = request.get_json()
    buyer = Buyer.query.filter_by(email=data['email']).first()
    if buyer and buyer.verify_password(data['password']):
        return jsonify({
            'id': buyer.id,
            'name': buyer.name,
            'email': buyer.email,
            # Add other fields as necessary
        }), 200
    return jsonify({'error': 'Invalid email or password'}), 401


if __name__ == '__main__':
    app.run(port=5555, debug=True)
