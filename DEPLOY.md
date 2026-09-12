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

3. **Add environment variables:**
   ```bash
   railway variables set TELEGRAM_BOT_TOKEN=your_token
   railway variables set OPENROUTER_API_KEY=your_key
   ```

4. **Deploy:**
   ```bash
   railway up
   ```

## Docker Deploy

Railway auto-detects `Dockerfile` or `railway.toml`.

### With Dockerfile (default)
```bash
# In project root:
railway up --docker
```

### With railway.toml
Create `railway.toml`:
```toml
[build]
dockerfile = "Dockerfile"

[start]
command = "python bot.py"

[healthcheck]
path = "/"
interval = 30
timeout = 5
```

## Manual Setup (web dashboard)

1. Push to GitHub
2. Go to https://railway.app/new
3. Connect GitHub repo `archeryfox/arcana-os`
4. Add variables: `TELEGRAM_BOT_TOKEN`, `OPENROUTER_API_KEY`
5. Deploy

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
