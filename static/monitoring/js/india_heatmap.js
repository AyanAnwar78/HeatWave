(() => {
  const config = window.HEATGUARD_MAP_CONFIG;
  const map = L.map('india-heatmap', {
    center: [22.8, 80.5],
    zoom: 5,
    minZoom: 4,
    maxZoom: 12
  });

  // High-availability Esri World Topographic raster tile layer (public, free, zero API key required, no 403 blocks)
  const basemap = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
    maxZoom: 18,
    attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, USGS, METI'
  }).addTo(map);

  let tileErrorCount = 0;
  let tileErrorShown = false;
  basemap.on('tileerror', () => {
    tileErrorCount++;
    if (tileErrorCount > 4 && !tileErrorShown) {
      tileErrorShown = true;
      const note = document.createElement('div');
      note.className = 'alert alert-warning';
      note.setAttribute('role', 'status');
      note.textContent = 'Map background tiles are temporarily unavailable. The India outline and thermal overlay remain visible.';
      const shell = document.querySelector('.map-shell');
      if (shell) shell.appendChild(note);
    }
  });
  basemap.on('tileload', () => {
    tileErrorCount = Math.max(0, tileErrorCount - 1);
  });

  // Color gradient for temperature: cool blue through warm orange and red.
  const tempGradient = {
    0.0: '#38bdf8',  // Cool cyan/blue (<= 5°C)
    0.25: '#22c55e', // Fresh green (~15°C)
    0.45: '#eab308', // Warm yellow (~23°C)
    0.65: '#f97316', // Orange (~30°C)
    0.82: '#ef4444', // Red-orange (~37°C)
    1.0: '#7f1d1d'   // Deep maroon/extreme (>= 44°C)
  };

  // Color gradient for Heat Index
  const hiGradient = {
    0.0: '#38bdf8',  // Cool cyan/blue (< 65°F)
    0.25: '#22c55e', // Normal green (65 - 80°F)
    0.45: '#eab308', // Caution yellow (80 - 90°F)
    0.65: '#f97316', // Extreme caution orange (90 - 103°F)
    0.82: '#ef4444', // Danger red (103 - 124°F)
    1.0: '#7f1d1d'   // Extreme danger maroon (>= 125°F)
  };

  // Heat layer with strong opacity and radius to ensure continuous color coverage across India
  const heat = L.heatLayer([], {
    radius: 56,
    blur: 34,
    maxZoom: 8,
    max: 1.0,
    minOpacity: 0.42,
    gradient: tempGradient
  }).addTo(map);

  // Dedicated interactive station markers layer
  const stationsLayer = L.layerGroup().addTo(map);

  let indiaBoundaryLayer = null;
  let currentMode = 'temp'; // 'temp' or 'hi'
  let cachedPayload = null;
  let busy = false;
  let loaded = false;

  const statusEl = document.getElementById('heatmap-status');
  const timestampEl = document.getElementById('heatmap-timestamp');
  const errorEl = document.getElementById('heatmap-error');
  const toggleTempBtn = document.getElementById('toggle-temp');
  const toggleHiBtn = document.getElementById('toggle-hi');
  const legendTitle = document.getElementById('legend-title');
  const legendLabels = document.getElementById('legend-labels');
  const legendDesc = document.getElementById('legend-description');

  // Load India Boundary
  const boundaryPromise = fetch(config.boundaryUrl)
    .then(r => {
      if (!r.ok) throw new Error('Boundary asset response not OK');
      return r.json();
    })
    .then(geo => {
      indiaBoundaryLayer = L.geoJSON(geo, {
        style: {
          color: '#0f172a',
          weight: 2,
          fill: false,
          opacity: 0.9
        }
      }).addTo(map);
      map.fitBounds(indiaBoundaryLayer.getBounds(), { padding: [15, 15] });
    })
    .catch(() => {
      if (errorEl) {
        errorEl.hidden = false;
        errorEl.textContent = 'India boundary overlay could not be loaded.';
      }
    });

  // Default major monitoring hubs across India (used if not passed via config)
  const defaultStationHubs = [
    { id: 2, name: 'Delhi', latitude: 28.6139, longitude: 77.2090, state_or_region: 'Delhi' },
    { id: 3, name: 'Mumbai', latitude: 19.0760, longitude: 72.8777, state_or_region: 'Maharashtra' },
    { id: 4, name: 'Kolkata', latitude: 22.5726, longitude: 88.3639, state_or_region: 'West Bengal' },
    { id: 5, name: 'Chennai', latitude: 13.0827, longitude: 80.2707, state_or_region: 'Tamil Nadu' },
    { id: 6, name: 'Bengaluru', latitude: 12.9716, longitude: 77.5946, state_or_region: 'Karnataka' },
    { id: 7, name: 'Hyderabad', latitude: 17.3850, longitude: 78.4867, state_or_region: 'Telangana' },
    { id: 8, name: 'Ahmedabad', latitude: 23.0225, longitude: 72.5714, state_or_region: 'Gujarat' },
    { id: 9, name: 'Jaipur', latitude: 26.9124, longitude: 75.7873, state_or_region: 'Rajasthan' },
    { id: 10, name: 'Lucknow', latitude: 26.8467, longitude: 80.9462, state_or_region: 'Uttar Pradesh' },
    { id: 12, name: 'Patna', latitude: 25.5941, longitude: 85.1376, state_or_region: 'Bihar' },
    { id: 13, name: 'Guwahati', latitude: 26.1844, longitude: 91.7458, state_or_region: 'Assam' },
    { id: 1, name: 'Prayagraj', latitude: 25.4358, longitude: 81.8463, state_or_region: 'Uttar Pradesh' }
  ];

  function renderStationMarkers(points) {
    stationsLayer.clearLayers();
    const stations = (config.stations && config.stations.length > 0) ? config.stations : defaultStationHubs;

    stations.forEach(st => {
      const sLat = parseFloat(st.latitude);
      const sLon = parseFloat(st.longitude);
      if (isNaN(sLat) || isNaN(sLon)) return;

      // Find nearest grid observation point
      let nearest = null;
      let minDist = Infinity;
      for (const p of points) {
        const distSq = (p.latitude - sLat) ** 2 + (p.longitude - sLon) ** 2;
        if (distSq < minDist) {
          minDist = distSq;
          nearest = p;
        }
      }

      if (!nearest) return;

      // Color mapping according to risk / mode
      let markerColor = '#10b981'; // Green (Normal)
      const risk = (nearest.risk || 'NORMAL').toUpperCase();
      if (risk === 'CAUTION') markerColor = '#f59e0b';
      else if (risk === 'EXTREME_CAUTION') markerColor = '#f97316';
      else if (risk === 'DANGER') markerColor = '#ef4444';
      else if (risk === 'EXTREME_DANGER') markerColor = '#7f1d1d';

      const tempVal = nearest.temperature_c !== undefined ? nearest.temperature_c.toFixed(1) + '°C' : '--';
      const hiVal = nearest.heat_index_c !== undefined ? nearest.heat_index_c.toFixed(1) + '°C' : '--';
      const hiValF = nearest.heat_index_f !== undefined ? nearest.heat_index_f.toFixed(1) + '°F' : '--';

      const circle = L.circleMarker([sLat, sLon], {
        radius: 7,
        fillColor: markerColor,
        color: '#ffffff',
        weight: 2.5,
        opacity: 1,
        fillOpacity: 0.95
      });

      // Tooltip on hover
      circle.bindTooltip(`<strong>${st.name}</strong>: ${currentMode === 'temp' ? tempVal : hiVal + ' (' + risk + ')'}`, {
        permanent: false,
        direction: 'top',
        offset: [0, -6]
      });

      // Rich popup on click
      const popupHtml = `
        <div style="font-family: inherit; font-size: 0.92rem; padding: 4px; min-width: 175px;">
          <div style="font-size: 1.1rem; font-weight: 800; color: #0f172a; margin-bottom: 4px;">
            <i class="fa-solid fa-location-dot" style="color: ${markerColor};"></i> ${st.name}
          </div>
          <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 8px;">${st.state_or_region || 'India'}</div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
            <span style="color: #475569;">Air Temp:</span>
            <strong style="color: #ea580c;">${tempVal}</strong>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <span style="color: #475569;">Heat Index:</span>
            <strong style="color: #0f172a;">${hiVal} (${hiValF})</strong>
          </div>
          <div style="margin-top: 6px; padding: 4px 8px; background: #f8fafc; border-radius: 6px; border: 1px solid #e2e8f0; font-size: 0.78rem;">
            Thermal Risk: <strong style="color: ${markerColor};">${risk}</strong>
          </div>
          ${st.id ? `
            <div style="margin-top: 10px;">
              <a href="/city/${st.id}/" style="display: block; text-align: center; background: #0f172a; color: #ffffff; text-decoration: none; padding: 5px 8px; border-radius: 6px; font-weight: 700; font-size: 0.8rem;">
                View Station Telemetry &rarr;
              </a>
            </div>
          ` : ''}
        </div>
      `;
      circle.bindPopup(popupHtml);
      stationsLayer.addLayer(circle);
    });
  }

  function updateLayerData() {
    if (!cachedPayload || !cachedPayload.valid_points) return;

    const points = cachedPayload.valid_points;
    const heatData = [];

    if (currentMode === 'temp') {
      // Temperature range in °C: Scale from 0°C to 48°C
      // Ensures cooler temperatures (<18°C) still render with a visible cyan/emerald tint
      const minT = 0;
      const maxT = 48;
      points.forEach(p => {
        const val = p.temperature_c !== undefined ? p.temperature_c : 20;
        const norm = Math.max(0.18, Math.min(1.0, 0.16 + ((val - minT) / (maxT - minT)) * 0.84));
        heatData.push([p.latitude, p.longitude, norm]);
      });

      heat.setOptions({ gradient: tempGradient });
      heat.setLatLngs(heatData);

      if (legendTitle) legendTitle.textContent = 'Live Temperature Scale (°C)';
      if (legendLabels) {
        legendLabels.innerHTML = `
          <span>&le; 0°C</span>
          <span>15°C</span>
          <span>25°C</span>
          <span>32°C</span>
          <span>38°C</span>
          <span>&ge; 45°C</span>
        `;
      }
      if (legendDesc) {
        legendDesc.textContent = 'Model-based 2 m air-temperature estimates from Open-Meteo. The smooth surface is interpolated between sample locations.';
      }
    } else {
      // Heat Index mode: Scale from 50°F to 125°F
      // Normal (<80°F) conditions render as visible cool green/cyan (~0.18 - 0.45)
      // Caution (80-90°F) renders as yellow (~0.45 - 0.60)
      // Extreme Caution (90-103°F) renders as orange (~0.60 - 0.78)
      // Danger (103-124°F) renders as red (~0.78 - 0.92)
      // Extreme Danger (>=125°F) renders as deep maroon (~0.92 - 1.0)
      const minHI = 50;
      const maxHI = 125;
      points.forEach(p => {
        const hi_f = (p.heat_index_f !== undefined && p.heat_index_f !== null) ? p.heat_index_f : 70;
        const norm = Math.max(0.18, Math.min(1.0, 0.16 + ((hi_f - minHI) / (maxHI - minHI)) * 0.84));
        heatData.push([p.latitude, p.longitude, norm]);
      });

      heat.setOptions({ gradient: hiGradient });
      heat.setLatLngs(heatData);

      if (legendTitle) legendTitle.textContent = 'Heat Index (Human Thermal Stress)';
      if (legendLabels) {
        legendLabels.innerHTML = `
          <span>Normal (&lt;80°F)</span>
          <span>Caution (80–90°F)</span>
          <span>Extreme Caution</span>
          <span>Danger</span>
          <span>Extreme Danger</span>
        `;
      }
      if (legendDesc) {
        legendDesc.textContent = 'Estimated Heat Index calculated from model-based air temperature and humidity using the NOAA/NWS method.';
      }
    }

    // Update interactive station markers
    renderStationMarkers(points);
  }

  async function refresh(manual = false) {
    if (busy || (document.hidden && !manual)) return;
    busy = true;
    if (statusEl) statusEl.textContent = 'Fetching the latest model-based weather estimates across India…';
    try {
      const response = await fetch(config.dataUrl, {
        headers: { 'Accept': 'application/json' }
      });
      const data = await response.json();
      if (!response.ok || !data.success || !data.valid_points?.length) {
        throw new Error(data.error || 'Weather telemetry temporarily unavailable.');
      }
      cachedPayload = data;
      loaded = true;
      if (errorEl) errorEl.hidden = true;

      updateLayerData();

      if (statusEl) {
        statusEl.textContent = `${data.valid_point_count} model-based sample points · Source: Open-Meteo · Provider time: ${data.provider_valid_time || 'unavailable'}`;
      }
      if (timestampEl) {
        timestampEl.textContent = `Updated: ${new Date(data.retrieved_at).toLocaleTimeString()}`;
      }
    } catch (e) {
      if (errorEl) {
        errorEl.hidden = false;
        errorEl.textContent = loaded
          ? `Live update failed. Displaying cached data from ${timestampEl ? timestampEl.textContent : 'earlier'}.`
          : 'Weather estimates are temporarily unavailable. Please try again shortly.';
      }
      if (statusEl) {
        statusEl.textContent = loaded ? 'Showing cached estimates' : 'Weather estimates unavailable';
      }
    } finally {
      busy = false;
    }
  }

  if (toggleTempBtn) {
    toggleTempBtn.addEventListener('click', () => {
      if (currentMode === 'temp') return;
      currentMode = 'temp';
      toggleTempBtn.classList.add('active');
      toggleTempBtn.setAttribute('aria-pressed', 'true');
      toggleHiBtn.classList.remove('active');
      toggleHiBtn.setAttribute('aria-pressed', 'false');
      updateLayerData();
    });
  }

  if (toggleHiBtn) {
    toggleHiBtn.addEventListener('click', () => {
      if (currentMode === 'hi') return;
      currentMode = 'hi';
      toggleHiBtn.classList.add('active');
      toggleHiBtn.setAttribute('aria-pressed', 'true');
      toggleTempBtn.classList.remove('active');
      toggleTempBtn.setAttribute('aria-pressed', 'false');
      updateLayerData();
    });
  }

  document.getElementById('heatmap-refresh')?.addEventListener('click', () => refresh(true));
  document.getElementById('heatmap-reset')?.addEventListener('click', () => {
    if (indiaBoundaryLayer) {
      map.fitBounds(indiaBoundaryLayer.getBounds(), { padding: [15, 15] });
    } else {
      map.setView([22.8, 80.5], 5);
    }
  });

  document.addEventListener('visibilitychange', () => {
    if (!document.hidden && (!loaded || Date.now() - (window._lastHeatmapFetch || 0) > 300000)) {
      refresh();
    }
  });

  boundaryPromise.finally(() => refresh());
  setInterval(() => {
    if (!document.hidden) refresh();
  }, 600000); // 10 minutes
})();
