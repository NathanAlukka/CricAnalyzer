const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export interface HistoricalDatasetStatusItem {
  dataset_type: string;
  rows_loaded: number;
  loaded: boolean;
}

export interface HistoricalUploadResult {
  dataset_type: string;
  source_file: string;
  rows_read: number;
  rows_saved: number;
  players_created: number;
  mapped_columns: Record<string, string>;
  missing_columns: string[];
}

export interface ScoreProcessingResult {
  players_processed: number;
  scores_created: number;
  scoring_version: string;
}

export interface PlayerDatabaseItem {
  id: number;
  name: string;
  team_name: string | null;
  role_hint: string;
  batting_score: number;
  bowling_score: number;
  fielding_score: number;
  overall_score: number;
}

export interface PlayerStatSummary {
  matches: number;
  runs?: number | null;
  average?: number | null;
  strike_rate?: number | null;
  fours?: number | null;
  wickets?: number | null;
  economy?: number | null;
  catches?: number | null;
  direct_run_outs?: number | null;
  indirect_run_outs?: number | null;
}

export interface PlayerComparisonScores {
  batting_score: number;
  bowling_score: number;
  fielding_score: number;
  overall_score: number;
}

export interface PlayerDetail {
  id: number;
  name: string;
  team_name: string | null;
  role_hint: string;
  batting_score: number;
  bowling_score: number;
  fielding_score: number;
  overall_score: number;
  batting_stats: PlayerStatSummary | null;
  bowling_stats: PlayerStatSummary | null;
  fielding_stats: PlayerStatSummary | null;
  batting_average_stats: PlayerStatSummary | null;
  bowling_average_stats: PlayerStatSummary | null;
  fielding_average_stats: PlayerStatSummary | null;
  player_scores: PlayerComparisonScores;
  average_scores: PlayerComparisonScores;
}

export interface CaptainSetupItem {
  team_name: string;
  owner_name: string | null;
  captain_name: string;
  captain_player_id: number | null;
  is_my_team: boolean;
}

export interface AuctionSettingsResponse {
  tournament_name: string;
  number_of_teams: number;
  squad_size: number;
  total_points_per_captain: number;
  captain_self_value_deduction: number;
  max_bid: number;
  teams: CaptainSetupItem[];
}

export interface PlayerOptionItem {
  id: number;
  name: string;
}

export interface CurrentPlayerPoolUploadResult {
  source_file: string;
  rows_read: number;
  rows_saved: number;
  players_created: number;
  captains_marked: number;
  mapped_columns: Record<string, string>;
  missing_columns: string[];
}

export interface CurrentPlayerPoolStatusResponse {
  rows_loaded: number;
  captains_loaded: number;
}

export interface LiveAuctionPlayerItem {
  player_id: number;
  player_name: string;
  team_name: string | null;
  role_hint: string;
  batting_score: number;
  bowling_score: number;
  fielding_score: number;
  overall_score: number;
  is_captain: boolean;
  reserve_price: number | null;
  auction_order: number | null;
}

export interface LiveAuctionTeamItem {
  team_id: number;
  team_name: string;
  owner_name: string | null;
  remaining_budget: number;
  squad_size_target: number | null;
  players_bought: number;
  is_my_team: boolean;
}

export interface MyTeamSummary {
  team_name: string;
  remaining_budget: number;
  squad_size_target: number | null;
  players_bought: number;
  open_slots: number;
  batter_count: number;
  bowler_count: number;
  all_rounder_count: number;
  fielding_asset_count: number;
  batting_total: number;
  bowling_total: number;
  fielding_total: number;
  overall_total: number;
}

export interface LiveAuctionEventItem {
  event_id: number;
  player_name: string;
  team_name: string | null;
  event_type: string;
  final_price: number | null;
  nomination_order: number | null;
}

export interface LiveAuctionStateResponse {
  remaining_pool: LiveAuctionPlayerItem[];
  teams: LiveAuctionTeamItem[];
  my_team_summary: MyTeamSummary | null;
  recent_events: LiveAuctionEventItem[];
}

export interface SubmitLiveAuctionEventRequest {
  player_id: number;
  event_type: string;
  team_id: number | null;
  final_price: number | null;
  notes: string | null;
}

export interface BidRecommendation {
  player_id: number;
  player_name: string;
  fair_value: number;
  good_buy_upto: number;
  overpay_threshold: number;
  hard_cap: number;
  recommendation_label: string;
  recommendation_reason: string;
  scarcity_score: number;
  team_need_score: number;
}

export interface TeamBuilderRosterItem {
  player_id: number;
  player_name: string;
  role_hint: string;
  roster_status: string;
  purchase_price: number | null;
  batting_score: number;
  bowling_score: number;
  fielding_score: number;
  overall_score: number;
}

export interface TeamBuilderSummary {
  team_name: string;
  remaining_budget: number;
  squad_size_target: number | null;
  players_bought: number;
  open_slots: number;
  batter_count: number;
  bowler_count: number;
  all_rounder_count: number;
  fielding_asset_count: number;
  batting_total: number;
  bowling_total: number;
  fielding_total: number;
  overall_total: number;
}

export interface TeamBuilderResponse {
  summary: TeamBuilderSummary | null;
  roster: TeamBuilderRosterItem[];
}

export interface PostAuctionTeamTopPlayer {
  player_name: string;
  overall_score: number;
}

export interface PostAuctionTeamItem {
  team_id: number;
  team_name: string;
  owner_name: string | null;
  players_count: number;
  remaining_budget: number;
  batting_total: number;
  bowling_total: number;
  fielding_total: number;
  overall_total: number;
  batter_count: number;
  bowler_count: number;
  all_rounder_count: number;
  fielding_asset_count: number;
  strengths: string[];
  weaknesses: string[];
  top_players: PostAuctionTeamTopPlayer[];
}

export interface BestValueBuyItem {
  player_name: string;
  team_name: string;
  sold_price: number;
  overall_score: number;
  value_index: number;
}

export interface PostAuctionAnalysisResponse {
  teams: PostAuctionTeamItem[];
  contender_team_names: string[];
  average_team_overall: number;
  best_value_buys: BestValueBuyItem[];
}

export function getApiBaseUrl() {
  return apiBaseUrl;
}

export async function fetchHistoricalStatus(): Promise<HistoricalDatasetStatusItem[]> {
  const response = await fetch(`${apiBaseUrl}/api/historical-data/status`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load historical data status.");
  }

  const data = (await response.json()) as { items: HistoricalDatasetStatusItem[] };
  return data.items;
}

export async function uploadHistoricalFile(
  datasetType: string,
  file: File,
): Promise<HistoricalUploadResult> {
  const formData = new FormData();
  formData.append("dataset_type", datasetType);
  formData.append("file", file);

  const response = await fetch(`${apiBaseUrl}/api/historical-data/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "Failed to upload historical file.");
  }

  return (await response.json()) as HistoricalUploadResult;
}

export async function processHistoricalScores(): Promise<ScoreProcessingResult> {
  const response = await fetch(`${apiBaseUrl}/api/scoring/process`, {
    method: "POST",
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "Failed to process scores.");
  }

  return (await response.json()) as ScoreProcessingResult;
}

export async function fetchPlayerDatabase(): Promise<PlayerDatabaseItem[]> {
  const response = await fetch(`${apiBaseUrl}/api/players`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load player database.");
  }

  const data = (await response.json()) as { items: PlayerDatabaseItem[] };
  return data.items;
}

export async function fetchPlayerDetail(playerId: number): Promise<PlayerDetail> {
  const response = await fetch(`${apiBaseUrl}/api/players/${playerId}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load player detail.");
  }

  return (await response.json()) as PlayerDetail;
}

export async function fetchAuctionSetup(): Promise<AuctionSettingsResponse> {
  const response = await fetch(`${apiBaseUrl}/api/auction-setup`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load auction setup.");
  }

  return (await response.json()) as AuctionSettingsResponse;
}

export async function saveAuctionSetup(
  payload: AuctionSettingsResponse,
): Promise<AuctionSettingsResponse> {
  const response = await fetch(`${apiBaseUrl}/api/auction-setup/settings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "Failed to save auction setup.");
  }

  return (await response.json()) as AuctionSettingsResponse;
}

export async function fetchPlayerOptions(): Promise<PlayerOptionItem[]> {
  const response = await fetch(`${apiBaseUrl}/api/auction-setup/player-options`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load player options.");
  }

  const data = (await response.json()) as { items: PlayerOptionItem[] };
  return data.items;
}

export async function fetchCurrentPlayerPoolStatus(): Promise<CurrentPlayerPoolStatusResponse> {
  const response = await fetch(`${apiBaseUrl}/api/auction-setup/player-pool/status`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load current player pool status.");
  }

  return (await response.json()) as CurrentPlayerPoolStatusResponse;
}

export async function uploadCurrentPlayerPool(
  file: File,
): Promise<CurrentPlayerPoolUploadResult> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${apiBaseUrl}/api/auction-setup/player-pool/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "Failed to upload current player pool.");
  }

  return (await response.json()) as CurrentPlayerPoolUploadResult;
}

export async function fetchLiveAuctionState(): Promise<LiveAuctionStateResponse> {
  const response = await fetch(`${apiBaseUrl}/api/live-auction/state`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load live auction state.");
  }

  return (await response.json()) as LiveAuctionStateResponse;
}

export async function submitLiveAuctionEvent(
  payload: SubmitLiveAuctionEventRequest,
): Promise<{ message: string }> {
  const response = await fetch(`${apiBaseUrl}/api/live-auction/events`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "Failed to save live auction event.");
  }

  return (await response.json()) as { message: string };
}

export async function resetLiveAuction(): Promise<{ message: string }> {
  const response = await fetch(`${apiBaseUrl}/api/live-auction/reset`, {
    method: "POST",
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "Failed to reset live auction.");
  }

  return (await response.json()) as { message: string };
}

export async function fetchBidRecommendation(playerId: number): Promise<BidRecommendation> {
  const response = await fetch(`${apiBaseUrl}/api/live-auction/recommendation/${playerId}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(errorBody || "Failed to load bid recommendation.");
  }

  return (await response.json()) as BidRecommendation;
}

export async function fetchTeamBuilderData(): Promise<TeamBuilderResponse> {
  const response = await fetch(`${apiBaseUrl}/api/team-builder`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load team builder data.");
  }

  return (await response.json()) as TeamBuilderResponse;
}

export async function fetchPostAuctionAnalysis(): Promise<PostAuctionAnalysisResponse> {
  const response = await fetch(`${apiBaseUrl}/api/post-auction-analysis`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load post-auction analysis.");
  }

  return (await response.json()) as PostAuctionAnalysisResponse;
}
