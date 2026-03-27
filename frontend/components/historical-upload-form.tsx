"use client";

import { useMemo, useRef, useState } from "react";

import {
  type HistoricalDatasetStatusItem,
  type HistoricalUploadResult,
  uploadHistoricalFile,
} from "@/lib/api";

interface HistoricalUploadFormProps {
  initialStatus: HistoricalDatasetStatusItem[];
}

const datasetOptions = [
  { value: "batting", label: "Batting" },
  { value: "bowling", label: "Bowling" },
  { value: "fielding", label: "Fielding" },
];

export function HistoricalUploadForm({ initialStatus }: HistoricalUploadFormProps) {
  const formRef = useRef<HTMLFormElement>(null);
  const [datasetType, setDatasetType] = useState("batting");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [statusItems, setStatusItems] = useState(initialStatus);
  const [result, setResult] = useState<HistoricalUploadResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const activeStatus = useMemo(
    () => statusItems.find((item) => item.dataset_type === datasetType),
    [datasetType, statusItems],
  );

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setErrorMessage("Choose an Excel file before uploading.");
      return;
    }

    setIsUploading(true);
    setErrorMessage(null);

    try {
      const uploadResult = await uploadHistoricalFile(datasetType, selectedFile);
      setResult(uploadResult);
      setStatusItems((currentItems) =>
        currentItems.map((item) =>
          item.dataset_type === datasetType
            ? {
                ...item,
                loaded: uploadResult.rows_saved > 0,
                rows_loaded: uploadResult.rows_saved,
              }
            : item,
        ),
      );
      setSelectedFile(null);
      formRef.current?.reset();
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Upload failed.");
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <div className="flex flex-col gap-2">
        <h2 className="text-2xl font-semibold text-slate-900">Historical Excel Upload</h2>
        <p className="text-sm leading-6 text-slate-600">
          Upload one file at a time and tell the backend whether it is batting,
          bowling, or fielding data.
        </p>
      </div>

      <form
        ref={formRef}
        className="mt-6 grid gap-4 md:grid-cols-[180px_1fr_auto]"
        onSubmit={handleSubmit}
      >
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Dataset type
          <select
            className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3 outline-none ring-0"
            value={datasetType}
            onChange={(event) => setDatasetType(event.target.value)}
          >
            {datasetOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Excel file
          <input
            accept=".xlsx,.xls"
            className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3"
            type="file"
            onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
          />
        </label>

        <button
          className="mt-auto rounded-xl bg-brand-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-brand-900 disabled:cursor-not-allowed disabled:bg-slate-400"
          disabled={isUploading}
          type="submit"
        >
          {isUploading ? "Uploading..." : "Upload file"}
        </button>
      </form>

      <div className="mt-6 rounded-2xl bg-slate-50 p-4 text-sm text-slate-700">
        <p>
          Current selection: <span className="font-semibold capitalize">{datasetType}</span>
        </p>
        <p className="mt-1">
          Loaded rows for this dataset: <span className="font-semibold">{activeStatus?.rows_loaded ?? 0}</span>
        </p>
      </div>

      {result ? (
        <div className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">
          <p className="font-semibold">Upload saved successfully.</p>
          <p className="mt-2">File: {result.source_file}</p>
          <p>Rows read: {result.rows_read}</p>
          <p>Rows saved: {result.rows_saved}</p>
          <p>Players created: {result.players_created}</p>
          {result.missing_columns.length > 0 ? (
            <p>Missing columns: {result.missing_columns.join(", ")}</p>
          ) : null}
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
