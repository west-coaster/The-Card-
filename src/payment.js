// Payment Portal Module
import { STRIPE_PUBLIC_KEY, PRICING_PLANS } from './config.js';
import { authManager } from './auth.js';

class PaymentManager {
  constructor() {
    this.stripe = null;
    this.selectedPlan = null;
    this.initStripe();
  }

  async initStripe() {
    // Dynamically load Stripe
    if (!window.Stripe) {
      const script = document.createElement('script');
      script.src = 'https://js.stripe.com/v3/';
      script.onload = () => {
        this.stripe = window.Stripe(STRIPE_PUBLIC_KEY);
      };
      document.head.appendChild(script);
    } else {
      this.stripe = window.Stripe(STRIPE_PUBLIC_KEY);
    }
  }

  async selectPlan(planKey) {
    this.selectedPlan = PRICING_PLANS[planKey];
    
    // If free plan, just update subscription
    if (planKey === 'free') {
      return await this.upgradePlan('free');
    }

    // For paid plans, redirect to Stripe checkout
    if (this.stripe) {
      const session = await this.createCheckoutSession(planKey);
      if (session.sessionId) {
        await this.stripe.redirectToCheckout({ sessionId: session.sessionId });
      }
    }
  }

  async createCheckoutSession(planKey) {
    const user = authManager.getCurrentUser();
    if (!user) {
      return { success: false, error: 'User not authenticated' };
    }

    try {
      const response = await fetch('/api/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authManager.session?.access_token}`
        },
        body: JSON.stringify({
          planKey,
          userId: user.id,
          email: user.email
        })
      });

      const data = await response.json();
      return data;
    } catch (err) {
      console.error('Failed to create checkout session:', err);
      return { success: false, error: err.message };
    }
  }

  async upgradePlan(planKey) {
    const result = await authManager.updateSubscription(planKey);
    
    if (result.success) {
      return {
        success: true,
        message: `Successfully upgraded to ${PRICING_PLANS[planKey].name}`,
        profile: result.profile
      };
    } else {
      return {
        success: false,
        error: result.error
      };
    }
  }

  getPricingPlans() {
    return PRICING_PLANS;
  }
}

export const paymentManager = new PaymentManager();
