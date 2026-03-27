"use client";

interface PlayerScoreCardsProps {
  battingScore: number;
  bowlingScore: number;
  fieldingScore: number;
  overallScore: number;
}

const cards = [
  { key: "batting", label: "Batting", color: "bg-sky-50 text-sky-800 border-sky-200" },
  { key: "bowling", label: "Bowling", color: "bg-emerald-50 text-emerald-800 border-emerald-200" },
  { key: "fielding", label: "Fielding", color: "bg-amber-50 text-amber-800 border-amber-200" },
  { key: "overall", label: "Overall", color: "bg-slate-100 text-slate-900 border-slate-200" },
] as const;

export function PlayerScoreCards({
  battingScore,
  bowlingScore,
  fieldingScore,
  overallScore,
}: PlayerScoreCardsProps) {
  const values = {
    batting: battingScore,
    bowling: bowlingScore,
    fielding: fieldingScore,
    overall: overallScore,
  };

  return (
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {cards.map((card) => (
        <div key={card.key} className={`rounded-2xl border p-5 ${card.color}`}>
          <p className="text-sm font-semibold uppercase tracking-wide">{card.label}</p>
          <p className="mt-3 text-3xl font-bold">{values[card.key].toFixed(2)}</p>
          <p className="mt-1 text-xs">Score out of 10</p>
        </div>
      ))}
    </section>
  );
}
