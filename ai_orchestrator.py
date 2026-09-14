import os
import time
import logging
from datetime import datetime, timedelta
from data_fetcher import DataFetcher
from ai_model import AIModel
from supabase_pusher import SupabasePusher
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AIOrchestrator:
    """
    SINGLE AI MODEL ORCHESTRATOR
    
    Orchestrates the entire pipeline:
    1. Fetch data from external APIs
    2. Run AI analysis & predictions
    3. Push results to Supabase
    4. Supabase distributes to all users
    """
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.ai_model = AIModel()
        self.supabase_pusher = SupabasePusher()
        self.fetch_interval = int(os.getenv('DATA_FETCH_INTERVAL', 300))  # 5 minutes default
        self.is_running = False
        
        logger.info("AI Orchestrator initialized")
        logger.info(f"Fetch interval: {self.fetch_interval} seconds")
    
    def run(self):
        """
        Main loop: Fetch -> Analyze -> Push to Supabase
        """
        self.is_running = True
        logger.info("Starting AI Orchestrator...")
        
        try:
            while self.is_running:
                try:
                    self.process_cycle()
                    logger.info(f"Next cycle in {self.fetch_interval} seconds")
                    time.sleep(self.fetch_interval)
                except Exception as e:
                    logger.error(f"Cycle error: {str(e)}")
                    time.sleep(30)  # Wait 30 seconds before retry
        except KeyboardInterrupt:
            logger.info("Orchestrator stopped by user")
        finally:
            self.stop()
    
    def process_cycle(self):
        """
        One complete cycle: Fetch -> Analyze -> Push
        """
        logger.info("\n" + "="*50)
        logger.info("Starting AI processing cycle")
        logger.info("="*50)
        
        # STEP 1: FETCH DATA FROM EXTERNAL SOURCES
        logger.info("\n[STEP 1] Fetching data from external APIs...")
        raw_data = self.data_fetcher.fetch_all_data()
        
        if not raw_data:
            logger.warning("No data fetched")
            return
        
        logger.info(f"✓ Fetched data for {len(raw_data)} events")
        
        # STEP 2: RUN AI ANALYSIS & PREDICTIONS
        logger.info("\n[STEP 2] Running AI analysis...")
        predictions = self.ai_model.analyze(raw_data)
        
        if not predictions:
            logger.warning("No predictions generated")
            return
        
        logger.info(f"✓ Generated {len(predictions)} predictions")
        
        # Log sample prediction
        if predictions:
            sample = predictions[0]
            logger.info(f"  Sample: {sample['runner_name']} - {sample['win_probability']}% confidence")
        
        # STEP 3: PUSH TO SUPABASE
        logger.info("\n[STEP 3] Pushing predictions to Supabase...")
        success = self.supabase_pusher.push_predictions(predictions)
        
        if success:
            logger.info(f"✓ Pushed {len(predictions)} predictions to Supabase")
            logger.info(f"✓ Supabase now broadcasting to ALL connected users")
            logger.info(f"✓ Mobile/Web/Desktop apps receive update INSTANTLY")
        else:
            logger.error("Failed to push predictions")
        
        # STEP 4: FETCH & PUSH EVENTS
        logger.info("\n[STEP 4] Processing events...")
        events = self.data_fetcher.fetch_events()
        if events:
            self.supabase_pusher.push_events(events)
            logger.info(f"✓ Pushed {len(events)} events")
        
        # STEP 5: GENERATE & PUSH FORECASTS
        logger.info("\n[STEP 5] Generating forecasts...")
        forecasts = self.ai_model.generate_forecasts(raw_data)
        if forecasts:
            self.supabase_pusher.push_forecasts(forecasts)
            logger.info(f"✓ Pushed {len(forecasts)} forecasts")
        
        logger.info("\n" + "="*50)
        logger.info(f"Cycle complete at {datetime.utcnow().isoformat()}")
        logger.info("="*50 + "\n")
    
    def stop(self):
        """Stop the orchestrator"""
        self.is_running = False
        logger.info("AI Orchestrator stopped")


if __name__ == '__main__':
    orchestrator = AIOrchestrator()
    orchestrator.run()
