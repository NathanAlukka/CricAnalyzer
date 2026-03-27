import type { BestValueBuyItem, PostAuctionTeamItem } from "@/lib/api";

interface PostAuctionAnalysisPanelProps {
  teams: PostAuctionTeamItem[];
  bestValueBuys: BestValueBuyItem[];
}

export function PostAuctionAnalysisPanel({
  teams,
  bestValueBuys,
}: PostAuctionAnalysisPanelProps) {
  return (
    <div className="space-y-8">
      <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-semibold text-slate-900">Team Breakdown</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          Each team is compared using the same batting, bowling, fielding, and overall score totals.
        </p>

        <div className="mt-6 space-y-5">
          {teams.map((team) => (
            <article key={team.team_id} className="rounded-2xl border border-slate-200 p-5">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                <div>
                  <h3 className="text-xl font-semibold text-slate-900">{team.team_name}</h3>
                  <p className="mt-1 text-sm text-slate-600">
                    Owner: {team.owner_name || "Not set"} | Players: {team.players_count} | Remaining budget:{" "}
                    {team.remaining_budget.toFixed(2)}
                  </p>
                </div>
                <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                  <div className="rounded-2xl bg-sky-50 px-4 py-3 text-sm text-sky-950">Batting: {team.batting_total.toFixed(2)}</div>
                  <div className="rounded-2xl bg-emerald-50 px-4 py-3 text-sm text-emerald-950">Bowling: {team.bowling_total.toFixed(2)}</div>
                  <div className="rounded-2xl bg-amber-50 px-4 py-3 text-sm text-amber-950">Fielding: {team.fielding_total.toFixed(2)}</div>
                  <div className="rounded-2xl bg-slate-100 px-4 py-3 text-sm font-semibold text-slate-950">Overall: {team.overall_total.toFixed(2)}</div>
                </div>
              </div>

              <div className="mt-5 grid gap-4 md:grid-cols-3">
                <div className="rounded-2xl bg-slate-50 p-4">
                  <p className="text-sm font-semibold text-slate-900">Role counts</p>
                  <p className="mt-2 text-sm text-slate-700">Batters: {team.batter_count}</p>
                  <p className="text-sm text-slate-700">Bowlers: {team.bowler_count}</p>
                  <p className="text-sm text-slate-700">All-rounders: {team.all_rounder_count}</p>
                  <p className="text-sm text-slate-700">Good fielders: {team.fielding_asset_count}</p>
                </div>
                <div className="rounded-2xl bg-emerald-50 p-4">
                  <p className="text-sm font-semibold text-emerald-950">Strengths</p>
                  <ul className="mt-2 space-y-1 text-sm text-emerald-900">
                    {team.strengths.map((strength) => (
                      <li key={strength}>{strength}</li>
                    ))}
                  </ul>
                </div>
                <div className="rounded-2xl bg-amber-50 p-4">
                  <p className="text-sm font-semibold text-amber-950">Weaknesses</p>
                  <ul className="mt-2 space-y-1 text-sm text-amber-900">
                    {team.weaknesses.map((weakness) => (
                      <li key={weakness}>{weakness}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="mt-5 rounded-2xl bg-slate-50 p-4">
                <p className="text-sm font-semibold text-slate-900">Top players by overall score</p>
                <div className="mt-2 flex flex-wrap gap-3 text-sm text-slate-700">
                  {team.top_players.length === 0 ? (
                    <span>No scored players yet.</span>
                  ) : (
                    team.top_players.map((player) => (
                      <span key={`${team.team_id}-${player.player_name}`} className="rounded-full bg-white px-3 py-2 shadow-sm">
                        {player.player_name} ({player.overall_score.toFixed(2)})
                      </span>
                    ))
                  )}
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-semibold text-slate-900">Best Value Buys</h2>
        <p className="mt-2 text-sm leading-6 text-slate-600">
          Value index is overall score divided by sold price. Higher usually means a better bargain.
        </p>

        <div className="mt-6 overflow-x-auto rounded-2xl border border-slate-200">
          <table className="min-w-full border-collapse text-left text-sm">
            <thead className="bg-slate-100 text-slate-700">
              <tr>
                <th className="px-4 py-3 font-semibold">Player</th>
                <th className="px-4 py-3 font-semibold">Team</th>
                <th className="px-4 py-3 font-semibold">Sold price</th>
                <th className="px-4 py-3 font-semibold">Overall score</th>
                <th className="px-4 py-3 font-semibold">Value index</th>
              </tr>
            </thead>
            <tbody>
              {bestValueBuys.length === 0 ? (
                <tr>
                  <td className="px-4 py-4 text-slate-500" colSpan={5}>
                    No sold-player price data yet. Finish more of the auction to unlock this section.
                  </td>
                </tr>
              ) : (
                bestValueBuys.map((item) => (
                  <tr key={`${item.team_name}-${item.player_name}`} className="border-t border-slate-200 text-slate-700">
                    <td className="px-4 py-3 font-medium text-slate-900">{item.player_name}</td>
                    <td className="px-4 py-3">{item.team_name}</td>
                    <td className="px-4 py-3">{item.sold_price.toFixed(2)}</td>
                    <td className="px-4 py-3">{item.overall_score.toFixed(2)}</td>
                    <td className="px-4 py-3 font-semibold text-slate-900">{item.value_index.toFixed(3)}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
