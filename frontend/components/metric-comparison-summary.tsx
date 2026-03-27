interface MetricComparisonSummaryProps {
  items: {
    label: string;
    playerValue: number | null | undefined;
    averageValue: number | null | undefined;
  }[];
}

function formatValue(value: number | null | undefined) {
  if (value === null || value === undefined) {
    return "-";
  }

  return Number.isInteger(value) ? value.toString() : value.toFixed(2);
}

export function MetricComparisonSummary({ items }: MetricComparisonSummaryProps) {
  return (
    <div className="mt-5 space-y-3">
      {items.map((item) => (
        <div
          key={item.label}
          className="flex items-center justify-between rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700"
        >
          <span className="font-medium text-slate-900">{item.label}</span>
          <div className="flex gap-6 text-right">
            <span>
              Player: <span className="font-semibold text-slate-900">{formatValue(item.playerValue)}</span>
            </span>
            <span>
              Average: <span className="font-semibold text-slate-900">{formatValue(item.averageValue)}</span>
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
