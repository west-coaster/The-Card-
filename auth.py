import jwt
import bcrypt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

class SubscriptionAuth:
    """Manages subscription-based JWT authentication."""
    
    def __init__(self, secret_key=None):
        self.secret_key = secret_key or os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
        self.algorithm = 'HS256'
        self.token_expiry = 86400  # 24 hours
    
    def hash_password(self, password):
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password, hashed):
        """Verify a password against its hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def generate_token(self, user_id, subscription_tier='basic', expires_in=None):
        """Generate a JWT token for authenticated user."""
        if expires_in is None:
            expires_in = self.token_expiry
        
        payload = {
            'user_id': user_id,
            'subscription_tier': subscription_tier,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token):
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def refresh_token(self, token):
        """Refresh an expiring token."""
        payload = self.verify_token(token)
        if payload:
            return self.generate_token(payload['user_id'], payload['subscription_tier'])
        return None


def require_subscription(subscription_tiers=None):
    """Decorator to require subscription authentication."""
    if subscription_tiers is None:
        subscription_tiers = ['basic', 'premium', 'professional']
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            
            # Extract token from Authorization header
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                try:
                    token = auth_header.split(' ')[1]
                except IndexError:
                    return jsonify({'error': 'Invalid authorization header'}), 401
            
            if not token:
                return jsonify({'error': 'Missing authentication token'}), 401
            
            auth = SubscriptionAuth()
            payload = auth.verify_token(token)
            
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            if payload['subscription_tier'] not in subscription_tiers:
                return jsonify({'error': 'Insufficient subscription level'}), 403
            
            # Store payload in request context
            request.user = payload
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    return decorator
