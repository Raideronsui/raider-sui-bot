# Raider Swing Bot

An automated SUI swing-trading Telegram bot using Cetus DEX. Built with:

- Trading logic (`sui_trader.py`)
- Telegram interface & scheduler (`trading_bot.py`)
- Deployable via Render (`render.yaml`)

## Setup

1. Clone this repo:
   ```bash
   git clone <repo_url>
   cd raider-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` → `.env` and fill in:
   ```
   SUI_PRIVATE_KEY=…
   SUI_RPC_URL=…
   CETUS_API=https://api-sui.cetus.zone
   TELEGRAM_TOKEN=…
   CHAT_ID=…
   ```

4. (Optional) Replace placeholder swap logic in `sui_trader.py` with actual Sui SDK calls.

5. Run locally:
   ```bash
   python trading_bot.py
   ```

6. Deploy on Render:
   - Push to GitHub
   - Connect repo in Render dashboard
