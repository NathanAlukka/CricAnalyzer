import type { BidRecommendation } from "@/lib/api";

interface RecommendationBoxProps {
  recommendation: BidRecommendation | null;
  errorMessage: string | null;
  isLoading: boolean;
}

export function RecommendationBox({ recommendation, errorMessage, isLoading }: RecommendationBoxProps) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <h2 className="text-2xl font-semibold text-slate-900">Bid Recommendation</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">
        Transparent rule-based guidance based on score, team need, scarcity, and remaining budget.
      </p>

      {isLoading ? <p className="mt-6 text-sm text-slate-600">Loading recommendation...</p> : null}

      {errorMessage ? (
        <div className="mt-6 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-900">
          {errorMessage}
        </div>
      ) : null}

      {recommendation ? (
        <div className="mt-6 space-y-6">
          <div className="rounded-2xl bg-slate-950 p-5 text-white">
            <p className="text-sm uppercase tracking-wide text-slate-300">Recommendation</p>
            <p className="mt-2 text-3xl font-bold capitalize">{recommendation.recommendation_label}</p>
            <p className="mt-3 text-sm leading-6 text-slate-200">{recommendation.recommendation_reason}</p>
          </div>

          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            <div className="rounded-2xl bg-emerald-50 p-4">
              <p className="text-sm text-emerald-800">Fair value</p>
              <p className="mt-2 text-3xl font-bold text-emerald-950">{recommendation.fair_value.toFixed(2)}</p>
            </div>
            <div className="rounded-2xl bg-sky-50 p-4">
              <p className="text-sm text-sky-800">Good buy up to</p>
              <p className="mt-2 text-3xl font-bold text-sky-950">{recommendation.good_buy_upto.toFixed(2)}</p>
            </div>
            <div className="rounded-2xl bg-amber-50 p-4">
              <p className="text-sm text-amber-800">Overpay threshold</p>
              <p className="mt-2 text-3xl font-bold text-amber-950">{recommendation.overpay_threshold.toFixed(2)}</p>
            </div>
            <div className="rounded-2xl bg-rose-50 p-4">
              <p className="text-sm text-rose-800">Hard cap</p>
              <p className="mt-2 text-3xl font-bold text-rose-950">{recommendation.hard_cap.toFixed(2)}</p>
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 p-4">
              <p className="text-sm text-slate-600">Team need score</p>
              <p className="mt-2 text-2xl font-bold text-slate-900">{recommendation.team_need_score.toFixed(2)}</p>
            </div>
            <div className="rounded-2xl border border-slate-200 p-4">
              <p className="text-sm text-slate-600">Scarcity score</p>
              <p className="mt-2 text-2xl font-bold text-slate-900">{recommendation.scarcity_score.toFixed(2)}</p>
            </div>
          </div>
        </div>
      ) : null}

      {!isLoading && !errorMessage && !recommendation ? (
        <p className="mt-6 text-sm text-slate-600">Select a player to generate a recommendation.</p>
      ) : null}
    </section>
  );
}
