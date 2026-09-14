import React, { useEffect, useState } from 'react';
import { supabase } from './supabase';
import './App.css';

const App = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [predictions, setPredictions] = useState([]);
  const [liveUpdates, setLiveUpdates] = useState(null);

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (user) {
      subscribeToUpdates();
      subscribeToNotifications();
      fetchPredictions();
    }
  }, [user]);

  const checkAuth = async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession();
      setUser(session?.user || null);
    } catch (error) {
      console.error('Auth check error:', error);
    } finally {
      setLoading(false);
    }
  };

  const subscribeToUpdates = async () => {
    if (!user?.id) return;
    
    const subscription = supabase
      .channel(`predictions:user_id=eq.${user.id}`)
      .on('postgres_changes', 
        { event: '*', schema: 'public', table: 'predictions', filter: `user_id=eq.${user.id}` },
        (payload) => {
          console.log('Prediction update:', payload);
          fetchPredictions();
        }
      )
      .subscribe();

    return subscription;
  };

  const subscribeToNotifications = async () => {
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
    if (!user?.id) return;
    
    try {
      const { data, error } = await supabase
        .from('predictions')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false });

      if (!error) {
        setPredictions(data || []);
      }
    } catch (error) {
      console.error('Error fetching predictions:', error);
    }
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
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
  const [loading, setLoading] = useState(false);

  const handleAuth = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (isSignUp) {
        const { error: signUpError } = await supabase.auth.signUp({
          email,
          password,
        });
        if (signUpError) throw signUpError;
      } else {
        const { error: signInError } = await supabase.auth.signInWithPassword({
          email,
          password,
        });
        if (signInError) throw signInError;
      }
      onAuth();
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
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
            disabled={loading}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
          {error && <p className="error">{error}</p>}
          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Loading...' : (isSignUp ? 'Sign Up' : 'Sign In')}
          </button>
        </form>
        <button
          type="button"
          className="btn-link"
          onClick={() => setIsSignUp(!isSignUp)}
          disabled={loading}
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
          <h3>{pred.runner_name || 'Prediction'}</h3>
          <div className="prediction-stats">
            <div className="stat">
              <span className="label">Win Probability</span>
              <span className="value">{pred.win_probability || 0}%</span>
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
