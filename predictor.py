import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RacePredictor:
    """Enhanced race predictor with multi-factor analysis and confidence scoring."""
    
    def __init__(self):
        self.model_version = "CardPredictor-v2.0"
        self.analysis_factors = {
            'rating': 0.35,
            'form': 0.30,
            'draw': 0.15,
            'jockey_trainer': 0.10,
            'going_fit': 0.10
        }
    
    def calculate_probabilities(self, runners):
        """
        Compute probability-based analysis with confidence scoring.
        
        Args:
            runners: List of runner objects with attributes (rating, form, draw, etc.)
        
        Returns:
            List of predictions with probabilities and confidence intervals
        """
        total_score = 0
        scored_runners = []
        
        for r in runners:
            score = self._calculate_composite_score(r)
            total_score += score
            scored_runners.append({
                "name": r.get("name"),
                "raw_score": score,
                "rating": r.get("rating", 50),
                "form": r.get("form", 50),
                "draw": r.get("draw", 5)
            })
        
        # Normalize to percentages
        predictions = []
        for r in sorted(scored_runners, key=lambda x: x["raw_score"], reverse=True):
            win_prob = (r["raw_score"] / total_score * 100) if total_score > 0 else 0
            
            # Calculate confidence interval
            confidence = self._calculate_confidence(r, total_score)
            
            # Determine recommendation tier
            recommendation = self._get_recommendation(win_prob, confidence)
            
            predictions.append({
                "runner": r["name"],
                "win_probability": f"{win_prob:.1f}%",
                "win_probability_raw": round(win_prob, 1),
                "confidence_score": f"{confidence:.2f}",
                "confidence_raw": round(confidence, 2),
                "recommendation": recommendation,
                "rating_contribution": f"{(r['rating'] / 100 * 35):.1f}%",
                "form_contribution": f"{(r['form'] / 100 * 30):.1f}%",
                "analysis_timestamp": datetime.utcnow().isoformat()
            })
        
        return predictions
    
    def _calculate_composite_score(self, runner):
        """
        Calculate weighted composite score from multiple factors.
        """
        rating = runner.get("rating", 50)
        form = runner.get("form", 50)
        draw = runner.get("draw", 5)
        
        # Draw factor (lower draw generally better, max 8 possible)
        draw_factor = max(1, 10 - draw)
        
        # Weighted calculation
        composite = (
            (rating * self.analysis_factors['rating']) +
            (form * self.analysis_factors['form']) +
            (draw_factor * self.analysis_factors['draw'] * 10) +
            (random.uniform(1, 5) * (self.analysis_factors['jockey_trainer'] + self.analysis_factors['going_fit']))
        )
        
        return composite
    
    def _calculate_confidence(self, runner, total_score):
        """
        Calculate confidence score (0-1) based on data consistency.
        """
        rating = runner.get("rating", 50)
        form = runner.get("form", 50)
        
        # Consistency check: rating and form alignment
        alignment = 1 - (abs(rating - form) / 100)  # 0 to 1
        
        # Factor in sample size and variance
        base_confidence = (alignment + 0.5) / 2  # Normalize between 0.25 and 1.0
        
        return base_confidence
    
    def _get_recommendation(self, win_prob, confidence):
        """
        Get recommendation tier based on probability and confidence.
        """
        if win_prob > 25 and confidence > 0.7:
            return "Strong Pick"
        elif win_prob > 20 and confidence > 0.6:
            return "Solid Pick"
        elif win_prob > 15 and confidence > 0.5:
            return "Consider"
        elif win_prob > 10:
            return "Outside Chance"
        else:
            return "Monitor"
    
    def get_live_predictions(self):
        """
        Placeholder for fetching live predictions.
        """
        return {
            "status": "active",
            "timestamp": datetime.utcnow().isoformat(),
            "model_version": self.model_version,
            "data_source": "live_stream"
        }
    
    def predict_future_performance(self, runner_id, historical_data, lookahead_days=7):
        """
        Forecast future performance based on historical patterns.
        
        Args:
            runner_id: Identifier for the runner
            historical_data: List of past performance scores
            lookahead_days: Number of days to forecast
        
        Returns:
            Performance forecast with trend indicators
        """
        if not historical_data or len(historical_data) < 3:
            return {
                'forecast': 'Insufficient historical data',
                'lookahead_days': lookahead_days,
                'status': 'pending'
            }
        
        # Simple linear trend analysis
        trend = self._calculate_trend(historical_data)
        
        # Project forward
        last_value = historical_data[-1]
        forecasted_values = []
        
        for day in range(1, lookahead_days + 1):
            projected = last_value + (trend * day)
            forecasted_values.append(round(max(0, min(100, projected)), 2))
        
        return {
            'runner_id': runner_id,
            'historical_avg': round(sum(historical_data) / len(historical_data), 2),
            'trend_direction': 'improving' if trend > 0.5 else 'declining' if trend < -0.5 else 'stable',
            'trend_magnitude': round(abs(trend), 2),
            'forecast': forecasted_values,
            'forecast_range': [min(forecasted_values), max(forecasted_values)],
            'confidence': round(min(len(historical_data) / 10, 1.0), 2),
            'generated_at': datetime.utcnow().isoformat()
        }
    
    def _calculate_trend(self, data):
        """
        Calculate trend using simple linear regression.
        """
        if len(data) < 2:
            return 0
        
        n = len(data)
        x_sum = sum(range(n))
        y_sum = sum(data)
        xy_sum = sum(i * data[i] for i in range(n))
        x2_sum = sum(i ** 2 for i in range(n))
        
        numerator = (n * xy_sum) - (x_sum * y_sum)
        denominator = (n * x2_sum) - (x_sum ** 2)
        
        slope = numerator / denominator if denominator != 0 else 0
        return slope
