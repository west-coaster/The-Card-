# THE CARD — GitHub Pages + Supabase Edition

![Version](https://img.shields.io/badge/version-2.0-blue)
![Platform](https://img.shields.io/badge/platform-GitHub%20Pages%20%2B%20Supabase-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Downloads](https://img.shields.io/badge/downloads-2.5K+-blue)

**The Card** is a downloadable desktop app and web application providing real-time sports analytics, AI-powered predictions, and performance forecasting.

🚀 **Live Demo:** https://devforge-os1.github.io/Bokke-Vs-New-Zeeland  
📥 **Download App:** See [Releases](https://github.com/devforge-os1/Bokke-Vs-New-Zeeland/releases)  
📖 **Documentation:** https://devforge-os1.github.io/Bokke-Vs-New-Zeeland/docs

## ✨ Features

### 🎯 Smart Analytics
- **Real-Time Streaming** — WebSocket updates every 5 seconds
- **AI Predictions** — Multi-factor confidence scoring
- **Performance Forecasting** — 7-day outlook with trend analysis
- **Sentiment Analysis** — Automated insights from historical data
- **Form Tracking** — Consistency scoring and trend detection

### 💻 Cross-Platform
- **Web App** — Works in all modern browsers (GitHub Pages)
- **Desktop App** — Electron-based app for Windows, macOS, Linux
- **Offline Mode** — View cached data without internet
- **Responsive Design** — Mobile-optimized interface

### 🔐 Secure & Scalable
- **Supabase Auth** — Built-in user authentication
- **PostgreSQL Database** — Reliable data persistence
- **JWT Tokens** — Secure API communication
- **Real-Time Updates** — PostgreSQL LISTEN/NOTIFY

### 📱 Desktop Application
- Built with Electron
- Native OS integration
- System tray support
- Push notifications
- Auto-updates

## 🚀 Quick Start

### Web App (GitHub Pages)

Visit: https://devforge-os1.github.io/Bokke-Vs-New-Zeeland

1. Sign up with email/password
2. Select subscription tier
3. View real-time analytics

### Desktop App

**Download:**
- [Windows](https://github.com/devforge-os1/Bokke-Vs-New-Zeeland/releases/download/v2.0/TheCard-Setup-2.0.exe)
- [macOS](https://github.com/devforge-os1/Bokke-Vs-New-Zeeland/releases/download/v2.0/TheCard-2.0.dmg)
- [Linux](https://github.com/devforge-os1/Bokke-Vs-New-Zeeland/releases/download/v2.0/the-card-2.0.AppImage)

**Installation:**

*Windows:*
```bash
# Run installer
TheCard-Setup-2.0.exe

# Or install via Chocolatey
choco install the-card
```

*macOS:*
```bash
# Mount DMG and drag to Applications
open TheCard-2.0.dmg

# Or install via Homebrew
brew install the-card
```

*Linux:*
```bash
# Make executable and run
chmod +x the-card-2.0.AppImage
./the-card-2.0.AppImage

# Or install via snap
sudo snap install the-card
```

## 🔧 Architecture

```
┌─────────────────────────────────────┐
│   GitHub Pages (Static Frontend)    │
│         index.html + CSS/JS         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Electron Desktop App           │
│   (Windows/macOS/Linux binary)      │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
┌─────────────┐    ┌──────────────┐
│  Supabase   │    │  Real-time   │
│  Auth/DB    │    │  WebSocket   │
└─────────────┘    └──────────────┘
```

## 📋 Setup Instructions

### Prerequisites
- GitHub account (for Pages hosting)
- Supabase account (free tier available)
- Node.js 16+ (for desktop app development)

### 1. Fork Repository

```bash
git clone https://github.com/devforge-os1/Bokke-Vs-New-Zeeland.git
cd Bokke-Vs-New-Zeeland
git remote add origin YOUR_FORK_URL
git push -u origin main
```

### 2. Configure GitHub Pages

1. Go to **Settings → Pages**
2. Set **Source** to `gh-pages` branch
3. Custom domain (optional): `thecard.yoursite.com`
4. Enable HTTPS

### 3. Setup Supabase

**Create Supabase Project:**

```bash
# 1. Go to https://supabase.com
# 2. Create new project
# 3. Get credentials from Settings → API

SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
```

**Initialize Database:**

```sql
-- Auth tables are auto-created by Supabase
-- Create custom tables:

CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  email TEXT UNIQUE,
  subscription_tier TEXT DEFAULT 'basic',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  event_name TEXT,
  event_data JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  runner_name TEXT,
  win_probability DECIMAL,
  confidence_score DECIMAL,
  forecast JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Add RLS policies
CREATE POLICY "Users can view own data" ON users
  USING (auth.uid() = id);
```

### 4. Create Configuration File

**`src/config.js`:**

```javascript
export const SUPABASE_URL = 'https://xxxxx.supabase.co';
export const SUPABASE_KEY = 'eyJhbGc...';
export const API_ENDPOINT = 'https://api.thecard.io';
export const WS_ENDPOINT = 'wss://api.thecard.io';
```

### 5. Deploy to GitHub Pages

```bash
# Build static files
npm run build

# Deploy to gh-pages branch
gh-pages -d dist
```

### 6. Build Desktop App (Optional)

```bash
# Install dependencies
cd electron
npm install

# Build for all platforms
npm run build:all

# Outputs to dist/
```

## 📦 File Structure

```
Bokke-Vs-New-Zeeland/
├── index.html              # Main web interface
├── src/
│   ├── app.js             # Main application
│   ├── auth.js            # Supabase auth
│   ├── api.js             # API client
│   ├── ui.js              # UI components
│   └── config.js          # Configuration
├── electron/              # Desktop app
│   ├── main.js            # Electron main process
│   ├── preload.js         # IPC bridge
│   └── package.json       # App metadata
├── dist/                  # Compiled static files
├── deploy/                # Deployment configs
└── docs/                  # Documentation
```

## 🔌 Supabase Integration

### Authentication

```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Sign up
const { user, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'SecurePassword123'
});

// Sign in
const { user, error } = await supabase.auth.signIn({
  email: 'user@example.com',
  password: 'SecurePassword123'
});

// Get session
const session = await supabase.auth.session();
```

### Real-Time Updates

```javascript
// Subscribe to predictions
const subscription = supabase
  .from('predictions')
  .on('*', payload => {
    console.log('Prediction update:', payload);
  })
  .subscribe();

// Unsubscribe
supabase.removeSubscription(subscription);
```

### Database Operations

```javascript
// Create prediction
const { data, error } = await supabase
  .from('predictions')
  .insert([{
    runner_name: 'Runner Name',
    win_probability: 32.5,
    confidence_score: 0.87
  }]);

// Read predictions
const { data, error } = await supabase
  .from('predictions')
  .select('*')
  .eq('user_id', userId);

// Update
const { data, error } = await supabase
  .from('predictions')
  .update({ confidence_score: 0.90 })
  .eq('id', predictionId);
```

## 🎯 Deployment Workflow

```bash
# 1. Development
git checkout -b feature/your-feature
npm run dev

# 2. Test
npm run test
npm run lint

# 3. Build
npm run build

# 4. Commit & Push
git add .
git commit -m "feat: add feature"
git push origin feature/your-feature

# 5. Create Pull Request
# → GitHub automatically deploys preview to GitHub Pages

# 6. Merge to main
# → Automatic deployment to production
```

## 📊 Performance

- **Page Load:** <1 second (cached)
- **API Response:** <200ms
- **Real-time Updates:** <500ms
- **Bundle Size:** 245KB (gzipped)

## 🔐 Security

- Supabase Row Level Security (RLS)
- JWT token validation
- HTTPS/TLS encryption
- No sensitive data in local storage
- Environment variable protection

## 📱 Desktop App Features

- System tray integration
- Push notifications
- Keyboard shortcuts
- Auto-update checking
- Offline data viewing
- Native file system access

## 🐛 Troubleshooting

### App won't start
```bash
# Clear cache
rm -rf ~/.config/TheCard/
rm -rf ~/AppData/Local/TheCard/  # Windows
rm -rf ~/Library/Application\ Support/TheCard/  # macOS
```

### Authentication issues
```bash
# Clear stored tokens
localStorage.clear();
sessionStorage.clear();
```

### Database connection errors
```bash
# Verify Supabase credentials
# Check SUPABASE_URL and SUPABASE_KEY in config.js
```

## 📖 Documentation

- [API Reference](./docs/api.md)
- [WebSocket Events](./docs/websocket.md)
- [Supabase Setup](./docs/supabase.md)
- [Desktop App Guide](./docs/electron.md)
- [Deployment Guide](./DEPLOYMENT.md)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

Contributions welcome! Please follow our [Code of Conduct](./CODE_OF_CONDUCT.md).

## 📄 License

MIT License — See [LICENSE](./LICENSE) file

## 🙏 Support

- **Issues:** [GitHub Issues](https://github.com/devforge-os1/Bokke-Vs-New-Zeeland/issues)
- **Discussions:** [GitHub Discussions](https://github.com/devforge-os1/Bokke-Vs-New-Zeeland/discussions)
- **Email:** support@thecard.io
- **Documentation:** https://docs.thecard.io

---

**Built with ❤️ by DevForge OS**

⭐ If you find this useful, please star the repository!
