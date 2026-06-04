# tg-ytdlp-bot

A Telegram bot that downloads videos, audio, and images from YouTube, TikTok, Instagram, and 1500+ other platforms using yt-dlp and gallery-dl.

## Run & Operate

- Entry point: `python magic.py`
- Deploy target: Render (Background Worker using Docker)
- See `RENDER_DEPLOY.md` for the full deployment guide

## Stack

- Python 3.10
- Pyrogram (PyroTGFork) — Telegram MTProto client
- yt-dlp — video/audio downloading engine
- gallery-dl — image downloading engine
- ffmpeg — media processing
- Firebase (optional) — caching layer

## Where things live

- `magic.py` — bot entry point; registers all handlers
- `CONFIG/config.py` — **env-var-based config** (no secrets in code)
- `CONFIG/_config.py` — original template with field docs (do not use directly)
- `COMMANDS/` — per-command handlers (`/format`, `/audio`, `/proxy`, etc.)
- `DOWN_AND_UP/` — download + upload logic, ffmpeg wrappers, yt-dlp hooks
- `URL_PARSERS/` — URL normalisation, YouTube/TikTok/embed parsers
- `HELPERS/` — rate limiting, logging, proxies, caption builder, decorators
- `DATABASE/` — Firebase cache, download history
- `TXT/` — cookie files, supported sites list
- `render.yaml` — Render deployment manifest
- `render.Dockerfile` — Render-optimised Docker image
- `.env.example` — documents every configurable env var

## Required env vars (set in Render dashboard)

| Variable | Description |
|----------|-------------|
| `BOT_TOKEN` | Bot token from @BotFather |
| `API_ID` | Integer from my.telegram.org |
| `API_HASH` | String from my.telegram.org |
| `ADMIN` | Your Telegram user ID (e.g. `123456789`) |
| `LOGS_ID` | Log channel ID (e.g. `-1001234567890`) |

All other variables are optional — see `.env.example`.

## User preferences

- Pure Telegram bot — no web app, no Node.js code
- Deployable on Render as a Background Worker
- All configuration via environment variables (no hardcoded secrets)
