"use client";

import { ArcElement, Chart as ChartJS, Legend, Tooltip } from "chart.js";
import { Doughnut } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

interface TeamCompositionChartProps {
  batterCount: number;
  bowlerCount: number;
  allRounderCount: number;
  fieldingAssetCount: number;
}

export function TeamCompositionChart({
  batterCount,
  bowlerCount,
  allRounderCount,
  fieldingAssetCount,
}: TeamCompositionChartProps) {
  const data = {
    labels: ["Batters", "Bowlers", "All-rounders", "Good fielders"],
    datasets: [
      {
        data: [batterCount, bowlerCount, allRounderCount, fieldingAssetCount],
        backgroundColor: ["#0ea5e9", "#16a34a", "#f59e0b", "#7c3aed"],
        borderWidth: 1,
      },
    ],
  };

  return <Doughnut data={data} />;
}
