// Configuration for The Card application
export const SUPABASE_URL = 'https://your-supabase-url.supabase.co';
export const SUPABASE_ANON_KEY = 'your-anon-key-here';

export const STRIPE_PUBLIC_KEY = 'pk_test_your_stripe_key';

export const PRICING_PLANS = {
  free: {
    name: 'Free',
    price: 0,
    tier: 'basic',
    features: [
      'Basic analytics',
      '5 predictions/day',
      'Email support',
      'Mobile access'
    ]
  },
  pro: {
    name: 'Pro',
    price: 9.99,
    tier: 'pro',
    features: [
      'Real-time streaming (5s)',
      'Unlimited predictions',
      'AI confidence scoring',
      '7-day forecasting',
      'Priority support'
    ],
    stripeId: 'price_pro_monthly'
  },
  premium: {
    name: 'Premium',
    price: 19.99,
    tier: 'premium',
    features: [
      'Everything in Pro',
      'Advanced analytics',
      'Custom reports',
      'API access',
      '24/7 VIP support'
    ],
    stripeId: 'price_premium_monthly'
  }
};

export const API_ENDPOINT = 'https://api.thecard.io';
export const WS_ENDPOINT = 'wss://api.thecard.io/ws';
