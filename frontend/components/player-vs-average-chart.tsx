"use client";

import {
  Chart as ChartJS,
  Filler,
  Legend,
  LineElement,
  PointElement,
  RadialLinearScale,
  Tooltip,
} from "chart.js";
import { Radar } from "react-chartjs-2";

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

interface PlayerVsAverageChartProps {
  playerScores: {
    batting_score: number;
    bowling_score: number;
    fielding_score: number;
    overall_score: number;
  };
  averageScores: {
    batting_score: number;
    bowling_score: number;
    fielding_score: number;
    overall_score: number;
  };
}

export function PlayerVsAverageChart({ playerScores, averageScores }: PlayerVsAverageChartProps) {
  const data = {
    labels: ["Batting", "Bowling", "Fielding", "Overall"],
    datasets: [
      {
        label: "Player",
        data: [
          playerScores.batting_score,
          playerScores.bowling_score,
          playerScores.fielding_score,
          playerScores.overall_score,
        ],
        backgroundColor: "rgba(14, 165, 233, 0.18)",
        borderColor: "#0284c7",
      },
      {
        label: "Average Player",
        data: [
          averageScores.batting_score,
          averageScores.bowling_score,
          averageScores.fielding_score,
          averageScores.overall_score,
        ],
        backgroundColor: "rgba(100, 116, 139, 0.12)",
        borderColor: "#475569",
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        min: 0,
        max: 10,
      },
    },
  };

  return <Radar data={data} options={options} />;
}
