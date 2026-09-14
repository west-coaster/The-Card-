from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAnalyst:
    """Enhanced AI Analyst with sentiment analysis and trend forecasting."""
    
    def __init__(self):
        self.name = "The Card AI Analyst"
        self.analysis_models = [
            'form_analysis',
            'going_compatibility',
            'jockey_trainer_synergy',
            'trend_forecast'
        ]
    
    def analyze_race(self, runners_data):
        """
        Comprehensive race analysis with multiple dimensions.
        
        Args:
            runners_data: List of runner objects with name, score, form, weight, etc.
        
        Returns:
            List of detailed insights for each runner
        """
        insights = []
        
        for runner in runners_data:
            score = runner.get('score', runner.get('rating', 50))
            
            # Determine confidence tier
            if score > 85:
                verdict = "Strong contender"
                confidence = "High"
            elif score > 70:
                verdict = "Solid prospect"
                confidence = "Medium"
            elif score > 50:
                verdict = "Moderate chance"
                confidence = "Medium"
            else:
                verdict = "Outsider"
                confidence = "Low"
            
            # Calculate trend based on historical form
            trend = self._calculate_trend(runner.get('form', []))
            
            insight = {
                "runner": runner.get("name"),
                "verdict": verdict,
                "score": score,
                "confidence": confidence,
                "trend": trend,
                "analysis_timestamp": datetime.utcnow().isoformat(),
                "key_factors": self._extract_key_factors(runner)
            }
            
            insights.append(insight)
        
        return insights
    
    def forecast_performance(self, runner_data, historical_form):
        """
        Forecast future performance based on historical data.
        
        Args:
            runner_data: Current runner attributes
            historical_form: List of past performance scores
        
        Returns:
            Performance forecast with confidence intervals
        """
        if not historical_form or len(historical_form) < 2:
            return {
                'forecast': 'Insufficient data',
                'confidence': 0.0,
                'status': 'pending'
            }
        
        # Calculate trend direction
        recent_avg = sum(historical_form[-3:]) / len(historical_form[-3:]) if len(historical_form) >= 3 else historical_form[0]
        overall_avg = sum(historical_form) / len(historical_form)
        
        trend_direction = "improving" if recent_avg > overall_avg else "declining" if recent_avg < overall_avg else "stable"
        
        # Calculate confidence based on consistency
        variance = self._calculate_variance(historical_form)
        consistency_score = max(0, 100 - variance)
        
        return {
            'trend_direction': trend_direction,
            'recent_average': round(recent_avg, 2),
            'overall_average': round(overall_avg, 2),
            'consistency_score': round(consistency_score, 2),
            'confidence': round(consistency_score / 100, 2),
            'forecast_generated': datetime.utcnow().isoformat()
        }
    
    def analyze_sentiment(self, commentary):
        """
        Analyze sentiment from race commentary.
        
        Args:
            commentary: Text commentary or analysis notes
        
        Returns:
            Sentiment analysis result
        """
        # Simple sentiment keywords (can be enhanced with NLP)
        positive_keywords = ['strong', 'excellent', 'dominant', 'impressive', 'consistent', 'threat']
        negative_keywords = ['weak', 'poor', 'struggling', 'unreliable', 'declining', 'doubt']
        
        if not commentary:
            return {'sentiment': 'neutral', 'score': 0.5}
        
        commentary_lower = commentary.lower()
        
        positive_count = sum(1 for word in positive_keywords if word in commentary_lower)
        negative_count = sum(1 for word in negative_keywords if word in commentary_lower)
        
        # Calculate sentiment score (-1 to 1)
        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 0.5
        else:
            sentiment_score = (positive_count - negative_count) / total
        
        sentiment = "positive" if sentiment_score > 0.3 else "negative" if sentiment_score < -0.3 else "neutral"
        
        return {
            'sentiment': sentiment,
            'score': round((sentiment_score + 1) / 2, 2),  # Normalize to 0-1
            'analysis_timestamp': datetime.utcnow().isoformat()
        }
    
    def _calculate_trend(self, form_list):
        """Calculate trend from form list (e.g., [1,2,1,3,1])."""
        if not form_list or len(form_list) < 2:
            return "unknown"
        
        recent = form_list[-2:]
        previous = form_list[:-2] if len(form_list) > 2 else form_list[:1]
        
        recent_avg = sum(recent) / len(recent)
        previous_avg = sum(previous) / len(previous)
        
        if recent_avg < previous_avg - 0.5:
            return "improving"
        elif recent_avg > previous_avg + 0.5:
            return "declining"
        else:
            return "stable"
    
    def _calculate_variance(self, data):
        """Calculate variance as a measure of consistency."""
        if len(data) < 2:
            return 0
        
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        return variance
    
    def _extract_key_factors(self, runner):
        """Extract key performance factors from runner data."""
        factors = []
        
        if runner.get('rating', 0) > 80:
            factors.append("High rating")
        
        if runner.get('form', 50) > 75:
            factors.append("Strong recent form")
        
        if runner.get('draw') and runner.get('draw') <= 2:
            factors.append("Favorable draw")
        
        return factors if factors else ["Average prospects"]
