# CricAnalyzer

CricAnalyzer is a beginner-friendly full-stack cricket auction assistant for cricket leagues and captain auctions. It reads historical Excel files, calculates transparent player scores, helps you run a live auction, tracks your squad, and compares teams after the auction.

## Current Version

This first version is:

- rule-based, not ML-based
- built for clarity over complexity
- easy to edit in a few main config and service files
- designed to run locally with SQLite by default

Completed steps:

- Step 1: project structure and environment setup
- Step 2: backend models and database schema
- Step 3: historical Excel upload and parsing
- Step 4: score calculation engine
- Step 5: player database page and API
- Step 6: player detail page and charts
- Step 7: auction setup page, team/captain setup, and current player pool upload
- Step 8: live auction page, auction event logging, and budget tracking
- Step 9: rule-based bid recommendation engine
- Step 10: team builder page
- Step 11: post-auction analysis page
- Step 12: cleanup, documentation, and test setup

## Tech Stack

- Frontend: Next.js App Router + TypeScript + Tailwind CSS
- Backend: FastAPI + Python
- Data processing: pandas + numpy
- Database: SQLite locally by default, `DATABASE_URL` available for Postgres later
- Charts: Chart.js
- Validation: Pydantic on backend

## Folder Structure

```text
CricAnalyzer/
├─ backend/
│  ├─ app/
│  │  ├─ api/routes/              # FastAPI route files
│  │  ├─ core/                    # config, score weights, column mappings
│  │  ├─ db/                      # SQLAlchemy base/session setup
│  │  ├─ schemas/                 # Pydantic request/response models
│  │  ├─ services/                # business logic
│  │  ├─ main.py                  # FastAPI app entry point
│  │  └─ models.py                # database models
│  ├─ tests/                      # backend tests
│  ├─ requirements.txt            # backend dependencies
│  └─ pytest.ini                  # pytest config
├─ frontend/
│  ├─ app/                        # Next.js pages
│  ├─ components/                 # reusable UI components
│  ├─ lib/api.ts                  # frontend API functions and shared types
│  └─ package.json                # frontend scripts/dependencies
├─ sample_data/                   # sample files for testing
└─ README.md
```

## Main Pages

- Dashboard: `http://localhost:3000/`
- Player Database: `http://localhost:3000/players`
- Auction Setup: `http://localhost:3000/auction-setup`
- Live Auction: `http://localhost:3000/live-auction`
- Team Builder: `http://localhost:3000/team-builder`
- Post-Auction Analysis: `http://localhost:3000/post-auction-analysis`

## First-Time Setup

### 1. Backend

```powershell
cd C:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

Backend URLs:

- Health check: `http://127.0.0.1:8000/api/health`
- Swagger docs: `http://127.0.0.1:8000/docs`

### 2. Frontend

Open a second terminal:

```powershell
cd C:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\frontend
npm install
npm run dev
```

Frontend URL:

- `http://localhost:3000`

Important:

- use `http://localhost:3000`
- not `http://127.0.0.1:3000`

That avoids browser origin/CORS mismatches with the backend.

## Environment Files

### Backend `.env`

Local SQLite is the default. Leave `DATABASE_URL` blank to use `backend/cricanalyzer.db`.

Example:

```env
APP_NAME=CricAnalyzer API
APP_ENV=development
APP_HOST=127.0.0.1
APP_PORT=8000
FRONTEND_ORIGIN=http://localhost:3000
DATABASE_URL=
SUPABASE_URL=
SUPABASE_KEY=
SUPABASE_DB_URL=
AUTO_CREATE_TABLES=true
SQL_ECHO=false
```

### Frontend `.env.local`

Only needed if your backend URL changes.

Example:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

## Main Commands

### Backend

Run API:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Run tests:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pytest
```

### Frontend

Run dev server:

```powershell
cd frontend
npm run dev
```

Lint + production build check:

```powershell
cd frontend
npm run check
```

## How the App Works

### Historical data flow

1. Upload batting, bowling, and fielding Excel files on the dashboard.
2. Backend parses the files with pandas.
3. Column names are normalized using editable mappings.
4. Raw stats are stored in database tables.
5. Click `Process and merge scores`.
6. Backend calculates batting, bowling, fielding, and overall scores.
7. Scores are stored in `merged_player_scores`.

Main files involved:

- [backend/app/services/excel_parser.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\excel_parser.py)
- [backend/app/services/historical_data_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\historical_data_service.py)
- [backend/app/services/scoring_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\scoring_service.py)

### Auction setup flow

1. Save auction rules and teams.
2. Link captains to scored players where possible.
3. Linked captains are retained automatically before auction starts.
4. Captain deduction is already reflected in team budget.
5. Retained captains are removed from the live auction pool.

Main files involved:

- [backend/app/services/auction_setup_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\auction_setup_service.py)
- [frontend/components/auction-settings-form.tsx](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\frontend\components\auction-settings-form.tsx)

### Live auction flow

1. Upload the current player pool.
2. Open live auction.
3. Select a player from the remaining pool.
4. View player summary and bid recommendation.
5. Record `bought by me`, `bought by another team`, or `unsold`.
6. Budgets, rosters, and recent event log update immediately.

Main files involved:

- [backend/app/services/live_auction_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\live_auction_service.py)
- [backend/app/services/bid_recommendation_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\bid_recommendation_service.py)
- [frontend/components/live-auction-panel.tsx](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\frontend\components\live-auction-panel.tsx)

### Post-auction analysis flow

1. Use saved auction setup plus live auction results.
2. Backend reads all teams and rosters.
3. Team totals are compared across batting, bowling, fielding, and overall.
4. Contenders, weaknesses, strengths, and value buys are shown.

Main files involved:

- [backend/app/services/post_auction_analysis_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\post_auction_analysis_service.py)
- [frontend/app/post-auction-analysis/page.tsx](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\frontend\app\post-auction-analysis\page.tsx)

## Scoring Rules

### Batting

Uses:

- 4s
- strike rate
- average

Weights:

- 20% fours
- 40% strike rate
- 40% average

Extra rule:

- batting score becomes `0.00` if innings `<= 7`

### Bowling

Uses:

- economy
- average

Weights:

- 66% economy
- 34% average

Extra rule:

- bowling score becomes `0.00` if overs `<= 7`

### Fielding

Uses per match:

- catches
- direct run outs
- indirect run outs

Weights:

- 45% catches
- 45% direct run outs
- 10% indirect run outs

### Overall

Uses:

- 40% batting
- 40% bowling
- 20% fielding

## Role Rules

Roles are derived from scores, not Excel labels:

- batter: batting score `>= 3.7`
- bowler: bowling score `>= 5.0`
- all-rounder: batting and bowling both meet cutoff
- fielding asset: fielding score `>= 4.0` when batting/bowling cutoffs are not met

Important:

- after changing role rules, click `Process and merge scores` again

## Current Player Pool Upload Format

Required column:

- player name

Optional columns:

- captain
- reserve price
- auction order

If your file headers differ, edit:

- [backend/app/core/column_mappings.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\core\column_mappings.py)

## Bid Recommendation Logic

Current fair value formula:

1. calculate average spend per open slot
2. detect which of batting, bowling, fielding your team still needs
3. compute the team-need multiplier based on how many of those needs the player covers
4. add `2 x (batting score + bowling score + fielding score)`

Current team rules:

- always target `7` bowlers
- aim for `3/4` of the squad to qualify as batters
- good fielders are always useful

Current recommendation labels:

- `skip`
- `not at the moment`
- `50/50`
- `good pick`
- `priority target`

Main files to edit:

- [backend/app/services/bid_recommendation_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\bid_recommendation_service.py)
- [backend/app/core/scoring_config.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\core\scoring_config.py)

## Most Important Files To Edit Later

### Change score weights

- [backend/app/core/scoring_config.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\core\scoring_config.py)

### Change Excel header mappings

- [backend/app/core/column_mappings.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\core\column_mappings.py)

### Change scoring formulas

- [backend/app/services/scoring_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\scoring_service.py)

### Change auction setup behavior

- [backend/app/services/auction_setup_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\auction_setup_service.py)

### Change live auction behavior

- [backend/app/services/live_auction_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\live_auction_service.py)

### Change bid recommendations

- [backend/app/services/bid_recommendation_service.py](c:\Users\natha\OneDrive\Desktop\ProjectsCS\CricAnalyzer\backend\app\services\bid_recommendation_service.py)

## Testing Checklist

### Historical data

1. Upload batting, bowling, and fielding files.
2. Confirm each status card changes to loaded.
3. Click `Process and merge scores`.

### Player pages

1. Open `/players`.
2. Search and filter.
3. Click a player name.
4. Confirm charts and numeric stat sections render.

### Auction setup

1. Save auction rules.
2. Link captains to players.
3. Confirm captains appear in team builder before the auction starts.

### Live auction

1. Upload current player pool.
2. Confirm retained captains do not appear in remaining pool.
3. Record a sold or unsold player.
4. Confirm budget, roster, and event log update.

### Team builder

1. Open `/team-builder`.
2. Confirm roster rows appear.
3. Confirm `Captain retained` and `Auction buy` sources display correctly.

### Post-auction analysis

1. Open `/post-auction-analysis`.
2. Confirm comparison chart renders.
3. Confirm contenders and value buys show when data exists.

## Tests Included

Backend tests currently cover:

- health route
- schema existence
- Excel parsing
- historical data service duplicate handling
- score normalization and role logic
- bid recommendation config
- auction setup route and captain retention
- live auction state route
- team builder route
- post-auction analysis route

## Future Improvements

- allow uploading final teams directly for post-auction analysis
- add similar-player suggestions on player detail page
- add export to CSV/Excel for auction logs and teams
- add frontend tests
- add deeper backend route tests with seeded sample data
- add auth if the app becomes multi-user later
- add optional ML experiments only after the rule-based version feels stable

## Notes

- Secrets should stay in `.env` files, not in code.
- The current version is intentionally transparent and rule-based.
- Linked captains are retained automatically and removed from the live auction pool.
