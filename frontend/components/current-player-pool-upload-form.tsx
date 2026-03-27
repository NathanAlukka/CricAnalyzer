"use client";

import { useRef, useState } from "react";

import type { CurrentPlayerPoolStatusResponse, CurrentPlayerPoolUploadResult } from "@/lib/api";
import { uploadCurrentPlayerPool } from "@/lib/api";

interface CurrentPlayerPoolUploadFormProps {
  initialStatus: CurrentPlayerPoolStatusResponse;
}

export function CurrentPlayerPoolUploadForm({ initialStatus }: CurrentPlayerPoolUploadFormProps) {
  const formRef = useRef<HTMLFormElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [status, setStatus] = useState(initialStatus);
  const [result, setResult] = useState<CurrentPlayerPoolUploadResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setErrorMessage("Choose a player pool Excel file before uploading.");
      return;
    }

    setIsUploading(true);
    setErrorMessage(null);

    try {
      const uploadResult = await uploadCurrentPlayerPool(selectedFile);
      setResult(uploadResult);
      setStatus({
        rows_loaded: uploadResult.rows_saved,
        captains_loaded: uploadResult.captains_marked,
      });
      setSelectedFile(null);
      formRef.current?.reset();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Failed to upload player pool.");
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <h2 className="text-2xl font-semibold text-slate-900">Current Player Pool Upload</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">
        Upload the current auction pool. The file only needs a player name column. Optional columns like captain, reserve price, and auction order are supported.
      </p>

      <form ref={formRef} className="mt-6 grid gap-4 md:grid-cols-[1fr_auto]" onSubmit={handleSubmit}>
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Player pool Excel file
          <input accept=".xlsx,.xls" className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" type="file" onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)} />
        </label>
        <button className="mt-auto rounded-xl bg-brand-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-brand-900 disabled:cursor-not-allowed disabled:bg-slate-400" disabled={isUploading} type="submit">
          {isUploading ? "Uploading..." : "Upload player pool"}
        </button>
      </form>

      <div className="mt-6 rounded-2xl bg-slate-50 p-4 text-sm text-slate-700">
        <p>Pool rows loaded: <span className="font-semibold">{status.rows_loaded}</span></p>
        <p className="mt-1">Captains marked in pool: <span className="font-semibold">{status.captains_loaded}</span></p>
      </div>

      {result ? (
        <div className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">
          <p className="font-semibold">Current player pool uploaded successfully.</p>
          <p className="mt-2">File: {result.source_file}</p>
          <p>Rows read: {result.rows_read}</p>
          <p>Rows saved: {result.rows_saved}</p>
          <p>Players created: {result.players_created}</p>
          <p>Captains marked: {result.captains_marked}</p>
          {result.missing_columns.length > 0 ? <p>Missing columns: {result.missing_columns.join(", ")}</p> : null}
        </div>
      ) : null}

      {errorMessage ? <div className="mt-6 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-900">{errorMessage}</div> : null}
    </section>
  );
}
