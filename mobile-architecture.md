# Mobile App Architecture

## Overview

**THE CARD Mobile App** is a cross-platform mobile application (iOS/Android) built with React Native + Expo.

Key features:
- ✅ Real-time data streaming
- ✅ Server push notifications
- ✅ Offline support
- ✅ Native performance
- ✅ WebSocket real-time updates

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│     Mobile App (iOS/Android - React Native/Expo)        │
│  ┌─────────────────────────────────────────────────┐    │
│  │  UI Layer (React Components)                    │    │
│  │  - Login Screen                                 │    │
│  │  - Predictions Dashboard                        │    │
│  │  - Real-time Updates Display                    │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    │                                     │
│  ┌─────────────────▼───────────────────────────────┐    │
│  │  Services Layer                                 │    │
│  │  - AuthService (Supabase)                       │    │
│  │  - RealtimeService (WebSocket + DB)            │    │
│  │  - APIService (HTTP)                            │    │
│  │  - StorageService (AsyncStorage)                │    │
│  └─────────────────┬───────────────────────────────┘    │
│                    │                                     │
└────────────────────┼─────────────────────────────────────┘
                     │ (HTTPS + WebSocket)
                     │
         ┌───────────┴──────────┐
         │                      │
    ┌────▼─────────┐     ┌──────▼──────────┐
    │  Supabase    │     │  Backend API   │
    │  ┌────────┐  │     │  ┌──────────┐  │
    │  │ Auth   │  │     │  │ /api/... │  │
    │  ├────────┤  │     │  ├──────────┤  │
    │  │ Realtime   │  │ │ WebSocket  │  │
    │  ├────────┤  │     │  ├──────────┤  │
    │  │Database   │  │ │ Broadcast  │  │
    │  └────────┘  │     │  └──────────┘  │
    └──────────────┘     └─────────────────┘
         (PostgreSQL)
```

## Single API Endpoint + Server Broadcast Pattern

### Flow:

```
1. Mobile App Calls Single API
   ↓
   POST /api/predictions
   {
     "predictions": [...],
     "timestamp": "2026-09-13T..."
   }

2. Server Updates Database
   ↓
   INSERT INTO predictions VALUES (...)

3. Server Broadcasts to ALL Connected Users
   ├─ WebSocket emit (real-time)
   ├─ Supabase broadcast (database subscribers)
   └─ Push notifications (offline users)

4. All Clients Receive Update
   ├─ Connected users: instant
   ├─ Database subscribers: automatic
   └─ Offline users: next connect
```

### Example API Call:

```javascript
// Mobile app makes ONE API call
const apiService = new APIService(API_URL);

await apiService.updatePredictions([
  {
    id: 'pred_123',
    runner_name: 'Runner Name',
    win_probability: 45.5,
    confidence_score: 0.87
  }
]);

// Server response:
// {
//   "status": "success",
//   "message": "Updated 1 predictions and broadcasted to all users",
//   "updated_count": 1,
//   "timestamp": "2026-09-13T..."
// }

// ALL OTHER USERS automatically receive update via:
// 1. WebSocket: 'predictions_update' event
// 2. Supabase: table subscription
// 3. Real-time database listener
```

## Setup Instructions

### Prerequisites

- Node.js 16+
- Expo CLI
- EAS CLI (for building)
- Supabase account
- Backend server running

### Installation

```bash
# Install dependencies
cd mobile
npm install

# Install Expo CLI globally
npm install -g expo-cli eas-cli

# Start development server
npm start

# Scan QR code with Expo Go app
```

### Configuration

**`mobile/config.js`:**

```javascript
export const CONFIG = {
  SUPABASE_URL: process.env.EXPO_PUBLIC_SUPABASE_URL,
  SUPABASE_KEY: process.env.EXPO_PUBLIC_SUPABASE_KEY,
  API_URL: process.env.EXPO_PUBLIC_API_URL,
  WS_URL: process.env.EXPO_PUBLIC_WS_URL
};
```

**`.env`:**

```
EXPO_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
EXPO_PUBLIC_SUPABASE_KEY=eyJhbGc...
EXPO_PUBLIC_API_URL=https://api.thecard.io
EXPO_PUBLIC_WS_URL=wss://api.thecard.io
```

### Build for iOS

```bash
# Create iOS build
npm run build:ios

# Or use Testflight
npm run publish:testflight
```

### Build for Android

```bash
# Create Android build
npm run build:android

# Or use Google Play
npm run publish:play
```

## Real-Time Features

### 1. Live Predictions Update

When server pushes new predictions:

```javascript
// Backend broadcasts
socketio.emit('predictions_update', data, broadcast=True)

// Mobile app receives via:
this.realtimeService.subscribeToPredictions(userId, (update) => {
  // Predictions automatically updated
  setPredictions(update.data);
});
```

### 2. Instant Notifications

```javascript
// Server push notification
socketio.emit('notification', {
  type: 'new_prediction',
  title: 'New Analysis Available',
  body: 'Latest predictions updated'
}, broadcast=True)

// Mobile app receives and displays
const notificationService = new NotificationService();
notificationService.showPushNotification(notification);
```

### 3. Offline Support

```javascript
// Store data locally
await AsyncStorage.setItem('predictions', JSON.stringify(predictions));

// Retrieve when offline
const cached = await AsyncStorage.getItem('predictions');

// Sync when online
NetInfo.addEventListener(state => {
  if (state.isConnected) {
    syncWithServer();
  }
});
```

## File Structure

```
mobile/
├── src/
│   ├── App.jsx                      # Main app component
│   ├── screens/
│   │   ├── LoginScreen.jsx
│   │   ├── DashboardScreen.jsx
│   │   └── DetailsScreen.jsx
│   ├── components/
│   │   ├── PredictionCard.jsx
│   │   ├── UpdateNotification.jsx
│   │   └── LoadingSpinner.jsx
│   ├── services/
│   │   ├── authService.js
│   │   ├── realtimeService.js
│   │   ├── apiService.js
│   │   ├── storageService.js
│   │   └── notificationService.js
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── usePredictions.js
│   │   └── useNetworkStatus.js
│   ├── config.js
│   └── supabase.js
├── app.json                         # Expo config
├── eas.json                         # EAS build config
├── package.json
└── .env.example
```

## Performance Optimization

- Lazy loading of predictions
- Memoization of components
- Optimized re-renders
- Image caching
- Database query optimization

## Testing

```bash
# Run tests
npm test

# Run with coverage
npm test -- --coverage

# E2E testing
npm run e2e
```

## Distribution

### iOS
- TestFlight (beta testing)
- App Store (production)

### Android
- Google Play Beta
- Google Play (production)
- APK direct download

---

**Mobile app ready for download! 📱**
