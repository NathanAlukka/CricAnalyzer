import type { LiveAuctionEventItem } from "@/lib/api";

interface AuctionEventLogProps {
  events: LiveAuctionEventItem[];
}

export function AuctionEventLog({ events }: AuctionEventLogProps) {
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <h2 className="text-2xl font-semibold text-slate-900">Auction Event Log</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">
        The most recent auction events are listed here.
      </p>

      <div className="mt-6 overflow-x-auto rounded-2xl border border-slate-200">
        <table className="min-w-full border-collapse text-left text-sm">
          <thead className="bg-slate-100 text-slate-700">
            <tr>
              <th className="px-4 py-3 font-semibold">#</th>
              <th className="px-4 py-3 font-semibold">Player</th>
              <th className="px-4 py-3 font-semibold">Result</th>
              <th className="px-4 py-3 font-semibold">Team</th>
              <th className="px-4 py-3 font-semibold">Price</th>
            </tr>
          </thead>
          <tbody>
            {events.length === 0 ? (
              <tr>
                <td className="px-4 py-4 text-slate-500" colSpan={5}>No auction events yet.</td>
              </tr>
            ) : (
              events.map((event) => (
                <tr key={event.event_id} className="border-t border-slate-200 text-slate-700">
                  <td className="px-4 py-3">{event.nomination_order ?? "-"}</td>
                  <td className="px-4 py-3 font-medium text-slate-900">{event.player_name}</td>
                  <td className="px-4 py-3 capitalize">{event.event_type.replaceAll("_", " ")}</td>
                  <td className="px-4 py-3">{event.team_name ?? "-"}</td>
                  <td className="px-4 py-3">{event.final_price ?? "-"}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
