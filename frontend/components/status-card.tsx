interface StatusCardProps {
  title: string;
  status: string;
  description: string;
}

export function StatusCard({ title, status, description }: StatusCardProps) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between gap-4">
        <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
        <span className="rounded-full bg-brand-50 px-3 py-1 text-sm font-medium text-brand-700">
          {status}
        </span>
      </div>
      <p className="mt-3 text-sm leading-6 text-slate-600">{description}</p>
    </div>
  );
}
