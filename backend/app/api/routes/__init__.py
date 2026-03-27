from fastapi import APIRouter

from app.api.routes.auction_setup import router as auction_setup_router
from app.api.routes.health import router as health_router
from app.api.routes.historical_data import router as historical_data_router
from app.api.routes.live_auction import router as live_auction_router
from app.api.routes.post_auction import router as post_auction_router
from app.api.routes.players import router as players_router
from app.api.routes.scoring import router as scoring_router
from app.api.routes.team_builder import router as team_builder_router

api_router = APIRouter()
api_router.include_router(auction_setup_router)
api_router.include_router(health_router)
api_router.include_router(historical_data_router)
api_router.include_router(live_auction_router)
api_router.include_router(post_auction_router)
api_router.include_router(scoring_router)
api_router.include_router(team_builder_router)
api_router.include_router(players_router)
