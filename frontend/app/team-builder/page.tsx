import Link from "next/link";

import { TeamCompositionChart } from "@/components/team-composition-chart";
import { TeamRosterTable } from "@/components/team-roster-table";
import { fetchTeamBuilderData, type TeamBuilderResponse } from "@/lib/api";

export default async function TeamBuilderPage() {
  let data: TeamBuilderResponse = {
    summary: null,
    roster: [],
  };
  let loadError: string | null = null;

  try {
    data = await fetchTeamBuilderData();
  } catch (error) {
    loadError = error instanceof Error ? error.message : "Failed to load team builder data.";
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-12">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-brand-700">Step 10</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">Team Builder</h1>
          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            Review your current squad, budget, depth, and composition while the auction is running.
          </p>
        </div>
        <div className="flex gap-3">
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/">Back to dashboard</Link>
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/live-auction">Live auction</Link>
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/post-auction-analysis">Post-auction analysis</Link>
        </div>
      </div>

      {loadError ? (
        <div className="mt-10 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-900">
          {loadError}
        </div>
      ) : null}

      <section className="mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-600">Remaining budget</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{data.summary?.remaining_budget ?? 0}</p>
        </div>
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-600">Players bought</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{data.summary?.players_bought ?? 0}</p>
        </div>
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-600">Open slots</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{data.summary?.open_slots ?? 0}</p>
        </div>
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-600">Overall total</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{data.summary?.overall_total ?? 0}</p>
        </div>
      </section>

      <section className="mt-10 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-semibold text-slate-900">Team Composition</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Score-based role counts for your current squad.
          </p>
          <div className="mt-6 flex items-center justify-center">
            <div className="h-[320px] w-[320px]">
              <TeamCompositionChart
                batterCount={data.summary?.batter_count ?? 0}
                bowlerCount={data.summary?.bowler_count ?? 0}
                allRounderCount={data.summary?.all_rounder_count ?? 0}
                fieldingAssetCount={data.summary?.fielding_asset_count ?? 0}
              />
            </div>
          </div>
          <div className="mt-6 grid gap-3 md:grid-cols-2">
            <div className="rounded-2xl bg-slate-50 p-4"><p className="text-sm text-slate-600">Batters</p><p className="mt-1 text-xl font-bold text-slate-900">{data.summary?.batter_count ?? 0}</p></div>
            <div className="rounded-2xl bg-slate-50 p-4"><p className="text-sm text-slate-600">Bowlers</p><p className="mt-1 text-xl font-bold text-slate-900">{data.summary?.bowler_count ?? 0}</p></div>
            <div className="rounded-2xl bg-slate-50 p-4"><p className="text-sm text-slate-600">All-rounders</p><p className="mt-1 text-xl font-bold text-slate-900">{data.summary?.all_rounder_count ?? 0}</p></div>
            <div className="rounded-2xl bg-slate-50 p-4"><p className="text-sm text-slate-600">Good fielders</p><p className="mt-1 text-xl font-bold text-slate-900">{data.summary?.fielding_asset_count ?? 0}</p></div>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-semibold text-slate-900">Depth Totals</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Combined score depth across your current roster.
          </p>
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl bg-sky-50 p-5"><p className="text-sm text-sky-800">Batting total</p><p className="mt-2 text-3xl font-bold text-sky-950">{data.summary?.batting_total ?? 0}</p></div>
            <div className="rounded-2xl bg-emerald-50 p-5"><p className="text-sm text-emerald-800">Bowling total</p><p className="mt-2 text-3xl font-bold text-emerald-950">{data.summary?.bowling_total ?? 0}</p></div>
            <div className="rounded-2xl bg-amber-50 p-5"><p className="text-sm text-amber-800">Fielding total</p><p className="mt-2 text-3xl font-bold text-amber-950">{data.summary?.fielding_total ?? 0}</p></div>
            <div className="rounded-2xl bg-slate-100 p-5"><p className="text-sm text-slate-700">Team name</p><p className="mt-2 text-2xl font-bold text-slate-950">{data.summary?.team_name ?? "No team set"}</p></div>
          </div>
        </div>
      </section>

      <section className="mt-10">
        <TeamRosterTable roster={data.roster} />
      </section>
    </main>
  );
}
