import Link from "next/link";

import { PostAuctionAnalysisPanel } from "@/components/post-auction-analysis-panel";
import { TeamComparisonBarChart } from "@/components/team-comparison-bar-chart";
import { fetchPostAuctionAnalysis, type PostAuctionAnalysisResponse } from "@/lib/api";

export default async function PostAuctionAnalysisPage() {
  let data: PostAuctionAnalysisResponse = {
    teams: [],
    contender_team_names: [],
    average_team_overall: 0,
    best_value_buys: [],
  };
  let loadError: string | null = null;

  try {
    data = await fetchPostAuctionAnalysis();
  } catch (error) {
    loadError = error instanceof Error ? error.message : "Failed to load post-auction analysis.";
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-12">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-brand-700">Step 11</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">Post-Auction Analysis</h1>
          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            Compare all teams after the auction, spot likely contenders, and review where the best bargains landed. This first version reads the teams already saved from auction setup plus live auction results.
          </p>
        </div>
        <div className="flex gap-3">
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/">
            Back to dashboard
          </Link>
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/live-auction">
            Live auction
          </Link>
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/team-builder">
            Team builder
          </Link>
        </div>
      </div>

      {loadError ? (
        <div className="mt-10 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-900">
          {loadError}
        </div>
      ) : null}

      <section className="mt-10 grid gap-4 md:grid-cols-3">
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-600">Teams analyzed</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{data.teams.length}</p>
        </div>
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-600">Average team overall</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{data.average_team_overall.toFixed(2)}</p>
        </div>
        <div className="rounded-2xl bg-white p-5 shadow-sm">
          <p className="text-sm text-slate-600">Likely contenders</p>
          <p className="mt-2 text-xl font-bold text-slate-900">
            {data.contender_team_names.length > 0 ? data.contender_team_names.join(", ") : "Not enough data yet"}
          </p>
        </div>
      </section>

      <section className="mt-10 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-semibold text-slate-900">Team Comparison Chart</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          This chart keeps the numeric totals visible by category so you can compare batting, bowling, fielding, and overall depth side by side.
        </p>
        <div className="mt-6 h-[420px]">
          <TeamComparisonBarChart teams={data.teams} />
        </div>
        <div className="mt-6 overflow-x-auto rounded-2xl border border-slate-200">
          <table className="min-w-full border-collapse text-left text-sm">
            <thead className="bg-slate-100 text-slate-700">
              <tr>
                <th className="px-4 py-3 font-semibold">Team</th>
                <th className="px-4 py-3 font-semibold">Batting</th>
                <th className="px-4 py-3 font-semibold">Bowling</th>
                <th className="px-4 py-3 font-semibold">Fielding</th>
                <th className="px-4 py-3 font-semibold">Overall</th>
              </tr>
            </thead>
            <tbody>
              {data.teams.map((team) => (
                <tr key={team.team_id} className="border-t border-slate-200 text-slate-700">
                  <td className="px-4 py-3 font-medium text-slate-900">{team.team_name}</td>
                  <td className="px-4 py-3">{team.batting_total.toFixed(2)}</td>
                  <td className="px-4 py-3">{team.bowling_total.toFixed(2)}</td>
                  <td className="px-4 py-3">{team.fielding_total.toFixed(2)}</td>
                  <td className="px-4 py-3 font-semibold text-slate-900">{team.overall_total.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mt-10">
        <PostAuctionAnalysisPanel bestValueBuys={data.best_value_buys} teams={data.teams} />
      </section>
    </main>
  );
}
