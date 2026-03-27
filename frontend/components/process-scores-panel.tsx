"use client";

import { useState } from "react";

import { processHistoricalScores, type ScoreProcessingResult } from "@/lib/api";

export function ProcessScoresPanel() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<ScoreProcessingResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleProcessScores() {
    setIsProcessing(true);
    setErrorMessage(null);

    try {
      const processResult = await processHistoricalScores();
      setResult(processResult);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Failed to process scores.");
    } finally {
      setIsProcessing(false);
    }
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <h2 className="text-2xl font-semibold text-slate-900">Process Player Scores</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">
        This step reads the uploaded batting, bowling, and fielding data, then creates
        merged player scores out of 10.
      </p>

      <button
        className="mt-6 rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
        disabled={isProcessing}
        onClick={handleProcessScores}
        type="button"
      >
        {isProcessing ? "Processing..." : "Process and merge scores"}
      </button>

      {result ? (
        <div className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">
          <p className="font-semibold">Scores processed successfully.</p>
          <p className="mt-2">Players processed: {result.players_processed}</p>
          <p>Scores created: {result.scores_created}</p>
          <p>Scoring version: {result.scoring_version}</p>
        </div>
      ) : null}

      {errorMessage ? (
        <div className="mt-6 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-900">
          {errorMessage}
        </div>
      ) : null}
    </section>
  );
}
