import Link from "next/link";

import { AuctionSettingsForm } from "@/components/auction-settings-form";
import { CurrentPlayerPoolUploadForm } from "@/components/current-player-pool-upload-form";
import {
  type AuctionSettingsResponse,
  type CurrentPlayerPoolStatusResponse,
  type PlayerOptionItem,
  fetchAuctionSetup,
  fetchCurrentPlayerPoolStatus,
  fetchPlayerOptions,
} from "@/lib/api";

export default async function AuctionSetupPage() {
  let settings: AuctionSettingsResponse = {
    tournament_name: "Cricket Auction",
    number_of_teams: 6,
    squad_size: 12,
    total_points_per_captain: 100,
    captain_self_value_deduction: 0,
    max_bid: 25,
    teams: [],
  };
  let playerOptions: PlayerOptionItem[] = [];
  let poolStatus: CurrentPlayerPoolStatusResponse = {
    rows_loaded: 0,
    captains_loaded: 0,
  };

  try {
    [settings, playerOptions, poolStatus] = await Promise.all([
      fetchAuctionSetup(),
      fetchPlayerOptions(),
      fetchCurrentPlayerPoolStatus(),
    ]);
  } catch {
    // The page should still render with defaults if the backend is unavailable.
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-12">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-brand-700">Step 7</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">Auction Setup</h1>
          <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
            Save the auction rules, define the teams and captains, and upload the current player pool before the live auction starts.
          </p>
        </div>
        <div className="flex gap-3">
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/">Back to dashboard</Link>
          <Link className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100" href="/players">Player database</Link>
          <Link className="rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-700" href="/live-auction">Live auction</Link>
        </div>
      </div>

      <section className="mt-10">
        <AuctionSettingsForm initialSettings={settings} playerOptions={playerOptions} />
      </section>

      <section className="mt-10">
        <CurrentPlayerPoolUploadForm initialStatus={poolStatus} />
      </section>
    </main>
  );
}
