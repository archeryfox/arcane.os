# Deploy to Railway (Free Tier)

## Quick Start

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and init:**
   ```bash
   railway login
   railway init
   ```

3. **Add environment variables in Railway dashboard or CLI:**
   ```bash
   railway variables set TELEGRAM_BOT_TOKEN=your_token
   railway variables set OPENROUTER_API_KEY=your_key
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

## Alternative: One-click Deploy

Push to GitHub, then connect repo at https://railway.app/new

## Other Free Options

**Render.com:**
- Create Web Service from GitHub repo
- Build: `pip install -r requirements.txt`
- Start: `python bot.py`
- Add env vars in dashboard

**Fly.io:**
```bash
flyctl launch --no-deploy
flyctl secrets set TELEGRAM_BOT_TOKEN=xxx OPENROUTER_API_KEY=xxx
flyctl deploy
```

**VPS (always-on):**
- DigitalOcean Droplet ($4/mo) / Hetzner CX22 (€4/mo)
- Use systemd service + nginx if needed