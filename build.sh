#!/bin/bash

# The Card - Build Script for GitHub Pages + Supabase

echo "🚀 Building The Card..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 16+"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"

# Check environment variables
if [ -z "$REACT_APP_SUPABASE_URL" ]; then
    echo "⚠️  REACT_APP_SUPABASE_URL not set. Using .env.local"
fi

if [ -z "$REACT_APP_SUPABASE_KEY" ]; then
    echo "⚠️  REACT_APP_SUPABASE_KEY not set. Using .env.local"
fi

# Build
echo "🔨 Building application..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build successful!"

# Summary
echo ""
echo "📊 Build Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Output directory: dist/"
echo "Total files: $(find dist -type f | wc -l)"
echo "Total size: $(du -sh dist | cut -f1)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "✨ Next steps:"
echo "  1. Push to GitHub: git push origin main"
echo "  2. Check deployment: https://github.com/YOUR_USERNAME/Bokke-Vs-New-Zeeland/deployments"
echo "  3. View live: https://YOUR_USERNAME.github.io/Bokke-Vs-New-Zeeland"
echo ""
echo "🎉 Ready to deploy!"
