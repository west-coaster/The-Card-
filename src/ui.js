// UI Manager Module
import { authManager } from './auth.js';
import { paymentManager } from './payment.js';
import { PRICING_PLANS } from './config.js';

class UIManager {
  constructor() {
    this.currentView = 'auth';
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Auth buttons
    const signupBtn = document.getElementById('signup-btn');
    const signinBtn = document.getElementById('signin-btn');
    const logoutBtn = document.getElementById('logout-btn');

    if (signupBtn) {
      signupBtn.addEventListener('click', () => this.handleSignUp());
    }
    if (signinBtn) {
      signinBtn.addEventListener('click', () => this.handleSignIn());
    }
    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => this.handleLogout());
    }

    // Skip payment
    const skipPaymentBtn = document.getElementById('skip-payment-btn');
    if (skipPaymentBtn) {
      skipPaymentBtn.addEventListener('click', () => this.skipPayment());
    }
  }

  async handleSignUp() {
    const email = document.getElementById('email')?.value;
    const password = document.getElementById('password')?.value;
    const errorDiv = document.getElementById('auth-error');

    if (!email || !password) {
      this.showError(errorDiv, 'Please enter email and password');
      return;
    }

    if (password.length < 6) {
      this.showError(errorDiv, 'Password must be at least 6 characters');
      return;
    }

    const result = await authManager.signUp(email, password);
    if (result.success) {
      this.showPaymentPortal();
    } else {
      this.showError(errorDiv, result.error);
    }
  }

  async handleSignIn() {
    const email = document.getElementById('email')?.value;
    const password = document.getElementById('password')?.value;
    const errorDiv = document.getElementById('auth-error');

    if (!email || !password) {
      this.showError(errorDiv, 'Please enter email and password');
      return;
    }

    const result = await authManager.signIn(email, password);
    if (result.success) {
      this.showDashboard();
    } else {
      this.showError(errorDiv, result.error);
    }
  }

  async handleLogout() {
    await authManager.signOut();
    this.showAuthSection();
  }

  showError(element, message) {
    if (element) {
      element.textContent = message;
      element.classList.remove('hidden');
    }
  }

  showAuthSection() {
    this.hideAllSections();
    document.getElementById('auth-section')?.classList.remove('hidden');
    this.currentView = 'auth';
  }

  showPaymentPortal() {
    this.hideAllSections();
    document.getElementById('payment-section')?.classList.remove('hidden');
    this.renderPricingCards();
    this.currentView = 'payment';
  }

  showDashboard() {
    this.hideAllSections();
    document.getElementById('dashboard-section')?.classList.remove('hidden');
    this.currentView = 'dashboard';
    this.loadDashboardData();
  }

  hideAllSections() {
    document.getElementById('auth-section')?.classList.add('hidden');
    document.getElementById('payment-section')?.classList.add('hidden');
    document.getElementById('dashboard-section')?.classList.add('hidden');
  }

  renderPricingCards() {
    const plans = paymentManager.getPricingPlans();
    // Cards are static in HTML, just ensure they're visible
  }

  async loadDashboardData() {
    const profile = await authManager.getUserProfile();
    if (profile) {
      const subscription = document.getElementById('current-subscription');
      if (subscription) {
        subscription.textContent = `${profile.subscription_tier.charAt(0).toUpperCase() + profile.subscription_tier.slice(1)} Plan`;
      }
    }

    // Load analytics data
    this.updateAnalytics();
  }

  updateAnalytics() {
    // Simulated data - replace with real API calls
    document.getElementById('active-events').textContent = '12';
    document.getElementById('total-predictions').textContent = '247';
    document.getElementById('avg-confidence').textContent = '87%';
    document.getElementById('win-rate').textContent = '62%';
  }

  async skipPayment() {
    await paymentManager.upgradePlan('free');
    this.showDashboard();
  }

  showDashboardView(viewName) {
    // Hide all views
    document.querySelectorAll('.view').forEach(view => {
      view.classList.add('hidden');
    });

    // Show selected view
    const viewId = `${viewName}-view`;
    const viewElement = document.getElementById(viewId);
    if (viewElement) {
      viewElement.classList.remove('hidden');
    }
  }
}

export const uiManager = new UIManager();

// Make functions globally available
window.selectPlan = (plan) => paymentManager.selectPlan(plan);
window.showDashboard = (view) => uiManager.showDashboardView(view);
window.showPaymentPortal = () => uiManager.showPaymentPortal();
