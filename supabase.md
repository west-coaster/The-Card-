# Supabase Setup Guide

## 1. Create Supabase Account

1. Go to https://supabase.com
2. Click "Start your project"
3. Sign up with GitHub or email
4. Create new organization
5. Create new project

## 2. Database Configuration

### Get API Keys

```
Settings → API
├── Project URL → SUPABASE_URL
├── anon (public) → SUPABASE_KEY
└── service_role → SECRET_KEY (keep private)
```

### Environment Variables

**`.env.local`:**
```
REACT_APP_SUPABASE_URL=https://xxxxx.supabase.co
REACT_APP_SUPABASE_KEY=eyJhbGc...
```

## 3. Create Database Tables

Go to **SQL Editor** and run:

```sql
-- Users table (links to auth.users)
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  subscription_tier TEXT DEFAULT 'basic',
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Predictions table
CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
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
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  event_type TEXT NOT NULL,
  event_name TEXT,
  event_data JSONB,
  track_id TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Forecasts table
CREATE TABLE forecasts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  runner_id TEXT NOT NULL,
  lookahead_days INT DEFAULT 7,
  trend_direction TEXT,
  forecast_values DECIMAL[],
  confidence DECIMAL(3, 2),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_predictions_user_id ON predictions(user_id);
CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_created_at ON events(created_at);
CREATE INDEX idx_forecasts_user_id ON forecasts(user_id);

-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE forecasts ENABLE ROW LEVEL SECURITY;

-- RLS Policies - Users can only see their own data
CREATE POLICY "Users can view own profile"
  ON users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Users can view own predictions"
  ON predictions FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own predictions"
  ON predictions FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own events"
  ON events FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create own events"
  ON events FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own forecasts"
  ON forecasts FOR SELECT
  USING (auth.uid() = user_id);

-- Create trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_predictions_updated_at BEFORE UPDATE ON predictions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## 4. Enable Authentication

Go to **Authentication → Providers**

Enable:
- [x] Email/Password
- [x] GitHub (optional)
- [x] Google (optional)

## 5. Configure Email Templates

Go to **Authentication → Email Templates**

Customize:
- Confirmation email
- Password reset email
- Magic link email

## 6. Setup Real-Time Updates

Go to **Database → Replication**

Enable replication for:
- `predictions`
- `events`
- `forecasts`

## 7. Configure Storage (Optional)

Go to **Storage → New bucket**

Create bucket: `user-avatars`

```sql
CREATE POLICY "Users can upload avatars"
  ON storage.objects FOR INSERT
  WITH CHECK (auth.uid() = owner);

CREATE POLICY "Public avatar access"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'user-avatars');
```

## 8. Test Connection

**`test-supabase.js`:**
```javascript
import { supabase } from './src/supabase.js';

// Test sign up
const { user, error } = await supabase.auth.signUp({
  email: 'test@example.com',
  password: 'TestPassword123'
});

if (error) {
  console.error('Sign up error:', error);
} else {
  console.log('Sign up successful:', user);
}

// Test database insert
const { data, error: insertError } = await supabase
  .from('predictions')
  .insert([{
    user_id: user.id,
    runner_name: 'Test Runner',
    win_probability: 50,
    confidence_score: 0.8
  }])
  .select();

if (insertError) {
  console.error('Insert error:', insertError);
} else {
  console.log('Insert successful:', data);
}
```

## 9. GitHub Pages Integration

**`.github/workflows/deploy.yml`:**
```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm run build
        env:
          REACT_APP_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          REACT_APP_SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

## 10. Add Secrets to GitHub

**Repository Settings → Secrets**

- `SUPABASE_URL`
- `SUPABASE_KEY`

---

✅ Database is now ready for THE CARD application!
