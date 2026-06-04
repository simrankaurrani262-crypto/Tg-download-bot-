# Deploying to Render

This guide walks you through deploying the bot as a **Background Worker** on Render.

---

## Prerequisites

| What | Where to get it |
|------|----------------|
| Telegram Bot Token | [@BotFather](https://t.me/BotFather) → `/newbot` |
| Telegram API ID & Hash | [my.telegram.org](https://my.telegram.org) → App API |
| Your Telegram user ID | [@userinfobot](https://t.me/userinfobot) |
| A Telegram channel for logs | Create a private channel, add your bot as admin, copy the channel ID (starts with `-100`) |

---

## Step 1 — Push this repo to GitHub / GitLab

Render deploys from a Git remote. Push the `tg-ytdlp-bot/` folder (or its parent) to your own repository.

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## Step 2 — Create a new Render service

1. Go to [render.com](https://render.com) → **New → Background Worker**
2. Connect your repository
3. Render will detect `render.yaml` automatically — click **Apply**

If Render doesn't auto-detect:
- **Environment**: Docker
- **Dockerfile path**: `render.Dockerfile`
- **Build & Deploy region**: your choice (Oregon is cheapest)

---

## Step 3 — Set environment variables

In Render → your service → **Environment** tab, add the following:

### Required

| Variable | Value |
|----------|-------|
| `BOT_TOKEN` | Your bot token from BotFather |
| `API_ID` | Your Telegram API ID (integer) |
| `API_HASH` | Your Telegram API hash (string) |
| `ADMIN` | Your Telegram user ID, e.g. `123456789` |
| `LOGS_ID` | Log channel ID, e.g. `-1001234567890` |

### Recommended

| Variable | Value |
|----------|-------|
| `BOT_NAME` | Internal name, no spaces (e.g. `myytdlpbot`) |
| `BOT_NAME_FOR_USERS` | Same as `BOT_NAME` or bot @username |
| `ADMIN_USERNAME` | Your @username, e.g. `@alice` |
| `SUBSCRIBE_CHANNEL` | Channel ID users must join before using the bot |
| `SUBSCRIBE_CHANNEL_URL` | Invite link, e.g. `https://t.me/+xxxxx` |

> **All remaining variables** are documented in `.env.example`.

---

## Step 4 — Deploy

Click **Save Changes** then **Manual Deploy → Deploy latest commit**.

Render will:
1. Build the Docker image (installs ffmpeg, mediainfo, Python deps)
2. Start the bot process

Watch the **Logs** tab — you should see `magic.py` start up and the bot come online.

---

## Persistent session file

Pyrogram stores a `magic.session` file to avoid re-authentication on restarts. On Render's free tier, the filesystem is **ephemeral** — the session file is lost on every deploy, forcing a re-auth.

**Fix (recommended):** Use a Render **Persistent Disk**:
- Render Dashboard → your service → **Disks** → Add disk
- Mount path: `/app`
- This keeps `magic.session`, downloads, and logs across deploys

On the **Standard plan** and above, you can add a persistent disk.

---

## Cookies (for age-restricted / private content)

Host your Netscape-format cookie files on any public HTTPS URL (GitHub Gist, S3, etc.) and set the corresponding env vars:

```
YOUTUBE_COOKIE_URL=https://raw.githubusercontent.com/YOU/cookies/main/youtube.txt
```

---

## Plan sizing

| Plan | RAM | Notes |
|------|-----|-------|
| Starter ($7/mo) | 512 MB | Fine for low traffic |
| Standard ($25/mo) | 2 GB | Recommended; allows persistent disk |
| Pro ($85/mo) | 4 GB | For heavy concurrent downloads |

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Bot starts but dies on each deploy | Add a Persistent Disk (see above) |
| `API_ID is 0` error | Check that `API_ID` env var is set as an integer without quotes |
| Firebase errors | Set `USE_FIREBASE=false` (default) unless you've configured Firebase |
| YouTube 403 errors | Set `YOUTUBE_COOKIE_URL` with valid cookies |
