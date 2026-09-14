# The Card — GitHub Pages + Supabase Deployment

## Architecture

```
┌─────────────────────────────┐
│   GitHub Pages (Static)     │
│   index.html + assets       │
│   (Automatic deployment)    │
└──────────────┬──────────────┘
               │ (HTTPS)
               ▼
┌─────────────────────────────┐
│    Supabase Backend         │
│  ┌────────────────────────┐ │
│  │ PostgreSQL Database    │ │
│  │ (users, predictions)   │ │
│  └────────────────────────┘ │
│  ┌────────────────────────┐ │
│  │ Auth (JWT tokens)      │ │
│  │ (email/password)       │ │
│  └────────────────────────┘ │
│  ┌────────────────────────┐ │
│  │ Real-time (Websocket)  │ │
│  │ (LISTEN/NOTIFY)        │ │
│  └────────────────────────┘ │
└─────────────────────────────┘
```

## Deployment Checklist

### GitHub Pages Setup

- [ ] Repository created
- [ ] GitHub Pages enabled
- [ ] Custom domain configured (optional)
- [ ] SSL certificate enabled
- [ ] Deploy workflow configured

### Supabase Setup

- [ ] Project created
- [ ] Database tables created
- [ ] Authentication enabled
- [ ] Real-time replication enabled
- [ ] API keys obtained
- [ ] RLS policies configured

### Environment Configuration

- [ ] `.env.local` created
- [ ] GitHub secrets added
- [ ] Supabase URL in config
- [ ] Supabase key in config

### Application Configuration

- [ ] `src/supabase.js` configured
- [ ] Authentication page functional
- [ ] Database CRUD operations working
- [ ] Real-time subscriptions working

## Step-by-Step Deployment

### 1. Fork Repository

```bash
# Clone fork
git clone https://github.com/YOUR_USERNAME/Bokke-Vs-New-Zeeland.git
cd Bokke-Vs-New-Zeeland

# Add upstream
git remote add upstream https://github.com/devforge-os1/Bokke-Vs-New-Zeeland.git
```

### 2. Configure GitHub Pages

1. Go to **Settings → Pages**
2. Source: `GitHub Actions` or `gh-pages branch`
3. Save

### 3. Configure Supabase

1. Create Supabase project
2. Run SQL from `docs/supabase.md`
3. Get API keys

### 4. Add GitHub Secrets

```bash
# Settings → Secrets → New repository secret

SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...
```

### 5. Update Configuration

**`src/config.js`:**
```javascript
export const config = {
  supabase: {
    url: process.env.REACT_APP_SUPABASE_URL,
    key: process.env.REACT_APP_SUPABASE_KEY
  },
  api: {
    baseUrl: 'https://api.thecard.io'
  }
};
```

### 6. Build and Deploy

```bash
# Install dependencies
npm install

# Build
npm run build

# Test locally
npm run preview

# Push to GitHub (automatic deployment)
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

## Automatic Deployment Workflow

**.github/workflows/deploy.yml:**

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm install
      
      - name: Build
        run: npm run build
        env:
          REACT_APP_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          REACT_APP_SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
      
      - name: Deploy to Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

## Custom Domain (Optional)

### 1. DNS Configuration

Add DNS records:
```
A record: 185.199.108.153
A record: 185.199.109.153
A record: 185.199.110.153
A record: 185.199.111.153
CNAME: www → your-username.github.io
```

### 2. GitHub Settings

1. **Settings → Pages**
2. Custom domain: `yourdomain.com`
3. Enforce HTTPS (automatic)

## Monitoring

### GitHub Pages

- **Status:** https://www.githubstatus.com
- **Analytics:** Repository → Insights → Traffic
- **Deployments:** Repository → Deployments

### Supabase

- **Dashboard:** https://supabase.com/dashboard
- **Database Stats:** Database → Stats
- **Real-time Usage:** Real-time → Connections
- **API Usage:** API → Rate Limit

## Troubleshooting

### Pages Not Deploying

```bash
# Check workflow status
# Repository → Actions → Latest workflow

# Check build logs
# Click on failed job for details
```

### Supabase Connection Issues

```bash
# Verify API keys
# Check environment variables
# Check CORS settings

# Test connection
curl -H "Authorization: Bearer YOUR_KEY" \
  https://xxxxx.supabase.co/rest/v1/users?select=count
```

### Authentication Not Working

```javascript
// Check browser console for errors
console.log('Supabase URL:', SUPABASE_URL);
console.log('Supabase Key:', SUPABASE_KEY);

// Test auth
const { user, error } = await supabase.auth.getSession();
console.log('Session:', { user, error });
```

## Performance Optimization

### GitHub Pages

- **Enable compression:** Gzip automatically enabled
- **Cache busting:** Vite handles automatically
- **CDN:** GitHub Pages uses Fastly CDN

### Supabase

- **Connection pooling:** Enabled by default
- **Query optimization:** Use indexes
- **Caching:** Client-side storage for offline support

## Security Best Practices

- ✅ Never commit `.env.local`
- ✅ Use GitHub Secrets for sensitive data
- ✅ Enable RLS policies in Supabase
- ✅ Use anon key for public access (read-only)
- ✅ Use service_role key only on backend
- ✅ Validate all user inputs
- ✅ Enable HTTPS (automatic)

## Scalability

### GitHub Pages Limits

- **Build time:** 10 minutes maximum
- **Repository size:** No strict limit
- **Bandwidth:** Unlimited
- **Concurrent users:** Unlimited (CDN)

### Supabase Limits (Free Tier)

- **Database:** 500MB
- **API calls:** 50,000/day (soft limit)
- **Concurrent connections:** 10
- **Backup:** 7 days retention

**Upgrade when needed:**
```
Settings → Billing → Change plan
```

## Support

- **GitHub Pages Docs:** https://docs.github.com/pages
- **Supabase Docs:** https://supabase.com/docs
- **Community Discord:** https://discord.supabase.com

---

**Deployment complete! Your app is now live! 🚀**
