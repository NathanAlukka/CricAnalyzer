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

interface PlayerMetricComparisonChartProps {
  label: string;
  playerValue: number;
  averageValue: number;
}

export function PlayerMetricComparisonChart({
  label,
  playerValue,
  averageValue,
}: PlayerMetricComparisonChartProps) {
  const data = {
    labels: [label],
    datasets: [
      {
        label: "Player",
        data: [playerValue],
        backgroundColor: "#250babff",
        borderRadius: 8,
      },
      {
        label: "Average",
        data: [averageValue],
        backgroundColor: "#a69b92ff",
        borderRadius: 8,
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
