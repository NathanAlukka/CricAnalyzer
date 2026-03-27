import Link from "next/link";

import { PlayerDatabaseTable } from "@/components/player-database-table";
import { fetchPlayerDatabase } from "@/lib/api";

export default async function PlayersPage() {
  let players = [];

  try {
    players = await fetchPlayerDatabase();
  } catch {
    players = [];
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-12">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-brand-700">Scored Players</p>
          <h1 className="mt-3 text-4xl font-bold tracking-tight text-slate-900">
            Player Database
          </h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">
            This page lists every player currently available in the merged score table.
            Click any player name to open the full detail view.
          </p>
        </div>
        <Link
          className="rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm font-semibold text-slate-900 transition hover:bg-slate-100"
          href="/"
        >
          Back to dashboard
        </Link>
      </div>

      <section className="mt-10">
        <PlayerDatabaseTable players={players} />
      </section>
    </main>
  );
}
