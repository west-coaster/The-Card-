// Authentication module using Supabase
import { SUPABASE_URL, SUPABASE_ANON_KEY } from './config.js';

class AuthManager {
  constructor() {
    this.user = null;
    this.session = null;
    this.supabaseClient = null;
    this.initSupabase();
  }

  async initSupabase() {
    // Dynamic import of Supabase
    const { createClient } = await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.38.4/+esm');
    this.supabaseClient = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    await this.restoreSession();
  }

  async restoreSession() {
    try {
      const { data } = await this.supabaseClient.auth.getSession();
      if (data.session) {
        this.session = data.session;
        this.user = data.session.user;
        this.onAuthChange?.(this.user);
      }
    } catch (err) {
      console.error('Failed to restore session:', err);
    }
  }

  async signUp(email, password) {
    try {
      const { data, error } = await this.supabaseClient.auth.signUp({
        email,
        password,
      });
      
      if (error) throw error;
      
      this.user = data.user;
      this.session = data.session;
      
      // Create user record in database
      await this.supabaseClient.from('users').insert([{
        id: data.user.id,
        email: email,
        subscription_tier: 'free',
      }]);
      
      this.onAuthChange?.(this.user);
      return { success: true, user: data.user };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async signIn(email, password) {
    try {
      const { data, error } = await this.supabaseClient.auth.signInWithPassword({
        email,
        password,
      });
      
      if (error) throw error;
      
      this.user = data.user;
      this.session = data.session;
      this.onAuthChange?.(this.user);
      return { success: true, user: data.user };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async signOut() {
    try {
      await this.supabaseClient.auth.signOut();
      this.user = null;
      this.session = null;
      this.onAuthChange?.(null);
      return { success: true };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  async getUserProfile() {
    if (!this.user) return null;
    
    try {
      const { data, error } = await this.supabaseClient
        .from('users')
        .select('*')
        .eq('id', this.user.id)
        .single();
      
      if (error) throw error;
      return data;
    } catch (err) {
      console.error('Failed to fetch user profile:', err);
      return null;
    }
  }

  async updateSubscription(tier) {
    if (!this.user) return { success: false, error: 'Not authenticated' };
    
    try {
      const { data, error } = await this.supabaseClient
        .from('users')
        .update({ subscription_tier: tier })
        .eq('id', this.user.id)
        .select()
        .single();
      
      if (error) throw error;
      return { success: true, profile: data };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  isAuthenticated() {
    return !!this.user;
  }

  getCurrentUser() {
    return this.user;
  }
}

export const authManager = new AuthManager();
