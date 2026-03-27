import Link from "next/link";

import { MetricComparisonSummary } from "@/components/metric-comparison-summary";
import { PlayerMetricComparisonChart } from "@/components/player-metric-comparison-chart";
import { PlayerProfileChart } from "@/components/player-profile-chart";
import { PlayerScoreCards } from "@/components/player-score-cards";
import { PlayerVsAverageChart } from "@/components/player-vs-average-chart";
import { fetchPlayerDetail } from "@/lib/api";

interface PlayerPageProps {
  params: {
    playerId: string;
  };
}

export default async function PlayerDetailPage({ params }: PlayerPageProps) {
  const player = await fetchPlayerDetail(Number(params.playerId));
  const scoreSummaryItems = [
    {
      label: "Batting",
      playerValue: player.batting_score,
      averageValue: player.average_scores.batting_score,
    },
    {
      label: "Bowling",
      playerValue: player.bowling_score,
      averageValue: player.average_scores.bowling_score,
    },
    {
      label: "Fielding",
      playerValue: player.fielding_score,
      averageValue: player.average_scores.fielding_score,
    },
    {
      label: "Overall",
      playerValue: player.overall_score,
      averageValue: player.average_scores.overall_score,
    },
  ];
  const battingComparisonItems = [
    {
      label: "Runs",
      playerValue: player.batting_stats?.runs ?? 0,
      averageValue: player.batting_average_stats?.runs ?? 0,
    },
    {
      label: "Average",
      playerValue: player.batting_stats?.average ?? 0,
      averageValue: player.batting_average_stats?.average ?? 0,
    },
    {
      label: "Strike Rate",
      playerValue: player.batting_stats?.strike_rate ?? 0,
      averageValue: player.batting_average_stats?.strike_rate ?? 0,
    },
    {
      label: "4s",
      playerValue: player.batting_stats?.fours ?? 0,
      averageValue: player.batting_average_stats?.fours ?? 0,
    },
  ];
  const bowlingComparisonItems = [
    {
      label: "Wickets",
      playerValue: player.bowling_stats?.wickets ?? 0,
      averageValue: player.bowling_average_stats?.wickets ?? 0,
    },
    {
      label: "Average",
      playerValue: player.bowling_stats?.average ?? 0,
      averageValue: player.bowling_average_stats?.average ?? 0,
    },
    {
      label: "Economy",
      playerValue: player.bowling_stats?.economy ?? 0,
      averageValue: player.bowling_average_stats?.economy ?? 0,
    },
  ];
  const fieldingComparisonItems = [
    {
      label: "Catches",
      playerValue: player.fielding_stats?.catches ?? 0,
      averageValue: player.fielding_average_stats?.catches ?? 0,
    },
    {
      label: "Direct RO",
      playerValue: player.fielding_stats?.direct_run_outs ?? 0,
      averageValue: player.fielding_average_stats?.direct_run_outs ?? 0,
    },
    {
      label: "Indirect RO",
      playerValue: player.fielding_stats?.indirect_run_outs ?? 0,
      averageValue: player.fielding_average_stats?.indirect_run_outs ?? 0,
    },
  ];

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-12">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-brand-700">Player Detail</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">{player.name}</h1>
          <p className="mt-3 text-sm leading-6 text-slate-600">
            Role hint: <span className="font-semibold capitalize text-slate-900">{player.role_hint}</span>
          </p>
          <p className="text-sm leading-6 text-slate-600">
            Team: <span className="font-semibold text-slate-900">{player.team_name ?? "-"}</span>
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Link
            className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100"
            href="/players"
          >
            Back to players
          </Link>
          <Link
            className="rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-700"
            href="/"
          >
            Go to dashboard
          </Link>
        </div>
      </div>

      <section className="mt-10">
        <PlayerScoreCards
          battingScore={player.batting_score}
          bowlingScore={player.bowling_score}
          fieldingScore={player.fielding_score}
          overallScore={player.overall_score}
        />
      </section>

      <section className="mt-10 grid gap-6 lg:grid-cols-2">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">Score Profile</h2>
          <div className="mt-6 h-[320px]">
            <PlayerProfileChart
              battingScore={player.batting_score}
              bowlingScore={player.bowling_score}
              fieldingScore={player.fielding_score}
              overallScore={player.overall_score}
            />
          </div>
          <MetricComparisonSummary items={scoreSummaryItems.map((item) => ({ ...item, averageValue: undefined }))} />
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-slate-900">Player vs Average</h2>
          <div className="mt-6 h-[320px]">
            <PlayerVsAverageChart
              playerScores={player.player_scores}
              averageScores={player.average_scores}
            />
          </div>
          <MetricComparisonSummary items={scoreSummaryItems} />
        </div>
      </section>

      <section className="mt-10 grid gap-6 lg:grid-cols-3">
        {battingComparisonItems.map((item) => (
          <div key={`batting-${item.label}`} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">Batting: {item.label}</h2>
            <div className="mt-6 h-[240px]">
              <PlayerMetricComparisonChart
                label={item.label}
                playerValue={item.playerValue}
                averageValue={item.averageValue}
              />
            </div>
            <MetricComparisonSummary items={[item]} />
          </div>
        ))}

        {bowlingComparisonItems.map((item) => (
          <div key={`bowling-${item.label}`} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">Bowling: {item.label}</h2>
            <div className="mt-6 h-[240px]">
              <PlayerMetricComparisonChart
                label={item.label}
                playerValue={item.playerValue}
                averageValue={item.averageValue}
              />
            </div>
            <MetricComparisonSummary items={[item]} />
          </div>
        ))}

        {fieldingComparisonItems.map((item) => (
          <div key={`fielding-${item.label}`} className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-900">Fielding: {item.label}</h2>
            <div className="mt-6 h-[240px]">
              <PlayerMetricComparisonChart
                label={item.label}
                playerValue={item.playerValue}
                averageValue={item.averageValue}
              />
            </div>
            <MetricComparisonSummary items={[item]} />
          </div>
        ))}
      </section>

      <section className="mt-10 grid gap-6 lg:grid-cols-3">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Batting Stats</h2>
          <div className="mt-4 space-y-2 text-sm text-slate-700">
            <p>Matches: {player.batting_stats?.matches ?? "-"}</p>
            <p>Runs: {player.batting_stats?.runs ?? "-"}</p>
            <p>Average: {player.batting_stats?.average ?? "-"}</p>
            <p>Strike Rate: {player.batting_stats?.strike_rate ?? "-"}</p>
            <p>4s: {player.batting_stats?.fours ?? "-"}</p>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Bowling Stats</h2>
          <div className="mt-4 space-y-2 text-sm text-slate-700">
            <p>Matches: {player.bowling_stats?.matches ?? "-"}</p>
            <p>Wickets: {player.bowling_stats?.wickets ?? "-"}</p>
            <p>Average: {player.bowling_stats?.average ?? "-"}</p>
            <p>Economy: {player.bowling_stats?.economy ?? "-"}</p>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900">Fielding Stats</h2>
          <div className="mt-4 space-y-2 text-sm text-slate-700">
            <p>Matches: {player.fielding_stats?.matches ?? "-"}</p>
            <p>Catches: {player.fielding_stats?.catches ?? "-"}</p>
            <p>Direct Run Outs: {player.fielding_stats?.direct_run_outs ?? "-"}</p>
            <p>Indirect Run Outs: {player.fielding_stats?.indirect_run_outs ?? "-"}</p>
          </div>
        </div>
      </section>
    </main>
  );
}
