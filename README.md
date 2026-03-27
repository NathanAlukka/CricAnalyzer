# CricAnalyzer

CricAnalyzer is a beginner-friendly full-stack cricket auction assistant.

## Stack

- Frontend: Next.js App Router + TypeScript + Tailwind CSS
- Backend: FastAPI + Python
- Data processing: pandas + numpy
- Database: SQLite locally by default, with `DATABASE_URL` available for Postgres later
- Charts: Chart.js
- Validation: Pydantic on backend

## Folder Structure

- `frontend/`: Next.js user interface
- `backend/`: FastAPI API, database models, parsing, and scoring logic

## Current Progress

- Step 1: project structure and environment setup
- Step 2: backend models and database schema
- Step 3: historical Excel upload and parsing
- Step 4: score calculation engine
- Step 5: player database page and API
- Step 6: player detail page and charts
- Step 7: auction setup page, team/captain setup, and current player pool upload
- Step 8: live auction page, auction event logging, and budget tracking

## Main Commands

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
uvicorn app.main:app --reload
```

## Main Pages

- Dashboard: `http://localhost:3000/`
- Player Database: `http://localhost:3000/players`
- Auction Setup: `http://localhost:3000/auction-setup`
- Live Auction: `http://localhost:3000/live-auction`

## Setup Notes

### Backend database

Local SQLite is the default. Leave `DATABASE_URL` blank in `backend/.env` to use the local file database.

### Frontend API URL

If needed, set `NEXT_PUBLIC_API_BASE_URL` in `frontend/.env.local`.

## What Step 7 Adds

The Auction Setup page lets you:

- save tournament name
- save number of teams
- save squad size
- save total points per captain
- save captain self-value deduction
- save max bid
- define teams and captains
- mark one team as your team
- upload the current player pool from Excel

## What Step 8 Adds

The Live Auction page lets you:

- select the current player from the remaining pool
- mark the player as bought by you, bought by another team, or unsold
- enter the final sale price
- update team remaining budgets
- update your roster count and open slots
- track recent auction events
- reset the live auction state if needed

## Current Player Pool Upload Format

Required column:

- player name

Optional columns:

- captain
- reserve price
- auction order

If your file uses different headers, edit:

- `backend/app/core/column_mappings.py`

## Important Files To Edit Later

### Scoring logic

- `backend/app/core/scoring_config.py`
- `backend/app/services/scoring_service.py`

### Historical Excel parsing

- `backend/app/core/column_mappings.py`
- `backend/app/services/excel_parser.py`

### Auction setup logic

- `backend/app/services/auction_setup_service.py`
- `backend/app/api/routes/auction_setup.py`

### Live auction logic

- `backend/app/services/live_auction_service.py`
- `backend/app/api/routes/live_auction.py`
- `frontend/components/live-auction-panel.tsx`
- `frontend/components/auction-event-log.tsx`
- `frontend/app/live-auction/page.tsx`

### Frontend pages and forms

- `frontend/app/page.tsx`
- `frontend/app/players/page.tsx`
- `frontend/app/players/[playerId]/page.tsx`
- `frontend/app/auction-setup/page.tsx`
- `frontend/components/auction-settings-form.tsx`
- `frontend/components/current-player-pool-upload-form.tsx`

## Testing Step 7

1. Start the backend.
2. Start the frontend.
3. Open `http://localhost:3000/auction-setup`.
4. Save the auction settings form.
5. Upload a current player pool Excel file.
6. Confirm the saved status messages appear.

## Testing Step 8

1. Complete Step 7 first.
2. Open `http://localhost:3000/live-auction`.
3. Select a player from the remaining pool.
4. Save an auction result.
5. Confirm the event log and team budgets update.

## Notes

- Secrets should stay in `.env` files, not in code.
- The current version is rule-based and does not use ML.
- Later steps will add live auction flow, recommendations, team builder, and post-auction analysis.
