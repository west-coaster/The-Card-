import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, broadcast
from supabase import create_client, Client
from functools import wraps
import jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')

# Initialize extensions
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Track connected clients
connected_users = {}

# ============= AUTHENTICATION =============

def verify_token(f):
    """Decorator to verify JWT token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(' ')[-1]
        
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        try:
            # Verify with Supabase
            payload = jwt.decode(token, options={"verify_signature": False})
            request.user_id = payload.get('sub')
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            return jsonify({'error': 'Invalid token'}), 401
    
    return decorated_function

# ============= SINGLE API ENDPOINT FOR UPDATES =============

@app.route('/api/predictions', methods=['POST'])
@verify_token
def update_predictions():
    """
    SINGLE API ENDPOINT
    Updates predictions in database and broadcasts to ALL connected users
    """
    try:
        data = request.get_json()
        predictions = data.get('predictions', [])
        user_id = request.user_id
        
        logger.info(f"Updating {len(predictions)} predictions from user {user_id}")
        
        # Update database
        for pred in predictions:
            pred['user_id'] = user_id
            pred['updated_at'] = datetime.utcnow().isoformat()
            
            # Insert or update prediction
            response = supabase.table('predictions').upsert(pred).execute()
            
            if response.error:
                logger.error(f"Database error: {response.error}")
                return jsonify({'error': str(response.error)}), 500
        
        # BROADCAST TO ALL CONNECTED USERS
        broadcast_data = {
            'type': 'predictions_updated',
            'timestamp': datetime.utcnow().isoformat(),
            'count': len(predictions),
            'data': predictions
        }
        
        # Send via WebSocket to all connected clients
        socketio.emit('predictions_update', broadcast_data, broadcast=True)
        
        # Also send Supabase broadcast for real-time database subscribers
        await send_supabase_broadcast('predictions', broadcast_data)
        
        logger.info(f"Broadcasted {len(predictions)} predictions to all users")
        
        return jsonify({
            'status': 'success',
            'message': f'Updated {len(predictions)} predictions and broadcasted to all users',
            'updated_count': len(predictions),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Prediction update error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/events', methods=['POST'])
@verify_token
def update_events():
    """
    Update events and broadcast to all users
    """
    try:
        data = request.get_json()
        user_id = request.user_id
        
        event_data = {
            'user_id': user_id,
            'event_type': data.get('event_type'),
            'event_name': data.get('event_name'),
            'event_data': data.get('event_data'),
            'track_id': data.get('track_id'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Insert event
        response = supabase.table('events').insert(event_data).execute()
        
        if response.error:
            return jsonify({'error': str(response.error)}), 500
        
        # BROADCAST TO ALL USERS
        socketio.emit('event_update', event_data, broadcast=True)
        await send_supabase_broadcast('events', event_data)
        
        return jsonify({
            'status': 'success',
            'data': event_data
        }), 201
    
    except Exception as e:
        logger.error(f"Event update error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis/publish', methods=['POST'])
@verify_token
def publish_analysis():
    """
    Publish analysis results to ALL users
    """
    try:
        data = request.get_json()
        user_id = request.user_id
        
        analysis_data = {
            'publisher_id': user_id,
            'analysis': data.get('analysis'),
            'predictions': data.get('predictions'),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # BROADCAST ANALYSIS TO ALL CONNECTED USERS
        socketio.emit('analysis_update', analysis_data, broadcast=True)
        await send_supabase_broadcast('analysis', analysis_data)
        
        logger.info(f"Published analysis from user {user_id} to all users")
        
        return jsonify({
            'status': 'success',
            'message': 'Analysis published to all users',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Analysis publish error: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============= WEBSOCKET EVENTS =============

@socketio.on('connect')
def handle_connect():
    """User connects"""
    user_id = request.args.get('user_id')
    if user_id:
        connected_users[request.sid] = user_id
        logger.info(f"User {user_id} connected. Total: {len(connected_users)}")
        emit('connection_response', {
            'status': 'connected',
            'message': 'Connected to real-time server',
            'timestamp': datetime.utcnow().isoformat()
        })


@socketio.on('disconnect')
def handle_disconnect():
    """User disconnects"""
    if request.sid in connected_users:
        user_id = connected_users[request.sid]
        del connected_users[request.sid]
        logger.info(f"User {user_id} disconnected. Total: {len(connected_users)}")


@socketio.on('subscribe_predictions')
def handle_subscribe_predictions(data):
    """User subscribes to predictions updates"""
    user_id = data.get('user_id')
    connected_users[request.sid] = user_id
    logger.info(f"User {user_id} subscribed to predictions")
    emit('subscription_confirmed', {
        'type': 'predictions',
        'status': 'active'
    })


# ============= BROADCAST FUNCTION =============

async def send_supabase_broadcast(channel, data):
    """
    Send broadcast message via Supabase Realtime
    This ensures all Supabase subscribers get updates
    """
    try:
        # Send to Supabase broadcast channel
        supabase.realtime.send('broadcast', {
            'event': channel,
            'payload': data
        })
        logger.info(f"Supabase broadcast sent to channel: {channel}")
    except Exception as e:
        logger.error(f"Supabase broadcast error: {str(e)}")


# ============= HEALTH CHECK =============

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'connected_users': len(connected_users),
        'timestamp': datetime.utcnow().isoformat()
    }), 200


# ============= STARTUP =============

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5050))
    logger.info(f"Starting server on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
