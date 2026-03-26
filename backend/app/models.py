from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TimestampMixin:
    """Reusable created/updated timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )


class PlayerRoleHint(StrEnum):
    BATTER = "batter"
    BOWLER = "bowler"
    ALL_ROUNDER = "all-rounder"
    FIELDING_ASSET = "fielding asset"
    UNKNOWN = "unknown"


class AuctionEventType(StrEnum):
    BOUGHT_BY_ME = "bought_by_me"
    BOUGHT_BY_OTHER = "bought_by_other"
    UNSOLD = "unsold"


class PoolStatus(StrEnum):
    AVAILABLE = "available"
    SOLD = "sold"
    UNSOLD = "unsold"
    WITHDRAWN = "withdrawn"


class RosterStatus(StrEnum):
    BOUGHT = "bought"
    CAPTAIN_RETAINED = "captain_retained"


class Player(TimestampMixin, Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    display_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    player_key: Mapped[str | None] = mapped_column(String(160), unique=True, nullable=True, index=True)
    playing_role: Mapped[str | None] = mapped_column(String(50), nullable=True)
    batting_style: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bowling_style: Mapped[str | None] = mapped_column(String(50), nullable=True)
    team_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    batting_stats: Mapped[list[BattingStat]] = relationship(back_populates="player", cascade="all, delete-orphan")
    bowling_stats: Mapped[list[BowlingStat]] = relationship(back_populates="player", cascade="all, delete-orphan")
    fielding_stats: Mapped[list[FieldingStat]] = relationship(back_populates="player", cascade="all, delete-orphan")
    merged_scores: Mapped[list[MergedPlayerScore]] = relationship(back_populates="player", cascade="all, delete-orphan")
    captain_record: Mapped[Captain | None] = relationship(back_populates="player")
    pool_entries: Mapped[list[CurrentPlayerPool]] = relationship(back_populates="player", cascade="all, delete-orphan")
    roster_entries: Mapped[list[TeamRoster]] = relationship(back_populates="player")
    auction_events: Mapped[list[AuctionEvent]] = relationship(back_populates="player")
    sold_record: Mapped[SoldPlayer | None] = relationship(back_populates="player")


class BattingStat(TimestampMixin, Base):
    __tablename__ = "batting_stats"
    __table_args__ = (UniqueConstraint("player_id", "source_file", name="uq_batting_player_source"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), index=True)
    source_file: Mapped[str] = mapped_column(String(255), default="historical_batting.xlsx", nullable=False)
    matches: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    innings: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    runs: Mapped[int | None] = mapped_column(Integer, nullable=True)
    average: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    strike_rate: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    fours: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    player: Mapped[Player] = relationship(back_populates="batting_stats")


class BowlingStat(TimestampMixin, Base):
    __tablename__ = "bowling_stats"
    __table_args__ = (UniqueConstraint("player_id", "source_file", name="uq_bowling_player_source"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), index=True)
    source_file: Mapped[str] = mapped_column(String(255), default="historical_bowling.xlsx", nullable=False)
    matches: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    overs: Mapped[Decimal] = mapped_column(Numeric(6, 2), default=0, nullable=False)
    wickets: Mapped[int | None] = mapped_column(Integer, nullable=True)
    average: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    economy: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)

    player: Mapped[Player] = relationship(back_populates="bowling_stats")


class FieldingStat(TimestampMixin, Base):
    __tablename__ = "fielding_stats"
    __table_args__ = (UniqueConstraint("player_id", "source_file", name="uq_fielding_player_source"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), index=True)
    source_file: Mapped[str] = mapped_column(String(255), default="historical_fielding.xlsx", nullable=False)
    matches: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    catches: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    direct_run_outs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    indirect_run_outs: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    player: Mapped[Player] = relationship(back_populates="fielding_stats")


class MergedPlayerScore(TimestampMixin, Base):
    __tablename__ = "merged_player_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), unique=True, index=True)
    batting_score: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=0, nullable=False)
    bowling_score: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=0, nullable=False)
    fielding_score: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=0, nullable=False)
    overall_score: Mapped[Decimal] = mapped_column(Numeric(4, 2), default=0, nullable=False)
    role_hint: Mapped[PlayerRoleHint] = mapped_column(Enum(PlayerRoleHint), default=PlayerRoleHint.UNKNOWN)
    scoring_version: Mapped[str] = mapped_column(String(30), default="v1", nullable=False)

    player: Mapped[Player] = relationship(back_populates="merged_scores")


class AuctionSetting(TimestampMixin, Base):
    __tablename__ = "auction_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tournament_name: Mapped[str] = mapped_column(String(120), default="Cricket Auction", nullable=False)
    number_of_teams: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    squad_size: Mapped[int] = mapped_column(Integer, default=12, nullable=False)
    total_points_per_captain: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=100, nullable=False)
    captain_self_value_deduction: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    max_bid: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=25, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    teams: Mapped[list[Team]] = relationship(back_populates="auction_setting")
    auction_events: Mapped[list[AuctionEvent]] = relationship(back_populates="auction_setting")


class Team(TimestampMixin, Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    auction_setting_id: Mapped[int | None] = mapped_column(ForeignKey("auction_settings.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    owner_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    starting_budget: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    remaining_budget: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    max_bid_limit: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    squad_size_target: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_my_team: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    auction_setting: Mapped[AuctionSetting | None] = relationship(back_populates="teams")
    captain: Mapped[Captain | None] = relationship(back_populates="team", cascade="all, delete-orphan")
    roster_entries: Mapped[list[TeamRoster]] = relationship(back_populates="team", cascade="all, delete-orphan")
    auction_events: Mapped[list[AuctionEvent]] = relationship(back_populates="team")
    sold_players: Mapped[list[SoldPlayer]] = relationship(back_populates="team")


class Captain(TimestampMixin, Base):
    __tablename__ = "captains"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), unique=True)
    player_id: Mapped[int | None] = mapped_column(ForeignKey("players.id", ondelete="SET NULL"), unique=True, nullable=True)
    captain_name: Mapped[str] = mapped_column(String(120), nullable=False)
    self_cost_deduction: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)

    team: Mapped[Team] = relationship(back_populates="captain")
    player: Mapped[Player | None] = relationship(back_populates="captain_record")


class TeamRoster(TimestampMixin, Base):
    __tablename__ = "team_rosters"
    __table_args__ = (UniqueConstraint("team_id", "player_id", name="uq_team_roster_player"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"), index=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), index=True)
    purchase_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    status: Mapped[RosterStatus] = mapped_column(Enum(RosterStatus), default=RosterStatus.BOUGHT)

    team: Mapped[Team] = relationship(back_populates="roster_entries")
    player: Mapped[Player] = relationship(back_populates="roster_entries")


class AuctionEvent(TimestampMixin, Base):
    __tablename__ = "auction_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    auction_setting_id: Mapped[int | None] = mapped_column(ForeignKey("auction_settings.id", ondelete="SET NULL"), nullable=True)
    player_id: Mapped[int | None] = mapped_column(ForeignKey("players.id", ondelete="SET NULL"), nullable=True)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id", ondelete="SET NULL"), nullable=True)
    nomination_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    final_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    event_type: Mapped[AuctionEventType] = mapped_column(Enum(AuctionEventType), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    auction_setting: Mapped[AuctionSetting | None] = relationship(back_populates="auction_events")
    player: Mapped[Player | None] = relationship(back_populates="auction_events")
    team: Mapped[Team | None] = relationship(back_populates="auction_events")
    sold_player: Mapped[SoldPlayer | None] = relationship(back_populates="auction_event")


class SoldPlayer(TimestampMixin, Base):
    __tablename__ = "sold_players"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    auction_event_id: Mapped[int | None] = mapped_column(ForeignKey("auction_events.id", ondelete="SET NULL"), unique=True, nullable=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), unique=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    sold_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    auction_event: Mapped[AuctionEvent | None] = relationship(back_populates="sold_player")
    player: Mapped[Player] = relationship(back_populates="sold_record")
    team: Mapped[Team] = relationship(back_populates="sold_players")


class CurrentPlayerPool(TimestampMixin, Base):
    __tablename__ = "current_player_pool"
    __table_args__ = (UniqueConstraint("player_id", name="uq_current_pool_player"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id", ondelete="CASCADE"), index=True)
    source_file: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[PoolStatus] = mapped_column(Enum(PoolStatus), default=PoolStatus.AVAILABLE, nullable=False)
    auction_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_captain: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reserve_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    player: Mapped[Player] = relationship(back_populates="pool_entries")
