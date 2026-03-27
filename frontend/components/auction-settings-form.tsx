"use client";

import { useMemo, useState } from "react";

import type { AuctionSettingsResponse, PlayerOptionItem } from "@/lib/api";
import { saveAuctionSetup } from "@/lib/api";

interface AuctionSettingsFormProps {
  initialSettings: AuctionSettingsResponse;
  playerOptions: PlayerOptionItem[];
}

interface TeamFormState {
  row_id: string;
  team_name: string;
  owner_name: string;
  captain_name: string;
  captain_player_id: string;
  is_my_team: boolean;
}

function createRowId(index: number) {
  return `team-row-${index}-${Math.random().toString(36).slice(2, 8)}`;
}

function buildDefaultTeams(count: number): TeamFormState[] {
  return Array.from({ length: count }, (_, index) => ({
    row_id: createRowId(index),
    team_name: `Team ${index + 1}`,
    owner_name: "",
    captain_name: "",
    captain_player_id: "",
    is_my_team: index === 0,
  }));
}

export function AuctionSettingsForm({ initialSettings, playerOptions }: AuctionSettingsFormProps) {
  const [tournamentName, setTournamentName] = useState(initialSettings.tournament_name);
  const [numberOfTeams, setNumberOfTeams] = useState(initialSettings.number_of_teams);
  const [squadSize, setSquadSize] = useState(initialSettings.squad_size);
  const [totalPointsPerCaptain, setTotalPointsPerCaptain] = useState(initialSettings.total_points_per_captain);
  const [captainSelfValueDeduction, setCaptainSelfValueDeduction] = useState(initialSettings.captain_self_value_deduction);
  const [maxBid, setMaxBid] = useState(initialSettings.max_bid);
  const [teams, setTeams] = useState<TeamFormState[]>(
    initialSettings.teams.length > 0
      ? initialSettings.teams.map((team) => ({
          row_id: createRowId(team.captain_player_id ?? Math.random()),
          team_name: team.team_name,
          owner_name: team.owner_name ?? "",
          captain_name: team.captain_name,
          captain_player_id: team.captain_player_id ? String(team.captain_player_id) : "",
          is_my_team: team.is_my_team,
        }))
      : buildDefaultTeams(initialSettings.number_of_teams),
  );
  const [isSaving, setIsSaving] = useState(false);
  const [resultMessage, setResultMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const playerSelectOptions = useMemo(() => [{ id: 0, name: "Select scored player" }, ...playerOptions], [playerOptions]);

  function syncTeamCount(nextCount: number) {
    setNumberOfTeams(nextCount);
    setTeams((current) => {
      if (current.length === nextCount) {
        return current;
      }
      if (current.length > nextCount) {
        return current.slice(0, nextCount);
      }
      return [...current, ...buildDefaultTeams(nextCount - current.length).map((team, index) => ({
        ...team,
        team_name: `Team ${current.length + index + 1}`,
        is_my_team: false,
      }))];
    });
  }

  function updateTeam(index: number, field: keyof TeamFormState, value: string | boolean) {
    setTeams((current) =>
      current.map((team, teamIndex) =>
        teamIndex === index
          ? { ...team, [field]: value }
          : field === "is_my_team" && value === true
            ? { ...team, is_my_team: false }
            : team,
      ),
    );
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setIsSaving(true);
    setResultMessage(null);
    setErrorMessage(null);

    try {
      const payload = {
        tournament_name: tournamentName,
        number_of_teams: numberOfTeams,
        squad_size: squadSize,
        total_points_per_captain: totalPointsPerCaptain,
        captain_self_value_deduction: captainSelfValueDeduction,
        max_bid: maxBid,
        teams: teams.map((team) => ({
          team_name: team.team_name,
          owner_name: team.owner_name || null,
          captain_name: team.captain_name,
          captain_player_id: team.captain_player_id ? Number(team.captain_player_id) : null,
          is_my_team: team.is_my_team,
        })),
      };

      const result = await saveAuctionSetup(payload);
      setResultMessage(`Saved auction setup for ${result.number_of_teams} teams.`);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Failed to save auction setup.");
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <h2 className="text-2xl font-semibold text-slate-900">Auction Rules And Teams</h2>
      <p className="mt-2 text-sm leading-6 text-slate-600">
        Set the basic auction rules, then define the teams and captains.
      </p>

      <form className="mt-6 space-y-8" onSubmit={handleSubmit}>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            Tournament name
            <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" value={tournamentName} onChange={(event) => setTournamentName(event.target.value)} />
          </label>
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            Number of teams
            <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" min={2} max={20} type="number" value={numberOfTeams} onChange={(event) => syncTeamCount(Number(event.target.value))} />
          </label>
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            Squad size
            <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" min={1} max={30} type="number" value={squadSize} onChange={(event) => setSquadSize(Number(event.target.value))} />
          </label>
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            Total points per captain
            <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" min={0} step="0.01" type="number" value={totalPointsPerCaptain} onChange={(event) => setTotalPointsPerCaptain(Number(event.target.value))} />
          </label>
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            Captain self-value deduction
            <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" min={0} step="0.01" type="number" value={captainSelfValueDeduction} onChange={(event) => setCaptainSelfValueDeduction(Number(event.target.value))} />
          </label>
          <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
            Max bid
            <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" min={0} step="0.01" type="number" value={maxBid} onChange={(event) => setMaxBid(Number(event.target.value))} />
          </label>
        </div>

        <div>
          <h3 className="text-lg font-semibold text-slate-900">Teams And Captains</h3>
          <div className="mt-4 space-y-4">
            {teams.map((team, index) => (
              <div key={team.row_id} className="rounded-2xl border border-slate-200 p-5">
                <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    Team name
                    <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" value={team.team_name} onChange={(event) => updateTeam(index, "team_name", event.target.value)} />
                  </label>
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    Owner name
                    <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" value={team.owner_name} onChange={(event) => updateTeam(index, "owner_name", event.target.value)} />
                  </label>
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    Captain name
                    <input className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" value={team.captain_name} onChange={(event) => updateTeam(index, "captain_name", event.target.value)} />
                  </label>
                  <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
                    Link captain to scored player
                    <select className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3" value={team.captain_player_id} onChange={(event) => updateTeam(index, "captain_player_id", event.target.value)}>
                      {playerSelectOptions.map((option) => (
                        <option key={option.id} value={option.id === 0 ? "" : option.id}>
                          {option.name}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className="flex items-center gap-3 rounded-xl bg-slate-50 px-4 py-3 text-sm font-medium text-slate-700">
                    <input checked={team.is_my_team} name="my-team" type="checkbox" onChange={(event) => updateTeam(index, "is_my_team", event.target.checked)} />
                    Mark as my team
                  </label>
                </div>
              </div>
            ))}
          </div>
        </div>

        <button className="rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400" disabled={isSaving} type="submit">
          {isSaving ? "Saving..." : "Save auction setup"}
        </button>
      </form>

      {resultMessage ? <div className="mt-6 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">{resultMessage}</div> : null}
      {errorMessage ? <div className="mt-6 rounded-2xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-900">{errorMessage}</div> : null}
    </section>
  );
}
