# HeatGuard — Extreme Heatwave Early Warning & Human Thermal Stress Monitoring System

---

## 1. Executive Summary & Purpose

### 1.1 Why This Project Was Created (Problem Statement)
Climate change, rapid urbanization, and deforestation have driven an alarming rise in the frequency, duration, and intensity of extreme heat events worldwide. In subtropical and tropical regions such as India, heatwaves pose a severe, life-threatening danger to public health, municipal infrastructure, and labor productivity.

Conventional weather applications typically display only the **dry-bulb ambient temperature**. However, this metric alone is dangerously misleading. In high-humidity environments (such as coastal areas, river basins, or monsoon transition periods), the human body's primary cooling mechanism—**evaporative perspiration (sweating)**—is severely hindered. When sweat cannot evaporate effectively, core body temperature climbs rapidly, leading to acute heat exhaustion, organ stress, and potentially fatal heatstroke.

### 1.2 The Purpose of HeatGuard
**HeatGuard** was designed and engineered as an **Environmental Intelligence and Public Safety Early Warning Platform**. Its core missions are:
- **Scientific Thermal Stress Estimation**: Moving beyond simple temperature by computing the true **Apparent Temperature (Heat Index)** using calibrated meteorological algorithms (the NOAA Rothfusz multivariate regression model and the Steadman physiological baseline).
- **Proactive Early Action**: Providing multi-day predictive horizons and 24-hour peak-hour warnings so communities, outdoor laborers, elderly care providers, and civic administrators can prepare *before* dangerous exposure occurs.
- **Centralized Statutory Communications**: Enabling meteorological and public health authorities to draft, manage, and disseminate verified heat advisories, warnings, and alerts with statutory accountability.
- **Accessible Public Health Guidance**: Offering targeted, actionable, tier-specific physiological precautions (hydration quotas, rest-to-work ratios, vulnerable demographic protection).

---

## 2. Comprehensive Feature Breakdown

HeatGuard delivers a cohesive suite of monitoring, forecasting, visualization, and safety tools:

```
+--------------------------------------------------------------------------------------------------+
|                                        HEATGUARD PLATFORM                                       |
+------------------------------------+-----------------------------------+-------------------------+
|        REAL-TIME INTELLIGENCE      |       FORECAST & COMPARISON       |     AUTHORITY & ACTION  |
+------------------------------------+-----------------------------------+-------------------------+
| * NOAA Rothfusz Heat Index         | * 7-Day Risk Horizon              | * Statutory Notices     |
| * Real-time Steadman Baseline      | * 24-Hour Peak Hour Detection     | * Staff Oversight Hub   |
| * Dynamic C / F Conversion         | * Multi-City Stress Comparison    | * Station Bookmarks     |
| * India Geospatial Heatmap         | * Global Geocoding Station Search | * Telemetry Logging     |
| * Scientific Category Transparency | * Historical Records Provenance   | * Safety Guides (OSHA)  |
+------------------------------------+-----------------------------------+-------------------------+
```

### 2.1 Real-Time Heat Index & Thermal Stress Calculation Engine
- **Algorithmic Rigor**: Implements the official **NOAA National Weather Service (NWS) Rothfusz formulation** (a 16-parameter multivariate polynomial regression) with low-temperature Steadman fallback and extreme-humidity adjustments.
- **5 Thermal Danger Tiers**:
  1. **Normal (`< 80°F / 26.7°C`)**: Minimal thermal stress; sweat evaporates normally.
  2. **Caution (`80°F – 90°F / 26.7°C – 32.2°C`)**: Fatigue possible with prolonged exposure and physical activity.
  3. **Extreme Caution (`90°F – 103°F / 32.2°C – 39.4°C`)**: Sunstroke, heat cramps, and heat exhaustion possible with prolonged exposure.
  4. **Danger (`103°F – 124°F / 39.4°C – 51.1°C`)**: Sunstroke, heat cramps, or heat exhaustion likely; heatstroke possible with continued exertion.
  5. **Extreme Danger (`≥ 125°F / ≥ 51.7°C`)**: Heatstroke or sunstroke highly imminent; life-threatening conditions.
- **Scientific Transparency**: Every station dashboard includes an explanatory scientific breakdown stating which mathematical equation (Steadman baseline vs. Rothfusz polynomial) was triggered and why.
- **Universal Unit Toggle**: Instantaneous, state-persistent toggle between Celsius (°C) and Fahrenheit (°F) with automatic localized mathematical rounding.

### 2.2 Interactive Geospatial India Thermal Heatmap
- **High-Reliability Cartography**: Integrated with Leaflet.js and backed by CARTO Voyager vector-styled tiles, preventing tile-quota bans and maintaining 100% uptime.
- **Boundary & Heat Gradient Overlays**: High-resolution GeoJSON boundaries for India combined with dynamic, color-coded thermal stress markers across major urban and rural observation hubs.
- **Interactive Inspection**: Clickable station nodes that display live ambient temperature, relative humidity, wind velocity, and calculated heat index with one-click navigation to full station telemetry.

### 2.3 Multi-Day Predictive Heatwave Forecast (7-Day Horizon)
- **7-Day Outlook**: Aggregates numerical weather predictions (NWP) via high-resolution gridded atmospheric models (Open-Meteo API).
- **Peak Hottest Hour Identification**: Analyzes 168 hourly time steps to isolate the single highest risk hour in the upcoming 24-hour window, providing exact target times (e.g., `14:00 IST`) and maximum projected heat index.
- **Peak Day Projection**: Highlights the most dangerous day in the 7-day forecast cycle so preventive municipal action can be planned days in advance.

### 2.4 Multi-City Thermal Comparison Tool
- **Side-by-Side Analysis**: Simultaneously compares two or more monitoring stations or arbitrary global cities.
- **Thermal Stress Delta**: Computes the exact variance in ambient temperature, relative humidity, and heat index between regions, highlighting which location presents greater physiological strain.

### 2.5 Dynamic Global Geocoding & Station Directory
- **Pre-Seeded Key Stations**: Pre-configured with major Indian metropolitan and regional hubs (Delhi, Ahmedabad, Mumbai, Bengaluru, Chennai, Guwahati, Prayagraj, etc.).
- **Global Search & Geocoding**: Users can search any city, town, or district worldwide using live Open-Meteo Geocoding. The system automatically extracts coordinates, altitude, country, and administrative region.

### 2.6 Historical Telemetry Records & Provenance Auditing
- **Strict Provenance Tagging**: Telemetry data clearly distinguishes between:
  - `provider-supplied`: Ingested directly from official gridded weather APIs.
  - `user-entered`: Manually observed and submitted readings.
- **Data Persistence**: Records track timestamp, ambient temperature, relative humidity, computed heat index, and assigned risk level.
- **Audit Table**: Searchable, paginated, and filterable telemetry logs for environmental audits and local safety reviews.

### 2.7 Official Statutory Heat Advisories & Emergency Bulletins
- **Broadcast Board**: Centralized public repository of official statutory weather notices issued by municipal or meteorological authorities.
- **Severity Levels**: Color-coded badges for **Advisory**, **Watch**, and **Warning**.
- **Statutory Traceability**: Each bulletin records the issuing organization, public verification URL, and explicit validity timeframes (`valid_from` and `valid_until`).

### 2.8 Physiological Safety Guidance & Symptom Checker
- **Evidence-Based Guidance**: Built on public health directives (aligned with NDMA and OSHA occupational safety guidelines).
- **Hydration Protocols & Work-Rest Ratios**: Concrete hourly fluid intake recommendations based on current heat index.
- **Vulnerable Group Directives**: Targeted advice for infants, older adults, outdoor manual laborers, and domestic animals.
- **Critical Symptom Differentiation**: Clear comparative diagnostic matrix contrasting **Heat Exhaustion** (cool/pale skin, heavy sweating, nausea) with life-threatening **Heatstroke** (high body temperature >103°F, red/hot dry or damp skin, confusion, loss of consciousness) with immediate emergency protocols (Call 108/112/911).

---

## 3. User Roles, Personas & Permission Matrix

HeatGuard implements a Role-Based Access Control (RBAC) model using standard Django authentication and group permission systems:

| Capability / Feature | Anonymous Public Visitor | Registered Telemetry User | Weather Authority Staff | Superuser / Administrator |
| :--- | :---: | :---: | :---: | :---: |
| **Browse Home & Public Dashboards** | Yes | Yes | Yes | Yes |
| **Search & Geocode Global Cities** | Yes | Yes | Yes | Yes |
| **View India Thermal Heatmap** | Yes | Yes | Yes | Yes |
| **View 7-Day & 24h Peak Forecasts** | Yes | Yes | Yes | Yes |
| **Multi-City Comparison Tool** | Yes | Yes | Yes | Yes |
| **Read Safety & Health Guidelines** | Yes | Yes | Yes | Yes |
| **Read Published Official Notices** | Yes | Yes | Yes | Yes |
| **Switch Units (°C / °F)** | Yes | Yes | Yes | Yes |
| **Bookmark Favorite Stations** | No | Yes | Yes | Yes |
| **Save Provider Telemetry to DB** | No | Yes | Yes | Yes |
| **Log Manual Station Observations** | No | Yes | Yes | Yes |
| **View Personal Saved Stations Hub**| No | Yes | Yes | Yes |
| **Access Authority Staff Dashboard** | No | No | Yes | Yes |
| **Draft & Publish Official Notices** | No | No | Yes | Yes |
| **Edit / Withdraw Existing Notices** | No | No | Yes | Yes |
| **Access Django Admin Site** | No | No | Limited (Staff) | Full Superuser |
| **User & Group Permission Mgmt** | No | No | No | Full Superuser |

---

### Detailed Persona Descriptions

#### 1. Anonymous Public Visitor (General Public)
- **Who they are**: Daily commuters, parents, students, athletes, and local residents seeking quick, accurate heatwave information.
- **What they can do**:
  - Access all real-time city dashboards and heat index calculations.
  - Explore the geospatial thermal heatmap of India.
  - Look up any city worldwide via geocoding.
  - Review 7-day predictive forecasts and 24-hour peak danger windows.
  - Access public safety guidelines, hydration recommendations, and emergency heatstroke protocols.
  - View published official notices and government warnings.
- **Limitations**: Cannot bookmark stations or persist data into the database.

#### 2. Registered Telemetry User (`demouser` / Community Observer)
- **Who they are**: Environmental enthusiasts, high-risk individuals needing regular monitoring, neighborhood monitors, or local facility managers.
- **What they can do**:
  - All public visitor privileges.
  - **Station Bookmarking**: Save frequently checked monitoring stations to their personal profile for instant access.
  - **Telemetry Persistence**: Explicitly record live API snapshots into the permanent database archive.
  - **Crowdsourced/Manual Ingestion**: Submit observed local station readings with automatic `user-entered` provenance tagging.
- **Limitations**: Cannot publish official heat advisories or modify administrative settings.

#### 3. Weather Authority Staff (`staffuser` / IMD / Municipal Health Officer)
- **Who they are**: Verified meteorologists, disaster management officers, civic safety administrators, and public health officials.
- **What they can do**:
  - All registered telemetry user privileges.
  - **Authority Staff Dashboard (`/staff/dashboard/`)**: A dedicated command center showing active stations, published bulletins, draft notices, and recent telemetry logs.
  - **Official Bulletin Management (CRUD)**:
    - Create and draft new heat advisories, warnings, and alerts.
    - Set validity periods, issuing authority names, and official citation links.
    - Publish notices to the public portal or archive expired advisories.
    - Edit existing bulletins when forecast conditions escalate or improve.
  - **Administrative Access**: Log in to Django Admin with staff-level permissions to inspect monitoring data.

#### 4. Superuser / System Administrator
- **Who they are**: Lead systems architects, DevOps engineers, and institutional system administrators.
- **What they can do**:
  - Complete control over the database, user models, and permission groups.
  - Configure automated seeding scripts, data backups, and environment variables.
  - Audit system security, session controls, and API rate limits.

---

## 4. Technical Architecture & Design Decisions

### 4.1 Strict Architectural Purity
- **Django Core**: Built strictly utilizing standard Django components (Function-Based Views, Django Templates, Forms, ORM, Auth, and Context Processors) without heavyweight single-page application (SPA) bloat.
- **Zero Third-Party Database Bloat**: Relies exclusively on standard Python libraries, official mathematical formulations, and minimal high-performance front-end libraries (Leaflet.js and FontAwesome).
- **Graceful Degradation & Resilience**: Designed to handle upstream weather API timeouts, rate limits, or network failures gracefully via local memory caching (`cached_weather_forecast`) and descriptive fallback states.

### 4.2 Security & Integrity
- **CSRF & XSS Protection**: All forms enforce Django CSRF tokens, strict input validation, and sanitized template rendering.
- **Session-Based Temperature Units**: Unit toggling (°C / °F) is preserved across requests via Django sessions.
- **Role Verification**: Views enforce role boundaries through `@login_required`, `user.is_staff`, and permission checks (`has_perm('monitoring.add_officialnotice')`), returning strict `PermissionDenied` (HTTP 403) for unauthorized access attempts.

---

## 5. Future Scope & Roadmap

While HeatGuard is currently a production-ready web platform, its architecture has been designed for scalable future expansion:

```
+-----------------------------------------------------------------------------------------------+
|                                      HEATGUARD FUTURE ROADMAP                                 |
+------------------------------+-------------------------------+--------------------------------+
|         PHASE 1: IOT         |       PHASE 2: ALERTS         |        PHASE 3: AI & SCALE     |
+------------------------------+-------------------------------+--------------------------------+
| * LoRaWAN / AWS Sensor Feeds | * Twilio SMS Emergency Alerts | * Microclimate AI Models       |
| * Hyperlocal Microclimates   | * WhatsApp Warning Broadcasts | * Hospital Admission Correlator|
| * MQTT Telemetry Ingestion   | * CAP Government Integration  | * Multilingual Indic Support   |
| * Solar Radiation Sensors    | * PWA Offline Push Alerts     | * Smart Urban Cooling Routing  |
+------------------------------+-------------------------------+--------------------------------+
```

### 5.1 Physical IoT Sensor & Automated Weather Station (AWS) Integration
- Direct telemetry ingestion from on-ground hardware sensors (LoRaWAN, ESP32, Raspberry Pi weather stations) via secure REST/MQTT webhooks.
- Monitoring hyperlocal urban heat island (UHI) factors such as asphalt surface radiation, tree-canopy density, and wet-bulb globe temperature (WBGT) sensors.

### 5.2 Automated Emergency Broadcast Alerts (SMS & WhatsApp)
- Integration with telecom gateways (e.g., Twilio, CDAC, Government Common Alerting Protocol - CAP).
- Automated dispatch of urgent SMS and WhatsApp warnings to registered residents and construction supervisors when heat indices breach "Danger" (>103°F) thresholds.

### 5.3 AI-Powered Microclimate & Urban Heat Island (UHI) Prediction
- Machine learning models trained on historical satellite thermal imagery (Landsat/Sentinel) and ground observations.
- Neighborhood-level thermal predictions accounting for concrete density, building elevation, and local wind corridors.

### 5.4 Progressive Web App (PWA) with GPS Safe-Exposure Timers
- Offline-first mobile app capability.
- Real-time GPS-based worker safety timer calculating maximum recommended continuous outdoor exertion time before mandatory rest and hydration.

### 5.5 Multilingual & Vernacular Accessibility
- Full localization into regional Indian languages (Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, etc.) ensuring life-saving advisories reach rural and marginalized outdoor workers.

### 5.6 Municipal Hospital & Public Health Correlation
- Integration with local municipal healthcare systems to cross-reference heat index spikes with emergency room admissions for dehydration and heat exhaustion, enabling automated emergency response resource allocation.

---

## 6. Conclusion
HeatGuard transforms raw meteorological data into actionable, life-saving intelligence. By unifying scientific apparent temperature calculations, multi-day predictive modeling, statutory public warning channels, and clear role-based accountability, HeatGuard provides communities with the foresight needed to withstand extreme climate realities.
