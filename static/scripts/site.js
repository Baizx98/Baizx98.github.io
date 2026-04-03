(function () {
  const payloadNode = document.getElementById("orcid-data");
  const yearChartNode = document.getElementById("year-chart");
  const typeChartNode = document.getElementById("type-chart");

  if (!payloadNode || !window.echarts || !yearChartNode || !typeChartNode) {
    return;
  }

  let payload = JSON.parse(payloadNode.textContent);
  if (typeof payload === "string") {
    payload = JSON.parse(payload);
  }
  const media = window.matchMedia("(prefers-color-scheme: dark)");

  const yearChart = window.echarts.init(yearChartNode);
  const typeChart = window.echarts.init(typeChartNode);

  function palette() {
    const dark = media.matches;
    return {
      text: dark ? "#edf3fb" : "#2a2119",
      muted: dark ? "#a4b3c4" : "#6a5d50",
      line: dark ? "#ff9f5a" : "#d96c2f",
      bar: dark ? "#47c1ff" : "#1e93e6",
      border: dark ? "rgba(212,225,239,0.12)" : "rgba(66,54,42,0.1)",
      panel: dark ? "rgba(18,25,35,0.75)" : "rgba(255,255,255,0.82)",
    };
  }

  function buildCharts() {
    const colors = palette();
    const yearly = payload.stats.yearly_counts || [];
    const types = payload.stats.type_counts || [];

    yearChart.setOption({
      animationDuration: 800,
      backgroundColor: "transparent",
      tooltip: {
        trigger: "axis",
        backgroundColor: colors.panel,
        borderColor: colors.border,
        textStyle: { color: colors.text },
      },
      grid: { left: 36, right: 18, top: 24, bottom: 30 },
      xAxis: {
        type: "category",
        data: yearly.map((entry) => entry.year),
        axisLabel: { color: colors.muted },
        axisLine: { lineStyle: { color: colors.border } },
      },
      yAxis: {
        type: "value",
        minInterval: 1,
        axisLabel: { color: colors.muted },
        splitLine: { lineStyle: { color: colors.border } },
      },
      series: [
        {
          type: "bar",
          data: yearly.map((entry) => entry.count),
          itemStyle: {
            color: colors.bar,
            borderRadius: [10, 10, 0, 0],
          },
        },
      ],
    });

    typeChart.setOption({
      animationDuration: 900,
      backgroundColor: "transparent",
      tooltip: {
        trigger: "item",
        backgroundColor: colors.panel,
        borderColor: colors.border,
        textStyle: { color: colors.text },
      },
      series: [
        {
          type: "pie",
          radius: ["42%", "72%"],
          avoidLabelOverlap: true,
          label: {
            color: colors.text,
            formatter: "{b}\n{c}",
          },
          itemStyle: {
            borderColor: colors.panel,
            borderWidth: 4,
          },
          data: types.map((entry, index) => ({
            name: entry.label,
            value: entry.count,
            itemStyle: {
              color: index % 2 === 0 ? colors.line : colors.bar,
            },
          })),
        },
      ],
    });
  }

  buildCharts();
  window.addEventListener("resize", function () {
    yearChart.resize();
    typeChart.resize();
  });
  media.addEventListener("change", buildCharts);
})();
