import Link from "next/link";

import { AuctionEventLog } from "@/components/auction-event-log";
import { LiveAuctionPanel } from "@/components/live-auction-panel";
import { fetchLiveAuctionState, type LiveAuctionStateResponse } from "@/lib/api";

export default async function LiveAuctionPage() {
  let state: LiveAuctionStateResponse = {
    remaining_pool: [],
    teams: [],
    my_team_summary: null,
    recent_events: [],
  };
  let loadError: string | null = null;

  try {
    state = await fetchLiveAuctionState();
  } catch (error) {
    loadError = error instanceof Error ? error.message : "Failed to load live auction state.";
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-12">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-brand-700">Step 8</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">Live Auction</h1>
          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            Record each player as they come up in the auction, update budgets, and track sold and unsold players live.
          </p>
        </div>
        <div className="flex gap-3">
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/">Back to dashboard</Link>
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/auction-setup">Auction setup</Link>
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/team-builder">Team builder</Link>
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/post-auction-analysis">Post-auction analysis</Link>
        </div>
      </div>

      <section className="mt-10">
        {loadError ? (
          <div className="mb-6 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-900">
            {loadError}
          </div>
        ) : null}
        <LiveAuctionPanel initialState={state} />
      </section>

      <section className="mt-10">
        <AuctionEventLog events={state.recent_events} />
      </section>
    </main>
  );
}
