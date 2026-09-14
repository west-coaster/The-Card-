import React, { useEffect, useState } from 'react';
import { supabase } from './supabase';
import { RealtimeService } from './services/realtimeService';
import { AuthService } from './services/authService';
import './App.css';

const App = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [predictions, setPredictions] = useState([]);
  const [liveUpdates, setLiveUpdates] = useState(null);

  const authService = new AuthService(supabase);
  const realtimeService = new RealtimeService(supabase);

  // Initialize auth and subscriptions
  useEffect(() => {
    checkAuth();
  }, []);

  // Subscribe to real-time updates
  useEffect(() => {
    if (user) {
      subscribeToUpdates();
      subscribeToNotifications();
    }
  }, [user]);

  const checkAuth = async () => {
    const session = await authService.getSession();
    setUser(session?.user || null);
    setLoading(false);
  };

  const subscribeToUpdates = async () => {
    // Subscribe to predictions for this user
    const subscription = supabase
      .from(`predictions:user_id=eq.${user.id}`)
      .on('*', (payload) => {
        console.log('Prediction update:', payload);
        // Refetch predictions
        fetchPredictions();
      })
      .subscribe();

    return subscription;
  };

  const subscribeToNotifications = async () => {
    // Listen for broadcast messages (server push notifications)
    const subscription = supabase
      .channel('updates')
      .on('broadcast', { event: 'new_data' }, (payload) => {
        console.log('Server push notification:', payload);
        setLiveUpdates(payload.data);
        fetchPredictions();
      })
      .subscribe();

    return subscription;
  };

  const fetchPredictions = async () => {
    const { data, error } = await supabase
      .from('predictions')
      .select('*')
      .eq('user_id', user.id)
      .order('created_at', { ascending: false });

    if (!error) {
      setPredictions(data);
    }
  };

  const handleSignOut = async () => {
    await authService.signOut();
    setUser(null);
    setPredictions([]);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return <LoginScreen onAuth={checkAuth} />;
  }

  return (
    <div className="app-container">
      <Header user={user} onSignOut={handleSignOut} />
      <main className="app-main">
        {liveUpdates && (
          <div className="live-notification">
            <span className="pulse">🔴 Live Update</span>
            <p>{liveUpdates.message}</p>
          </div>
        )}
        <PredictionsGrid predictions={predictions} />
      </main>
    </div>
  );
};

const Header = ({ user, onSignOut }) => (
  <header className="app-header">
    <div className="header-left">
      <h1>THE CARD</h1>
      <p className="user-info">Welcome, {user.email}</p>
    </div>
    <button onClick={onSignOut} className="btn-signout">
      Sign Out
    </button>
  </header>
);

const LoginScreen = ({ onAuth }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);

  const handleAuth = async (e) => {
    e.preventDefault();
    const authService = new AuthService(supabase);

    try {
      if (isSignUp) {
        await authService.signUp(email, password);
      } else {
        await authService.signIn(email, password);
      }
      onAuth();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-screen">
      <div className="login-card">
        <h1>THE CARD</h1>
        <p className="tagline">Sports Analytics & Predictions</p>
        <form onSubmit={handleAuth}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {error && <p className="error">{error}</p>}
          <button type="submit" className="btn-primary">
            {isSignUp ? 'Sign Up' : 'Sign In'}
          </button>
        </form>
        <button
          type="button"
          className="btn-link"
          onClick={() => setIsSignUp(!isSignUp)}
        >
          {isSignUp ? 'Already have an account?' : 'Create account'}
        </button>
      </div>
    </div>
  );
};

const PredictionsGrid = ({ predictions }) => {
  if (predictions.length === 0) {
    return (
      <div className="empty-state">
        <p>No predictions yet</p>
      </div>
    );
  }

  return (
    <div className="predictions-grid">
      {predictions.map((pred) => (
        <div key={pred.id} className="prediction-card">
          <h3>{pred.runner_name}</h3>
          <div className="prediction-stats">
            <div className="stat">
              <span className="label">Win Probability</span>
              <span className="value">{pred.win_probability}%</span>
            </div>
            <div className="stat">
              <span className="label">Confidence</span>
              <span className="value">{(pred.confidence_score * 100).toFixed(1)}%</span>
            </div>
            <div className="stat">
              <span className="label">Recommendation</span>
              <span className="value">{pred.recommendation || 'Monitor'}</span>
            </div>
          </div>
          <p className="timestamp">
            {new Date(pred.created_at).toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  );
};

export default App;
