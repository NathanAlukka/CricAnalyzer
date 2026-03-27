"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

import type { LiveAuctionStateResponse } from "@/lib/api";
import { fetchLiveAuctionState, resetLiveAuction, submitLiveAuctionEvent } from "@/lib/api";

interface LiveAuctionPanelProps {
  initialState: LiveAuctionStateResponse;
}

export function LiveAuctionPanel({ initialState }: LiveAuctionPanelProps) {
  const [state, setState] = useState(initialState);
  const [selectedPlayerId, setSelectedPlayerId] = useState(initialState.remaining_pool[0]?.player_id ? String(initialState.remaining_pool[0].player_id) : "");
  const [eventType, setEventType] = useState("bought_by_me");
  const [teamId, setTeamId] = useState("");
  const [finalPrice, setFinalPrice] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isResetting, setIsResetting] = useState(false);
  const [resultMessage, setResultMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const selectedPlayer = useMemo(
    () => state.remaining_pool.find((player) => String(player.player_id) === selectedPlayerId) ?? null,
    [selectedPlayerId, state.remaining_pool],
  );

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSubmitting(true);
    setResultMessage(null);
    setErrorMessage(null);

    try {
      if (!selectedPlayerId) {
        throw new Error("Select a player first.");
      }

      const payload = {
        player_id: Number(selectedPlayerId),
        event_type: eventType,
        team_id: eventType === "bought_by_other" && teamId ? Number(teamId) : null,
        final_price: eventType === "unsold" || finalPrice === "" ? null : Number(finalPrice),
        notes: null,
      };

      await submitLiveAuctionEvent(payload);
      const nextState = await fetchLiveAuctionState();
      setState(nextState);
      setSelectedPlayerId(nextState.remaining_pool[0]?.player_id ? String(nextState.remaining_pool[0].player_id) : "");
      setFinalPrice("");
      setTeamId("");
      setResultMessage("Auction event saved.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Failed to save auction event.");
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleResetAuction() {
    setIsResetting(true);
    setResultMessage(null);
    setErrorMessage(null);

    try {
      await resetLiveAuction();
      const nextState = await fetchLiveAuctionState();
      setState(nextState);
      setSelectedPlayerId(nextState.remaining_pool[0]?.player_id ? String(nextState.remaining_pool[0].player_id) : "");
      setFinalPrice("");
      setTeamId("");
      setResultMessage("Auction reset complete.");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Failed to reset auction.");
    } finally {
      setIsResetting(false);
    }
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">Live Auction Control</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Select the current player, record the result, and keep budgets and rosters updated.
          </p>
        </div>
        <button className="rounded-xl border border-rose-300 bg-rose-50 px-4 py-3 text-sm font-semibold text-rose-900 transition hover:bg-rose-100 disabled:cursor-not-allowed disabled:opacity-60" disabled={isResetting} onClick={handleResetAuction} type="button">
          {isResetting ? "Resetting..." : "Reset auction"}
        </button>
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <form className="space-y-5" onSubmit={handleSubmit}>
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            Current player
            <select className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" value={selectedPlayerId} onChange={(event) => setSelectedPlayerId(event.target.value)}>
              <option value="">Select player from remaining pool</option>
              {state.remaining_pool.map((player) => (
                <option key={player.player_id} value={player.player_id}>
                  {player.player_name}
                </option>
              ))}
            </select>
            {state.remaining_pool.length === 0 ? (
              <span className="text-xs font-normal text-slate-500">
                No available players are in the live pool yet. Upload the current player pool on the auction setup page, or reset the auction if all players were already processed.
              </span>
            ) : null}
          </label>

          <div className="grid gap-4 md:grid-cols-3">
            <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
              Result
              <select className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" value={eventType} onChange={(event) => setEventType(event.target.value)}>
                <option value="bought_by_me">Bought by me</option>
                <option value="bought_by_other">Bought by another team</option>
                <option value="unsold">Unsold</option>
              </select>
            </label>

            <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
              Team
              <select className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" disabled={eventType !== "bought_by_other"} value={teamId} onChange={(event) => setTeamId(event.target.value)}>
                <option value="">Select team</option>
                {state.teams.filter((team) => !team.is_my_team).map((team) => (
                  <option key={team.team_id} value={team.team_id}>
                    {team.team_name}
                  </option>
                ))}
              </select>
            </label>

            <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
              Final price
              <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" disabled={eventType === "unsold"} min={0} step="0.01" type="number" value={finalPrice} onChange={(event) => setFinalPrice(event.target.value)} />
            </label>
          </div>

          <button className="rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Saving..." : "Save auction event"}
          </button>

          {resultMessage ? <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">{resultMessage}</div> : null}
          {errorMessage ? <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-900">{errorMessage}</div> : null}
        </form>

        <div className="rounded-2xl bg-slate-50 p-5">
          <h3 className="text-lg font-semibold text-slate-900">Current Player Summary</h3>
          {selectedPlayer ? (
            <div className="mt-4 space-y-2 text-sm text-slate-700">
              <p className="text-base font-semibold text-slate-900">{selectedPlayer.player_name}</p>
              <p>Role: <span className="font-semibold capitalize">{selectedPlayer.role_hint}</span></p>
              <p>Batting score: <span className="font-semibold">{selectedPlayer.batting_score.toFixed(2)}</span></p>
              <p>Bowling score: <span className="font-semibold">{selectedPlayer.bowling_score.toFixed(2)}</span></p>
              <p>Fielding score: <span className="font-semibold">{selectedPlayer.fielding_score.toFixed(2)}</span></p>
              <p>Overall score: <span className="font-semibold">{selectedPlayer.overall_score.toFixed(2)}</span></p>
              <p>Reserve price: <span className="font-semibold">{selectedPlayer.reserve_price ?? "-"}</span></p>
              <p>Captain in pool: <span className="font-semibold">{selectedPlayer.is_captain ? "Yes" : "No"}</span></p>
              <Link className="inline-flex rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href={`/players/${selectedPlayer.player_id}`}>
                Open full player detail
              </Link>
            </div>
          ) : (
            <p className="mt-4 text-sm text-slate-600">Select a player to see their summary.</p>
          )}
        </div>
      </div>

      <section className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-sm text-slate-600">Players left in pool</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{state.remaining_pool.length}</p>
        </div>
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-sm text-slate-600">My team budget</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{state.my_team_summary?.remaining_budget ?? 0}</p>
        </div>
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-sm text-slate-600">Players bought</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{state.my_team_summary?.players_bought ?? 0}</p>
        </div>
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="text-sm text-slate-600">Open slots</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{state.my_team_summary?.open_slots ?? 0}</p>
        </div>
      </section>

      <section className="mt-8 rounded-2xl border border-slate-200">
        <div className="border-b border-slate-200 bg-slate-50 px-4 py-3">
          <h3 className="text-lg font-semibold text-slate-900">Team Budgets</h3>
        </div>
        <div className="divide-y divide-slate-200">
          {state.teams.map((team) => (
            <div key={team.team_id} className="flex items-center justify-between px-4 py-3 text-sm text-slate-700">
              <div>
                <p className="font-semibold text-slate-900">{team.team_name}</p>
                <p>{team.players_bought} players bought</p>
              </div>
              <div className="text-right">
                <p className="font-semibold text-slate-900">{team.remaining_budget.toFixed(2)}</p>
                <p>{team.is_my_team ? "My team" : team.owner_name ?? "Other team"}</p>
              </div>
            </div>
          ))}
        </div>
      </section>
    </section>
  );
}
