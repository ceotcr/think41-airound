from flask import Flask, request, jsonify
from models import db, User, Conversation, Message, Order
from datetime import datetime
import dotenv
import os
from groq import Groq
import json
import re

# Load environment variables
dotenv.load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost:3306/think41'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Groq client
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# Helper functions
def get_or_create_user(username, email):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            first_name=username.split('@')[0],
            last_name='',
            email=email
        )
        db.session.add(user)
        db.session.commit()
    return user

def create_new_conversation(user_id, title="New Conversation"):
    conversation = Conversation(
        user_id=user_id,
        title=title
    )
    db.session.add(conversation)
    db.session.commit()
    return conversation

def get_conversation_history(conversation_id):
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
    return [{"role": "user" if m.is_from_user else "assistant", "content": m.content} for m in messages]

def generate_ai_response(messages):
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=1024
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

def detect_order_query(message):
    """Improved order query detection with regex"""
    order_match = re.search(r"(?:order|details).*?(?:id|#)\s*[:#]?\s*(\d+)", message, re.IGNORECASE)
    return int(order_match.group(1)) if order_match else None

def query_order_details(order_id):
    """Query order details from database"""
    order = Order.query.get(order_id)
    if not order:
        return None
    
    return {
        "order_id": order.order_id,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "shipped_at": order.shipped_at.isoformat() if order.shipped_at else None,
        "num_items": order.num_of_item
    }

# Core Chat API Endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        app.logger.debug(f"Received data: {data}")

        # Validate input
        if not data or not data.get('email') or not data.get('message'):
            return jsonify({"error": "Email and message are required"}), 400

        # Get or create user
        try:
            user = get_or_create_user(data.get('username', data['email']), data['email'])
            app.logger.debug(f"User: {user.id}")
        except Exception as e:
            app.logger.error(f"User error: {str(e)}")
            return jsonify({"error": "User processing failed"}), 500

        # Conversation handling
        try:
            if data.get('conversation_id'):
                conversation = Conversation.query.get(data['conversation_id'])
                if not conversation or conversation.user_id != user.id:
                    return jsonify({"error": "Invalid conversation ID"}), 404
            else:
                conversation = create_new_conversation(user.id)
            app.logger.debug(f"Conversation: {conversation.id}")
        except Exception as e:
            app.logger.error(f"Conversation error: {str(e)}")
            return jsonify({"error": "Conversation processing failed"}), 500
    
        # Store user message
        user_message = Message(
            conversation_id=conversation.id,
            content=data['message'],
            is_from_user=True,
            message_data=data.get('metadata')
        )
        db.session.add(user_message)
        
        # Get conversation history
        history = get_conversation_history(conversation.id)
        
        # Prepare messages for LLM with system instruction
        messages_for_llm = [
            {
                "role": "system",
                "content": """You are an API assistant that responds with JSON only. 
                Analyze the user's request and respond with one of these structures:
                
                For order inquiries:
                {
                    "action": "order_details",
                    "payload": {"id": <order_id>}
                }
                
                For general chat:
                {
                    "action": "general_response",
                    "payload": {"response": "your_response_here"}
                }
                
                Extract order IDs from any format (Order #123, ID: 456, etc.)"""
            },
            *history,
            {"role": "user", "content": data['message']}
        ]
        
        # Get structured response from Groq
        try:
            llm_response = groq_client.chat.completions.create(
                messages=messages_for_llm,
                model="llama-3.1-8b-instant",
                temperature=0.1,  # Lower temp for more consistent JSON
                response_format={"type": "json_object"}
            )
            response_json = json.loads(llm_response.choices[0].message.content)
        except Exception as e:
            return jsonify({"error": f"LLM processing failed: {str(e)}"}), 500
        
        # Process the action
        db_response = None
        ai_response = "I couldn't process that request."
        
        if response_json['action'] == 'order_details':
            order_id = response_json['payload']['id']
            db_response = query_order_details(order_id)
            
            if db_response:
                ai_response = f"Here are details for order #{order_id}:"
                # Add more details from db_response as needed
            else:
                ai_response = f"Order #{order_id} not found."
                
        elif response_json['action'] == 'general_response':
            ai_response = response_json['payload']['response']
        
        # Store AI response
        ai_message = Message(
            conversation_id=conversation.id,
            content=ai_response,
            is_from_user=False,
            message_data={
                "action": response_json['action'],
                "database_used": bool(db_response)
            }
        )
        db.session.add(ai_message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "conversation_id": conversation.id,
            "user_message_id": user_message.id,
            "ai_response": ai_response,
            "ai_message_id": ai_message.id,
            "action": response_json['action'],
            "database_used": bool(db_response),
            "data": db_response if db_response else None,
            "message" : f"Here are details for order #{db_response['order_id']}: {f"Status: {db_response['status']}\nCreated at: {db_response['created_at']}\nNumber of items: {db_response['num_items']}" if db_response else ''}"
        })
    except Exception as e:
        app.logger.error(f"Unhandled exception: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Additional endpoints
@app.route('/api/conversations/<int:user_id>', methods=['GET'])
def get_conversations(user_id):
    conversations = Conversation.query.filter_by(user_id=user_id).order_by(Conversation.updated_at.desc()).all()
    return jsonify([{
        "id": c.id,
        "title": c.title,
        "updated_at": c.updated_at.isoformat(),
        "message_count": len(c.messages)
    } for c in conversations])

@app.route('/api/messages/<int:conversation_id>', methods=['GET'])
def get_messages(conversation_id):
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
    return jsonify([{
        "id": m.id,
        "content": m.content,
        "is_from_user": m.is_from_user,
        "created_at": m.created_at.isoformat()
    } for m in messages])

if __name__ == '__main__':
    app.run(debug=True)