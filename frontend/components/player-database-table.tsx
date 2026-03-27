"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

import type { PlayerDatabaseItem } from "@/lib/api";

interface PlayerDatabaseTableProps {
  players: PlayerDatabaseItem[];
}

const roleOptions = ["all", "batter", "bowler", "all-rounder", "fielding asset", "unknown"];
const sortOptions = ["overall", "batting", "bowling", "fielding"];

export function PlayerDatabaseTable({ players }: PlayerDatabaseTableProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [roleFilter, setRoleFilter] = useState("all");
  const [sortBy, setSortBy] = useState("overall");

  const filteredPlayers = useMemo(() => {
    const filtered = players.filter((player) => {
      const matchesSearch = player.name.toLowerCase().includes(searchTerm.trim().toLowerCase());
      const matchesRole = roleFilter === "all" || player.role_hint === roleFilter;
      return matchesSearch && matchesRole;
    });

    const scoreKey =
      sortBy === "batting"
        ? "batting_score"
        : sortBy === "bowling"
          ? "bowling_score"
          : sortBy === "fielding"
            ? "fielding_score"
            : "overall_score";

    return [...filtered].sort((left, right) => {
      const scoreDifference = right[scoreKey] - left[scoreKey];
      if (scoreDifference !== 0) {
        return scoreDifference;
      }
      return left.name.localeCompare(right.name);
    });
  }, [players, roleFilter, searchTerm, sortBy]);

  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">Player Database</h2>
          <p className="mt-2 text-sm leading-6 text-slate-600">
            Search by player name or filter by role hint. Scores are shown out of 10.
          </p>
        </div>
        <div className="text-sm font-medium text-slate-600">
          Players shown: <span className="text-slate-900">{filteredPlayers.length}</span>
        </div>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-[1fr_220px_220px]">
        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Search player
          <input
            className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3"
            placeholder="Type a player name"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />
        </label>

        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Filter by role
          <select
            className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3"
            value={roleFilter}
            onChange={(event) => setRoleFilter(event.target.value)}
          >
            {roleOptions.map((option) => (
              <option key={option} value={option}>
                {option === "all" ? "All roles" : option}
              </option>
            ))}
          </select>
        </label>

        <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
          Arrange by score
          <select
            className="rounded-xl border border-slate-300 bg-slate-50 px-3 py-3"
            value={sortBy}
            onChange={(event) => setSortBy(event.target.value)}
          >
            {sortOptions.map((option) => (
              <option key={option} value={option}>
                {option === "overall" ? "Original overall score" : `${option} score`}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="mt-6 overflow-x-auto rounded-2xl border border-slate-200">
        <table className="min-w-full border-collapse text-left text-sm">
          <thead className="bg-slate-100 text-slate-700">
            <tr>
              <th className="px-4 py-3 font-semibold">#</th>
              <th className="px-4 py-3 font-semibold">Player</th>
              <th className="px-4 py-3 font-semibold">Team</th>
              <th className="px-4 py-3 font-semibold">Role Hint</th>
              <th className="px-4 py-3 font-semibold">Batting</th>
              <th className="px-4 py-3 font-semibold">Bowling</th>
              <th className="px-4 py-3 font-semibold">Fielding</th>
              <th className="px-4 py-3 font-semibold">Overall</th>
            </tr>
          </thead>
          <tbody>
            {filteredPlayers.map((player, index) => (
              <tr key={player.id} className="border-t border-slate-200 text-slate-700">
                <td className="px-4 py-3 font-medium text-slate-500">{index + 1}</td>
                <td className="px-4 py-3 font-medium text-slate-900">
                  <Link className="transition hover:text-brand-700 hover:underline" href={`/players/${player.id}`}>
                    {player.name}
                  </Link>
                </td>
                <td className="px-4 py-3">{player.team_name ?? "-"}</td>
                <td className="px-4 py-3 capitalize">{player.role_hint}</td>
                <td className="px-4 py-3">{player.batting_score.toFixed(2)}</td>
                <td className="px-4 py-3">{player.bowling_score.toFixed(2)}</td>
                <td className="px-4 py-3">{player.fielding_score.toFixed(2)}</td>
                <td className="px-4 py-3 font-semibold text-slate-900">{player.overall_score.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
