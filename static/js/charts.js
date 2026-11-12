/* HeatGuard – charts.js  (Chart.js v4) */

// ── Shared defaults ──────────────────────────────────────────────────
Chart.defaults.color = 'rgba(255,255,255,0.5)';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';
Chart.defaults.font.family = 'Inter, system-ui, sans-serif';

const gridOpts = {
  color: 'rgba(255,255,255,0.06)',
};

// ── Temperature & Heat Index chart ───────────────────────────────────
(function () {
  const canvas = document.getElementById('tempChart');
  if (!canvas) return;

  new Chart(canvas, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Temperature (°C)',
          data: temps,
          borderColor: '#f97316',
          backgroundColor: 'rgba(249,115,22,0.15)',
          fill: true,
          tension: 0.4,
          pointRadius: 2,
          borderWidth: 2,
        },
        {
          label: 'Feels Like (°C)',
          data: feels,
          borderColor: '#fbbf24',
          backgroundColor: 'rgba(251,191,36,0.1)',
          fill: false,
          tension: 0.4,
          pointRadius: 2,
          borderWidth: 2,
          borderDash: [4, 3],
        },
        {
          label: 'Heat Index (°C)',
          data: heatIdx,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239,68,68,0.1)',
          fill: false,
          tension: 0.4,
          pointRadius: 2,
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { boxWidth: 12, padding: 16 } },
        tooltip: { backgroundColor: 'rgba(0,0,0,0.8)' },
      },
      scales: {
        x: { grid: gridOpts, ticks: { maxTicksLimit: 8 } },
        y: { grid: gridOpts, ticks: { callback: v => v + '°' } },
      },
    },
  });
})();

// ── Humidity chart ───────────────────────────────────────────────────
(function () {
  const canvas = document.getElementById('humidChart');
  if (!canvas) return;

  new Chart(canvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Humidity (%)',
          data: humidity,
          backgroundColor: 'rgba(59,130,246,0.5)',
          borderColor: '#3b82f6',
          borderWidth: 1,
          borderRadius: 4,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { boxWidth: 12 } },
        tooltip: { backgroundColor: 'rgba(0,0,0,0.8)' },
      },
      scales: {
        x: { grid: gridOpts, ticks: { maxTicksLimit: 8 } },
        y: { grid: gridOpts, min: 0, max: 100, ticks: { callback: v => v + '%' } },
      },
    },
  });
})();

