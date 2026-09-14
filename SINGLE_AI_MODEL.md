# THE CARD - Single AI Model Architecture

## Overview

**ONE AI MODEL** is responsible for:
1. ✅ Fetching all data from external APIs
2. ✅ Processing & analyzing data
3. ✅ Generating predictions
4. ✅ Pushing to Supabase server
5. ✅ Supabase distributes to ALL users

No other processing. Everything flows through this single AI model.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    External Data Sources                     │
│  (Race APIs, Market Data, Weather, Historical Records)      │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
          ┌────────────────────────────┐
          │   SINGLE AI MODEL          │
          │  ==================        │
          │                            │
          │  1. Fetch Data             │
          │  2. Process & Analyze      │
          │  3. Generate Predictions   │
          │  4. Push to Supabase       │
          │                            │
          └────────────┬───────────────┘
                       │
                       ▼
          ┌────────────────────────────┐
          │    Supabase Server         │
          │  ==================        │
          │  - PostgreSQL DB           │
          │  - Real-time Updates       │
          │  - Authentication          │
          │  - Row Level Security      │
          └────────────┬───────────────┘
                       │
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ Mobile  │  │   Web   │  │ Desktop │
    │  App    │  │   App   │  │  App    │
    │ (iOS)   │  │ (Pages) │  │(Electron)│
    └─────────┘  └─────────┘  └─────────┘
    
    User 1       User 2       User 3
    (Real-time sync from Supabase)
```

## Setup Instructions

### 1. Create Supabase Project

Visit: https://supabase.com

1. Create new project
2. Get credentials:
   ```
   SUPABASE_URL = https://xxxxx.supabase.co
   SUPABASE_KEY = eyJhbGc...
   ```

### 2. Run Database Setup

Go to **SQL Editor** → paste this:

```sql
-- Main predictions table
CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  runner_name TEXT NOT NULL,
  win_probability DECIMAL(5, 2),
  confidence_score DECIMAL(3, 2),
  recommendation TEXT,
  analysis JSONB,
  forecast JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Events table
CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type TEXT,
  event_name TEXT,
  event_data JSONB,
  track_id TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Forecasts table
CREATE TABLE forecasts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  runner_id TEXT,
  lookahead_days INT DEFAULT 7,
  trend_direction TEXT,
  forecast_values DECIMAL[],
  confidence DECIMAL(3, 2),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable real-time
ALTER TABLE predictions REPLICA IDENTITY FULL;
ALTER TABLE events REPLICA IDENTITY FULL;
ALTER TABLE forecasts REPLICA IDENTITY FULL;
```

### 3. Configure AI Model

Set environment variables:

```bash
# .env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
AI_MODEL_API_KEY=your-api-key
DATA_FETCH_INTERVAL=300  # 5 minutes
```

### 4. Run AI Model

```bash
python ai_orchestrator.py
```

That's it! The AI model will:
- Fetch data every 5 minutes
- Process it
- Push to Supabase
- All users get updates via Supabase real-time

## How It Works

### Flow:

```
1. AI Model wakes up every 5 minutes
2. Fetches data from external APIs
3. Runs analysis & predictions
4. Pushes results to Supabase
5. Supabase triggers real-time broadcast
6. All connected users get update INSTANTLY
7. Mobile/Web/Desktop apps display new data
```

### Example:

```python
# AI Model Loop (ai_orchestrator.py)

while True:
    # 1. FETCH DATA
    data = fetch_from_apis()
    
    # 2. ANALYZE
    predictions = ai_model.predict(data)
    
    # 3. PUSH TO SUPABASE
    supabase.table('predictions').insert(predictions).execute()
    
    # 4. SUPABASE BROADCASTS TO USERS
    # (automatic via real-time subscription)
    
    # Wait 5 minutes
    time.sleep(300)
```

## Client Subscription

All apps subscribe to Supabase:

```javascript
// Web/Mobile apps
supabase
  .from('predictions')
  .on('*', payload => {
    console.log('New data from AI model:', payload);
    updateUI(payload.new);
  })
  .subscribe();
```

## Files Needed

- ✅ `ai_orchestrator.py` — Main AI model
- ✅ `ai_model.py` — ML/prediction logic
- ✅ `data_fetcher.py` — External API integrations
- ✅ `supabase_pusher.py` — Push to Supabase
- ✅ `.env` — Configuration

That's all!

---

**Summary:** ONE AI model fetches → processes → pushes to Supabase → Supabase broadcasts to ALL users! 🚀
