/* HeatGuard – map.js  (Leaflet 1.9) */

document.addEventListener('DOMContentLoaded', () => {
  const mapEl = document.getElementById('heatMap');
  if (!mapEl || typeof L === 'undefined') return;

  // Dark tile layer
  const map = L.map('heatMap', { zoomControl: true });

  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 19,
  }).addTo(map);

  if (!markers || markers.length === 0) {
    map.setView([20.5937, 78.9629], 5);  // India default
    return;
  }

  // ── Build markers ────────────────────────────────────────────────
  const latLngs = [];

  markers.forEach(m => {
    const ll = [m.lat, m.lon];
    latLngs.push(ll);

    const icon = L.divIcon({
      className: '',
      iconSize:  [44, 44],
      iconAnchor:[22, 22],
      html: `
        <div style="
          width: 44px; height: 44px;
          background: ${m.colour};
          border: 3px solid rgba(255,255,255,0.3);
          border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          font-size: 1.1rem;
          box-shadow: 0 0 12px ${m.colour}88;
          cursor: pointer;
        ">${m.emoji}</div>`,
    });

    const popup = L.popup({ className: 'heat-popup' }).setContent(`
      <div style="color:#fff; font-family:Inter,sans-serif; min-width:160px;">
        <div style="font-weight:700; font-size:1rem; margin-bottom:4px;">
          📍 ${m.name}, ${m.country}
        </div>
        <div style="color:${m.colour}; font-weight:600; margin-bottom:6px;">
          ${m.emoji} ${m.risk_level}
        </div>
        <div style="font-size:0.8rem; opacity:0.75; line-height:1.6;">
          🌡 Temp: ${m.temperature}°C<br>
          💧 Humidity: ${m.humidity}%<br>
          🔥 Heat Index: ${m.heat_index}°C
        </div>
      </div>
    `);

    L.marker(ll, { icon }).addTo(map).bindPopup(popup);
  });

  // Fit map to markers
  if (latLngs.length > 1) {
    map.fitBounds(L.latLngBounds(latLngs), { padding: [40, 40] });
  } else if (latLngs.length === 1) {
    map.setView(latLngs[0], 10);
  }
});

