import logging
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIModel:
    """
    SINGLE AI MODEL FOR ALL PREDICTIONS
    
    Handles:
    - Data analysis
    - Probability calculation
    - Confidence scoring
    - Trend forecasting
    - Recommendation generation
    """
    
    def __init__(self):
        self.model_version = "TheCard-AI-v2.0"
        self.analysis_factors = {
            'rating': 0.35,
            'form': 0.30,
            'draw': 0.15,
            'consistency': 0.10,
            'external': 0.10
        }
        logger.info(f"AI Model initialized: {self.model_version}")
    
    def analyze(self, raw_data):
        """
        Main analysis function
        Input: raw data from external APIs
        Output: predictions ready for Supabase
        """
        predictions = []
        
        for event in raw_data:
            try:
                # Extract event details
                event_name = event.get('event_name')
                runners = event.get('runners', [])
                
                logger.info(f"Analyzing event: {event_name} ({len(runners)} participants)")
                
                # Analyze each runner
                for runner in runners:
                    prediction = self._analyze_runner(runner, event)
                    if prediction:
                        predictions.append(prediction)
                
            except Exception as e:
                logger.error(f"Error analyzing event: {str(e)}")
                continue
        
        return predictions
    
    def _analyze_runner(self, runner, event):
        """
        Analyze individual runner
        """
        try:
            # Extract runner data
            name = runner.get('name', 'Unknown')
            rating = float(runner.get('rating', 50))
            form = float(runner.get('form', 50))
            draw = int(runner.get('draw', 5))
            
            # Calculate composite score
            score = self._calculate_score(rating, form, draw)
            
            # Calculate confidence
            confidence = self._calculate_confidence(rating, form)
            
            # Generate recommendation
            recommendation = self._get_recommendation(score, confidence)
            
            # Generate analysis text
            analysis = self._generate_analysis(runner, event, score)
            
            prediction = {
                'runner_name': name,
                'event_name': event.get('event_name'),
                'track_id': event.get('track_id'),
                'win_probability': round(score, 2),
                'confidence_score': round(confidence, 3),
                'recommendation': recommendation,
                'analysis': analysis,
                'rating': rating,
                'form': form,
                'draw': draw,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            return prediction
        
        except Exception as e:
            logger.error(f"Error analyzing runner: {str(e)}")
            return None
    
    def _calculate_score(self, rating, form, draw):
        """
        Calculate probability score (0-100)
        """
        # Normalize inputs (0-100 range)
        rating_norm = min(100, max(0, rating))
        form_norm = min(100, max(0, form))
        draw_factor = max(1, 10 - draw)  # Better draw = higher factor
        
        # Weighted calculation
        score = (
            rating_norm * self.analysis_factors['rating'] +
            form_norm * self.analysis_factors['form'] +
            (draw_factor * 10) * self.analysis_factors['draw']
        ) / (self.analysis_factors['rating'] + self.analysis_factors['form'] + self.analysis_factors['draw'])
        
        return min(100, max(0, score))
    
    def _calculate_confidence(self, rating, form):
        """
        Calculate confidence score (0-1)
        """
        # How well rating and form align
        alignment = 1 - (abs(rating - form) / 100)
        
        # Base confidence
        confidence = (alignment + 0.5) / 2
        
        return min(1.0, max(0.0, confidence))
    
    def _get_recommendation(self, score, confidence):
        """
        Generate recommendation based on score and confidence
        """
        if score > 60 and confidence > 0.75:
            return "Strong Pick"
        elif score > 50 and confidence > 0.65:
            return "Solid Pick"
        elif score > 40 and confidence > 0.55:
            return "Consider"
        elif score > 25:
            return "Outside Chance"
        else:
            return "Monitor"
    
    def _generate_analysis(self, runner, event, score):
        """
        Generate human-readable analysis
        """
        name = runner.get('name')
        rating = runner.get('rating')
        form = runner.get('form')
        
        analysis = {
            'summary': f"{name} shows strong form and rating",
            'rating': f"Current rating: {rating}/100",
            'form': f"Recent form: {form}/100",
            'score': f"Composite score: {score:.1f}%",
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return analysis
    
    def generate_forecasts(self, raw_data):
        """
        Generate future performance forecasts
        """
        forecasts = []
        
        for event in raw_data:
            runners = event.get('runners', [])
            for runner in runners:
                name = runner.get('name')
                rating = runner.get('rating')
                
                # Generate 7-day forecast
                forecast_values = self._forecast_performance(rating)
                
                forecast = {
                    'runner_id': name,
                    'event_name': event.get('event_name'),
                    'lookahead_days': 7,
                    'forecast_values': forecast_values,
                    'confidence': 0.85,
                    'created_at': datetime.utcnow().isoformat()
                }
                
                forecasts.append(forecast)
        
        return forecasts
    
    def _forecast_performance(self, current_rating):
        """
        Simple linear trend forecast
        """
        forecast = []
        trend = 0.5  # Slight improvement trend
        
        for day in range(7):
            projected = current_rating + (trend * day)
            forecast.append(round(min(100, max(0, projected)), 2))
        
        return forecast
