# THE CARD - Single AI Model Quick Start

## What This Is

**ONE AI MODEL** handles everything:
1. Fetches data from APIs
2. Analyzes with AI
3. Generates predictions
4. Pushes to Supabase
5. Supabase broadcasts to users

That's it! Simple and clean.

## 30-Second Setup

### 1. Create Supabase Project
```
https://supabase.com → Create new project
Copy URL and API key
```

### 2. Setup Database

Go to **SQL Editor** in Supabase, paste:

```sql
CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  runner_name TEXT,
  win_probability DECIMAL(5, 2),
  confidence_score DECIMAL(3, 2),
  recommendation TEXT,
  analysis JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type TEXT,
  event_data JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE forecasts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  runner_id TEXT,
  forecast_values DECIMAL[],
  created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE predictions REPLICA IDENTITY FULL;
ALTER TABLE events REPLICA IDENTITY FULL;
ALTER TABLE forecasts REPLICA IDENTITY FULL;
```

### 3. Configure AI Model

Edit `.env`:
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
DATA_FETCH_INTERVAL=300
```

### 4. Run AI Model

```bash
# Setup
bash setup.sh

# Run
python ai_orchestrator.py
```

Done! ✅

## How It Works

```
AI Model Loop (every 5 minutes):

1. Fetch Data
   ├─ Race APIs
   ├─ Market data
   └─ Historical records
   ↓
2. AI Analysis
   ├─ Process features
   ├─ Calculate scores
   └─ Generate predictions
   ↓
3. Push to Supabase
   ├─ Insert predictions
   ├─ Insert events
   └─ Insert forecasts
   ↓
4. Supabase Real-time
   ├─ Broadcasts to all users
   ├─ Mobile app gets update
   ├─ Web app gets update
   └─ Desktop app gets update
```

## Monitoring

```bash
# View logs
tail -f logs/ai_model.log

# Check Supabase dashboard
https://supabase.com/dashboard

# View data
SUPABASE → Tables → predictions
```

## That's All!

Your system is now:
- ✅ Fetching data
- ✅ Running AI analysis
- ✅ Pushing to Supabase
- ✅ Broadcasting to users
- ✅ 100% automated

**Everything runs through that ONE AI model! 🎯**
