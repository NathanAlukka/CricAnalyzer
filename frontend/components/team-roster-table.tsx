import Link from "next/link";

import type { TeamBuilderRosterItem } from "@/lib/api";

interface TeamRosterTableProps {
  roster: TeamBuilderRosterItem[];
}

export function TeamRosterTable({ roster }: TeamRosterTableProps) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <h2 className="text-2xl font-semibold text-slate-900">My Roster</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">
        Your current team, purchase prices, and player scores.
      </p>

      <div className="mt-6 overflow-x-auto rounded-2xl border border-slate-200">
        <table className="min-w-full border-collapse text-left text-sm">
          <thead className="bg-slate-100 text-slate-700">
            <tr>
              <th className="px-4 py-3 font-semibold">Player</th>
              <th className="px-4 py-3 font-semibold">Role</th>
              <th className="px-4 py-3 font-semibold">Source</th>
              <th className="px-4 py-3 font-semibold">Price</th>
              <th className="px-4 py-3 font-semibold">Batting</th>
              <th className="px-4 py-3 font-semibold">Bowling</th>
              <th className="px-4 py-3 font-semibold">Fielding</th>
              <th className="px-4 py-3 font-semibold">Overall</th>
            </tr>
          </thead>
          <tbody>
            {roster.length === 0 ? (
              <tr>
                <td className="px-4 py-4 text-slate-500" colSpan={8}>No players bought yet.</td>
              </tr>
            ) : (
              roster.map((player) => (
                <tr key={player.player_id} className="border-t border-slate-200 text-slate-700">
                  <td className="px-4 py-3 font-medium text-slate-900">
                    <Link className="hover:text-brand-700 hover:underline" href={`/players/${player.player_id}`}>
                      {player.player_name}
                    </Link>
                  </td>
                  <td className="px-4 py-3 capitalize">{player.role_hint}</td>
                  <td className="px-4 py-3">
                    {player.roster_status === "captain_retained" ? "Captain retained" : "Auction buy"}
                  </td>
                  <td className="px-4 py-3">{player.purchase_price ?? "-"}</td>
                  <td className="px-4 py-3">{player.batting_score.toFixed(2)}</td>
                  <td className="px-4 py-3">{player.bowling_score.toFixed(2)}</td>
                  <td className="px-4 py-3">{player.fielding_score.toFixed(2)}</td>
                  <td className="px-4 py-3 font-semibold text-slate-900">{player.overall_score.toFixed(2)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
