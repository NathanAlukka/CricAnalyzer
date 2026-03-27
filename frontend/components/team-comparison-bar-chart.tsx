"use client";

import {
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  Tooltip,
} from "chart.js";
import { Bar } from "react-chartjs-2";

import type { PostAuctionTeamItem } from "@/lib/api";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

interface TeamComparisonBarChartProps {
  teams: PostAuctionTeamItem[];
}

export function TeamComparisonBarChart({ teams }: TeamComparisonBarChartProps) {
  const data = {
    labels: teams.map((team) => team.team_name),
    datasets: [
      {
        label: "Batting",
        data: teams.map((team) => team.batting_total),
        backgroundColor: "#0ea5e9",
      },
      {
        label: "Bowling",
        data: teams.map((team) => team.bowling_total),
        backgroundColor: "#16a34a",
      },
      {
        label: "Fielding",
        data: teams.map((team) => team.fielding_total),
        backgroundColor: "#f59e0b",
      },
      {
        label: "Overall",
        data: teams.map((team) => team.overall_total),
        backgroundColor: "#0f172a",
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top" as const,
      },
    },
  };

  return <Bar data={data} options={options} />;
}
