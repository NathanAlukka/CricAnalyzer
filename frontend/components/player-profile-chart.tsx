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

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

interface PlayerProfileChartProps {
  battingScore: number;
  bowlingScore: number;
  fieldingScore: number;
  overallScore: number;
}

export function PlayerProfileChart({
  battingScore,
  bowlingScore,
  fieldingScore,
  overallScore,
}: PlayerProfileChartProps) {
  const data = {
    labels: ["Batting", "Bowling", "Fielding", "Overall"],
    datasets: [
      {
        label: "Player Score",
        data: [battingScore, bowlingScore, fieldingScore, overallScore],
        backgroundColor: ["#0ea5e9", "#16a34a", "#d97706", "#0f172a"],
        borderRadius: 8,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        min: 0,
        max: 10,
      },
    },
    plugins: {
      legend: {
        display: false,
      },
    },
  };

  return <Bar data={data} options={options} />;
}
