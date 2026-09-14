import os
import logging
from supabase import create_client, Client
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabasePusher:
    """
    PUSHES DATA TO SUPABASE
    
    After AI analysis, pushes to Supabase where it:
    - Stores in PostgreSQL
    - Triggers real-time broadcast
    - Notifies all connected users
    """
    
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        logger.info("Supabase Pusher initialized")
        logger.info(f"Supabase URL: {self.supabase_url}")
    
    def push_predictions(self, predictions):
        """
        Push predictions to Supabase
        Triggers: Real-time broadcast to all users
        """
        try:
            if not predictions:
                logger.warning("No predictions to push")
                return False
            
            logger.info(f"Pushing {len(predictions)} predictions to Supabase...")
            
            # Delete old predictions (keep last 24 hours)
            self._cleanup_old_predictions()
            
            # Insert new predictions
            response = self.client.table('predictions').insert(predictions).execute()
            
            if response.data:
                logger.info(f"✓ Successfully pushed {len(response.data)} predictions")
                logger.info(f"✓ Supabase triggered real-time broadcast")
                logger.info(f"✓ All connected users receiving update...")
                return True
            else:
                logger.error(f"Push response error: {response}")
                return False
        
        except Exception as e:
            logger.error(f"Error pushing predictions: {str(e)}")
            return False
    
    def push_events(self, events):
        """
        Push events to Supabase
        """
        try:
            if not events:
                return False
            
            logger.info(f"Pushing {len(events)} events to Supabase...")
            response = self.client.table('events').insert(events).execute()
            
            if response.data:
                logger.info(f"✓ Pushed {len(response.data)} events")
                return True
            return False
        
        except Exception as e:
            logger.error(f"Error pushing events: {str(e)}")
            return False
    
    def push_forecasts(self, forecasts):
        """
        Push forecasts to Supabase
        """
        try:
            if not forecasts:
                return False
            
            logger.info(f"Pushing {len(forecasts)} forecasts to Supabase...")
            response = self.client.table('forecasts').insert(forecasts).execute()
            
            if response.data:
                logger.info(f"✓ Pushed {len(response.data)} forecasts")
                return True
            return False
        
        except Exception as e:
            logger.error(f"Error pushing forecasts: {str(e)}")
            return False
    
    def _cleanup_old_predictions(self):
        """
        Remove predictions older than 24 hours
        """
        try:
            from datetime import datetime, timedelta
            cutoff = datetime.utcnow() - timedelta(hours=24)
            
            response = self.client.table('predictions').delete().lt(
                'created_at', cutoff.isoformat()
            ).execute()
            
            logger.info(f"Cleaned up old predictions")
        except Exception as e:
            logger.warning(f"Cleanup error: {str(e)}")
