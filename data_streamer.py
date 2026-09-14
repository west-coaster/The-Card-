import threading
import time
import json
from datetime import datetime
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealtimeDataStreamer:
    """Manages real-time data streaming and daily updates."""
    
    def __init__(self, socketio=None):
        self.socketio = socketio
        self.scheduler = BackgroundScheduler()
        self.active_streams = {}
        self.data_cache = {}
    
    def start_scheduler(self):
        """Start the background scheduler for daily updates."""
        # Schedule daily data refresh at 6 AM UTC
        self.scheduler.add_job(
            func=self.refresh_daily_data,
            trigger=CronTrigger(hour=6, minute=0),
            id='daily_refresh',
            name='Daily data refresh',
            replace_existing=True
        )
        
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Background scheduler started")
    
    def stop_scheduler(self):
        """Stop the background scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Background scheduler stopped")
    
    def refresh_daily_data(self):
        """Refresh event and analytics data daily."""
        logger.info("Starting daily data refresh at %s", datetime.utcnow())
        
        try:
            # Fetch updated event data from external sources
            updated_events = self._fetch_external_events()
            self.data_cache['events'] = updated_events
            
            # Broadcast to all connected clients
            if self.socketio:
                self.socketio.emit('data_updated', {
                    'timestamp': datetime.utcnow().isoformat(),
                    'event_count': len(updated_events),
                    'status': 'success'
                }, broadcast=True)
            
            logger.info("Daily data refresh completed: %d events", len(updated_events))
        
        except Exception as e:
            logger.error("Daily data refresh failed: %s", str(e))
            if self.socketio:
                self.socketio.emit('data_error', {'error': str(e)}, broadcast=True)
    
    def stream_live_updates(self, session_id, track_id, interval=5):
        """Stream live updates for a specific track."""
        self.active_streams[session_id] = {
            'track_id': track_id,
            'interval': interval,
            'active': True,
            'started_at': datetime.utcnow()
        }
        
        def _stream():
            while self.active_streams[session_id]['active']:
                try:
                    # Fetch latest data for the track
                    live_data = self._fetch_track_data(track_id)
                    
                    if self.socketio:
                        self.socketio.emit('live_update', {
                            'session_id': session_id,
                            'track_id': track_id,
                            'data': live_data,
                            'timestamp': datetime.utcnow().isoformat()
                        }, room=session_id)
                    
                    time.sleep(interval)
                
                except Exception as e:
                    logger.error("Stream error for session %s: %s", session_id, str(e))
                    time.sleep(5)
        
        # Run stream in background thread
        thread = threading.Thread(target=_stream, daemon=True)
        thread.start()
    
    def stop_stream(self, session_id):
        """Stop streaming for a session."""
        if session_id in self.active_streams:
            self.active_streams[session_id]['active'] = False
            del self.active_streams[session_id]
            logger.info("Stream stopped for session %s", session_id)
    
    def _fetch_external_events(self):
        """Fetch event data from external APIs."""
        # This would connect to real data sources
        # For now, return placeholder data
        return [
            {
                'event_id': 'evt_001',
                'name': 'Sample Event Analysis',
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'active',
                'participants': 4
            }
        ]
    
    def _fetch_track_data(self, track_id):
        """Fetch live data for a specific track."""
        # This would fetch real-time track data
        return {
            'track_id': track_id,
            'current_event': 'Live Event Analysis',
            'participants_count': 4,
            'timestamp': datetime.utcnow().isoformat()
        }


class EventCache:
    """In-memory cache for event data with TTL."""
    
    def __init__(self, ttl_seconds=3600):
        self.cache = {}
        self.ttl = ttl_seconds
    
    def get(self, key):
        """Get cached value if not expired."""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key, value):
        """Set cache value with timestamp."""
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """Clear all cached data."""
        self.cache.clear()
