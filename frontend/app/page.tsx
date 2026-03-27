import Link from "next/link";

import { HistoricalUploadForm } from "@/components/historical-upload-form";
import { ProcessScoresPanel } from "@/components/process-scores-panel";
import { StatusCard } from "@/components/status-card";
import { fetchHistoricalStatus, getApiBaseUrl } from "@/lib/api";

export default async function HomePage() {
  let statusItems = [
    { dataset_type: "batting", rows_loaded: 0, loaded: false },
    { dataset_type: "bowling", rows_loaded: 0, loaded: false },
    { dataset_type: "fielding", rows_loaded: 0, loaded: false },
  ];

  try {
    statusItems = await fetchHistoricalStatus();
  } catch {
    // The dashboard should still render even if the backend is not reachable yet.
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-12">
      <section className="rounded-3xl bg-slate-950 px-8 py-10 text-white shadow-xl">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-brand-100">
              Cricket Auction Assistant
            </p>
            <h1 className="mt-4 max-w-3xl text-4xl font-bold tracking-tight sm:text-5xl">
              Load your historical data first, then turn it into transparent player scores.
            </h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-300">
              The dashboard now supports uploads, score processing, and a scored player database page.
            </p>
            <div className="mt-6 inline-flex rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200">
              Backend API target: {getApiBaseUrl()}
            </div>
          </div>

          <div className="flex flex-col gap-3">
            <Link
              className="rounded-xl bg-brand-500 px-4 py-3 text-sm font-semibold text-white transition hover:bg-brand-700"
              href="/players"
            >
              Open player database
            </Link>
            <Link
              className="rounded-xl border border-white/20 bg-white/10 px-4 py-3 text-sm font-semibold text-white transition hover:bg-white/20"
              href="/auction-setup"
            >
              Open auction setup
            </Link>
            <Link
              className="rounded-xl border border-white/20 bg-white/10 px-4 py-3 text-sm font-semibold text-white transition hover:bg-white/20"
              href="/live-auction"
            >
              Open live auction
            </Link>
          </div>
        </div>
      </section>

      <section className="mt-10 grid gap-4 md:grid-cols-3">
        {statusItems.map((item) => (
          <StatusCard
            key={item.dataset_type}
            title={`${item.dataset_type.charAt(0).toUpperCase()}${item.dataset_type.slice(1)} Data`}
            status={item.loaded ? "Loaded" : "Not loaded"}
            description={`Rows currently stored: ${item.rows_loaded}`}
          />
        ))}
      </section>

      <section className="mt-10">
        <HistoricalUploadForm initialStatus={statusItems} />
      </section>

      <section className="mt-10">
        <ProcessScoresPanel />
      </section>

      <section className="mt-10 rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
        <h2 className="text-2xl font-semibold text-slate-900">What this step adds</h2>
        <ul className="mt-4 space-y-2 text-sm leading-6 text-slate-700">
          <li>Score calculation endpoint in FastAPI</li>
          <li>Configurable batting, bowling, fielding, and overall weights</li>
          <li>Normalization logic for higher-is-better and lower-is-better metrics</li>
          <li>Merged player score storage with simple role hints</li>
          <li>A dedicated player database page</li>
          <li>An auction setup page for rules, teams, captains, and player pool upload</li>
          <li>A live auction page for event logging, budget tracking, and sold/unsold updates</li>
        </ul>
      </section>
    </main>
  );
}
