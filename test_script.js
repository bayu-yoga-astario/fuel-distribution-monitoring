
        // ============================================================
        // NAVIGATION LOGIC
        // ============================================================
        const navItems = document.querySelectorAll('.nav-item');
        const views = document.querySelectorAll('.view-section');
        const titles = {
            'dashboard': 'KPI Dashboard|Real-Time Enterprise Overview',
            'tracking':  'Live GPS Tracking|Real-Time Fleet Positioning',
            'ai':        'AI Forecasting|Predictive Demand & Stock Analysis',
            'logs':      'Full Logs|Complete Distribution History',
            'analytics': 'Supply Chain Analytics|Distribution Flow Metrics',
            'depot':     'Depot Management|Capacity & Inventory Control',
            'esg':       'ESG Report|Environmental Impact & Emissions',
            'alerts':    'Alerts & Notifications|Automated WA & Email Triggers',
            'access':    'Multi-Role Access|Security & Permissions'
        };

        let trackingMapInit = false;

        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                navItems.forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');

                const targetId = item.getAttribute('data-target');

                // Switch views
                views.forEach(v => v.classList.remove('active'));
                const targetView = document.getElementById('view-' + targetId);
                if (targetView) targetView.classList.add('active');

                // Update header
                if (titles[targetId]) {
                    const parts = titles[targetId].split('|');
                    document.getElementById('page-header-title').innerText = parts[0];
                    document.getElementById('page-header-subtitle').innerText = parts[1];
                }

                // Scroll to top on view change
                document.querySelector('.dashboard-area').scrollTop = 0;
                window.scrollTo(0, 0);

                // Map resize triggers
                if (targetId === 'tracking' && typeof trackingMap !== 'undefined') {
                    setTimeout(() => trackingMap.invalidateSize(), 200);
                }
                if (targetId === 'depot' && typeof depotMap !== 'undefined') {
                    setTimeout(() => depotMap.invalidateSize(), 200);
                }

                // Load dynamic data
                if (targetId === 'access') loadUsers();
            });
        });

        // ============================================================
        // CRUD FUNCTIONS
        // ============================================================
        function loadUsers() {
            fetch('/api/users')
                .then(res => res.json())
                .then(data => {
                    const tbody = document.getElementById('users-table-body');
                    tbody.innerHTML = '';
                    data.forEach(u => {
                        let badgeColor = 'badge-warning';
                        if(u.role === 'manager') badgeColor = 'badge-danger';
                        if(u.role === 'supervisor') badgeColor = 'badge-info';
                        
                        tbody.innerHTML += `
                            <tr>
                                <td>${u.id}</td>
                                <td>${u.name}</td>
                                <td><span class="badge-pill ${badgeColor}">${u.role}</span></td>
                                <td><span class="badge-pill badge-success">${u.status}</span></td>
                                <td><button class="panel-action" onclick="alert('Editing user ${u.name}')">Edit</button></td>
                            </tr>
                        `;
                    });
                });
        }

        function saveUser() {
            const username = document.getElementById('new-username').value;
            const password = document.getElementById('new-password').value;
            const role = document.getElementById('new-role').value;
            fetch('/api/users/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password, role })
            }).then(() => {
                document.getElementById('userModal').style.display = 'none';
                loadUsers();
            });
        }

        function saveDepot() {
            const name = document.getElementById('new-depot-name').value;
            const location = document.getElementById('new-depot-location').value;
            fetch('/api/stock/depots', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, location })
            }).then(() => {
                document.getElementById('depotModal').style.display = 'none';
                alert('Depot created successfully!');
            });
        }

        function sendTestAlert() {
            const channel = document.getElementById('alert-channel').value;
            const recipient = document.getElementById('alert-recipient').value;
            const msg = document.getElementById('alert-msg').value;
            
            fetch(`/api/notifications/trigger-alert?channel=${channel}&recipient=${recipient}&message=${msg}`, {
                method: 'POST'
            }).then(res => res.json()).then(data => {
                const tbody = document.getElementById('alerts-table-body');
                const icon = channel === 'WhatsApp' ? '<i class="fa-brands fa-whatsapp" style="color:var(--success)"></i>' : '<i class="fa-solid fa-envelope" style="color:var(--accent-blue)"></i>';
                const row = `<tr><td>${icon} ${channel}</td><td>${recipient}</td><td>${msg}</td><td><span class="badge-pill badge-success">Just Sent!</span></td></tr>`;
                tbody.insertAdjacentHTML('afterbegin', row);
                document.getElementById('alert-recipient').value = '';
                document.getElementById('alert-msg').value = '';
            });
        }

        // ============================================================
        // PLOTLY CHARTS
        // ============================================================
        const darkLayout = {
            margin: {t: 20, l: 40, r: 20, b: 40}, paper_bgcolor: 'transparent', plot_bgcolor: 'transparent',
            font: {color: '#8c93a8', family: 'Outfit'}, xaxis: {showgrid: false}, yaxis: {gridcolor: 'rgba(255,255,255,0.05)'},
            legend: {orientation: 'h', y: -0.2}
        };

        // 1. KPI Dashboard - Main Chart
        const chartData = [10, 12, 14, 16, 18, 20].map(h => ({time: `${h}:00`, valA: Math.random()*5000+10000, valB: Math.random()*5000+8000, valC: Math.random()*3000+5000}));
        Plotly.newPlot('main-chart', [
            { x: chartData.map(d=>d.time), y: chartData.map(d=>d.valA), type: 'scatter', mode: 'lines+markers', name: 'Pertamax', line: {color: '#00e5ff', width: 3, shape: 'spline'} },
            { x: chartData.map(d=>d.time), y: chartData.map(d=>d.valB), type: 'scatter', mode: 'lines+markers', name: 'Solar', line: {color: '#9d00ff', width: 3, shape: 'spline'} },
            { x: chartData.map(d=>d.time), y: chartData.map(d=>d.valC), type: 'scatter', mode: 'lines+markers', name: 'Pertalite', line: {color: '#ff3366', width: 3, shape: 'spline'} }
        ], darkLayout, {displayModeBar: false, responsive: true});

        // 2. KPI Dashboard - Pie Chart
        Plotly.newPlot('pie-chart', [{
            values: [40, 20, 10, 30], labels: ['Pertamax', 'Pertamax Turbo', 'Solar', 'Pertalite'], type: 'pie', hole: .6,
            marker: {colors: ['#00e5ff', '#ffb300', '#9d00ff', '#ff3366']}, textinfo: 'label+percent'
        }], { ...darkLayout, showlegend: false, margin: {t: 0, l: 0, r: 0, b: 0} }, {displayModeBar: false});

        // 3. Analytics - Sankey Chart
        Plotly.newPlot('sankey-chart', [{
            type: "sankey", orientation: "h",
            node: { pad: 15, thickness: 20, line: {color: "black", width: 0}, label: ["Plumpang", "T. Gerem", "Jakarta", "Bandung", "Banten"], color: ["#00e5ff", "#9d00ff", "#ff3366", "#00e676", "#ffb300"] },
            link: { source: [0,0,1,1], target: [2,3,2,4], value: [8, 4, 2, 8], color: "rgba(255,255,255,0.1)" }
        }], { ...darkLayout, font: {color: '#fff', size: 12} }, {displayModeBar: false});

        // 4. ESG - Bar Chart
        Plotly.newPlot('bar-chart', [{
            x: ['Jakarta', 'Bandung', 'Banten', 'Cirebon'], y: [420, 310, 250, 150], type: 'bar', marker: {color: ['#ff3366', '#ffb300', '#00e5ff', '#9d00ff']}
        }], darkLayout, {displayModeBar: false});

        // ============================================================
        // JWT AUTH & FETCH OVERRIDE
        // ============================================================
        let jwtToken = localStorage.getItem('fueltrack_jwt');
        if (jwtToken) {
            document.getElementById('login-overlay').style.display = 'none';
            document.getElementById('app-content').style.display = 'flex';
            loadInitialData();
        }

        const originalFetch = window.fetch;
        window.fetch = async function(url, options = {}) {
            if (jwtToken) {
                options.headers = { ...options.headers, 'Authorization': `Bearer ${jwtToken}` };
            }
            const res = await originalFetch(url, options);
            if (res.status === 401 && url !== '/api/auth/login') {
                localStorage.removeItem('fueltrack_jwt');
                window.location.reload();
            }
            return res;
        };

        function performLogin() {
            const u = document.getElementById('login-username').value;
            const p = document.getElementById('login-password').value;
            fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({username: u, password: p})
            }).then(async res => {
                if(res.ok) {
                    const data = await res.json();
                    jwtToken = data.access_token;
                    localStorage.setItem('fueltrack_jwt', jwtToken);
                    document.getElementById('login-overlay').style.display = 'none';
                    document.getElementById('app-content').style.display = 'flex';
                    loadInitialData();
                } else {
                    document.getElementById('login-error').style.display = 'block';
                }
            });
        }

        // ============================================================
        // LOAD INITIAL DATA (after login)
        // ============================================================
        function loadInitialData() {
            initDepotMap();
            loadFullLogs();
            loadForecast();
            loadTrackingMap();
            loadAnalytics();
        }

        // Depot Map
        let depotMap;
        let depotMapInitialized = false;
        function initDepotMap() {
            if(depotMapInitialized) return;
            depotMap = L.map('depot-map').setView([-6.200000, 106.816666], 9);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; <a href="https://carto.com/">CARTO</a>'
            }).addTo(depotMap);
            
            var factoryIcon = L.divIcon({
                className: 'custom-div-icon',
                html: "<div style='font-size:20px; color:#ffb300; filter: drop-shadow(0 0 10px #ffb300);'><i class='fa-solid fa-industry'></i></div>",
                iconSize: [20, 20], iconAnchor: [10, 10]
            });

            L.marker([-6.1264, 106.8993], {icon: factoryIcon}).addTo(depotMap).bindPopup("<b>Plumpang Terminal</b><br>Pertamax: 75%<br>Solar: 40%");
            L.marker([-5.9272, 105.9980], {icon: factoryIcon}).addTo(depotMap).bindPopup("<b>Tanjung Gerem</b><br>Pertalite: 90%<br>Pertamax: 20%");
            L.marker([-6.4014, 107.4526], {icon: factoryIcon}).addTo(depotMap).bindPopup("<b>Cikampek Depot</b><br>Solar: 60%<br>Turbo: 85%");
            depotMapInitialized = true;
        }

        // AI Forecast
        function loadForecast() {
            fetch('/api/forecast/predict-stockout')
                .then(response => response.json())
                .then(data => {
                    if(data.length > 0) {
                        const forecastData = [1, 2, 3, 4, 5, 6].map(h => ({time: `${h}h`, valA: data[0].current_stock - (h*1000), valB: data[0].current_stock - (h*800)}));
                        Plotly.newPlot('forecast-chart', [
                            { x: forecastData.map(d=>d.time), y: forecastData.map(d=>d.valA), type: 'scatter', mode: 'lines', name: 'Actual Demand', line: {color: '#00e5ff', width: 2} },
                            { x: forecastData.map(d=>d.time), y: forecastData.map(d=>d.valB), type: 'scatter', mode: 'lines', name: 'AI Prediction', line: {color: '#ff3366', width: 2, dash: 'dashdot'} }
                        ], darkLayout, {displayModeBar: false});
                    }
                });
        }

        // Full Distribution Logs
        function loadFullLogs() {
            fetch('/api/distribution/')
                .then(res => res.json())
                .then(data => {
                    const tbody = document.getElementById('full-logs-body');
                    tbody.innerHTML = '';
                    if(data.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--text-secondary);">No distribution logs found in database.</td></tr>';
                        return;
                    }
                    data.forEach(log => {
                        const date = new Date(log.timestamp).toLocaleString();
                        const fuelColor = log.fuel_type === 'Pertamax' ? '#00e5ff' : (log.fuel_type === 'Solar' ? '#9d00ff' : '#ff3366');
                        const row = `<tr>
                            <td>#LOG-${log.id}</td>
                            <td>${log.depot_name}</td>
                            <td>${log.station_name}</td>
                            <td><span style="color: ${fuelColor}; font-weight: 600;">${log.fuel_type}</span></td>
                            <td>${log.quantity.toLocaleString()} L</td>
                            <td>${date}</td>
                        </tr>`;
                        tbody.insertAdjacentHTML('beforeend', row);
                    });
                })
                .catch(() => {
                    document.getElementById('full-logs-body').innerHTML = '<tr><td colspan="6" style="text-align: center; color: var(--danger);">Failed to load logs.</td></tr>';
                });
        }

        // Tracking Map
        let trackingMap;
        let trackingMapInitialized = false;
        function loadTrackingMap() {
            fetch('/api/tracking/active-fleet')
                .then(response => response.json())
                .then(fleet => {
                    if(!trackingMapInitialized) {
                        trackingMap = L.map('tracking-map').setView([-6.150000, 106.900000], 11);
                        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                            attribution: '&copy; <a href="https://carto.com/">CARTO</a>'
                        }).addTo(trackingMap);
                        trackingMapInitialized = true;
                    }

                    var glowIcon = L.divIcon({
                        className: 'custom-div-icon',
                        html: "<div style='background-color:#00e5ff; width:15px; height:15px; border-radius:50%; box-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff;'></div>",
                        iconSize: [15, 15], iconAnchor: [7, 7]
                    });
                    
                    var idleIcon = L.divIcon({
                        className: 'custom-div-icon',
                        html: "<div style='background-color:#ffb300; width:15px; height:15px; border-radius:50%; box-shadow: 0 0 10px #ffb300, 0 0 20px #ffb300;'></div>",
                        iconSize: [15, 15], iconAnchor: [7, 7]
                    });

                    // Clear previous markers
                    trackingMap.eachLayer((layer) => {
                        if (layer instanceof L.Marker) {
                            trackingMap.removeLayer(layer);
                        }
                    });

                    const fleetList = document.getElementById('fleet-list');
                    fleetList.innerHTML = '';
                    
                    if(fleet.length === 0) {
                        fleetList.innerHTML = '<tr><td colspan="2" style="text-align: center; color: var(--text-secondary);">No active fleet data found.</td></tr>';
                    }
                    
                    fleet.forEach(t => {
                        let icon = t.status === 'Moving' ? glowIcon : idleIcon;
                        L.marker([t.lat, t.lng], {icon: icon}).addTo(trackingMap)
                            .bindPopup(`<b>${t.truck_id}</b><br>Status: ${t.status}<br>Speed: ${t.speed} km/h`);
                            
                        const statusBadge = t.status === 'Moving' ? 'badge-info' : 'badge-warning';
                        fleetList.innerHTML += `
                            <tr>
                                <td><strong>${t.truck_id}</strong><br><span style="font-size:0.8rem;color:var(--text-secondary)">Speed: ${t.speed} km/h</span></td>
                                <td><span class="badge-pill ${statusBadge}">${t.status}</span></td>
                            </tr>
                        `;
                    });
                });
        }

        // Analytics Data
        function loadAnalytics() {
            fetch('/api/analytics/fuel-breakdown')
                .then(res => res.json())
                .then(data => {
                    // Update KPIs
                    document.getElementById('kpi-pertalite').innerText = (data.current_stock_kl.Pertalite / 1000).toFixed(1) + "k kL";
                    const totalPertamax = data.current_stock_kl.Pertamax + data.current_stock_kl['Pertamax Turbo'];
                    document.getElementById('kpi-pertamax').innerText = (totalPertamax / 1000).toFixed(1) + "k kL";
                    const totalSolar = data.current_stock_kl.Solar + data.current_stock_kl.Dexlite;
                    document.getElementById('kpi-solar').innerText = (totalSolar / 1000).toFixed(1) + "k kL";

                    // 1. Donut Chart (Volume Share)
                    const labels = Object.keys(data.volume_share);
                    const values = Object.values(data.volume_share);
                    const colors = ['#00e5ff', '#ff3366', '#ffb300', '#00e676', '#9d00ff'];
                    
                    Plotly.newPlot('fuel-donut-chart', [{
                        values: values, labels: labels, type: 'pie', hole: .6,
                        marker: { colors: colors },
                        textinfo: 'percent', hoverinfo: 'label+percent'
                    }], { ...darkLayout, showlegend: true, margin: {t:20, b:20, l:20, r:20} }, {displayModeBar: false});

                    // 2. Trend Chart (Line)
                    const trend = data.weekly_trend;
                    Plotly.newPlot('fuel-trend-chart', [
                        { x: trend.days, y: trend.Pertalite, name: 'Pertalite', type: 'scatter', mode: 'lines+markers', line: {color: '#00e5ff', width: 3} },
                        { x: trend.days, y: trend.Pertamax, name: 'Pertamax', type: 'scatter', mode: 'lines+markers', line: {color: '#ff3366', width: 3} },
                        { x: trend.days, y: trend.Solar, name: 'Solar', type: 'scatter', mode: 'lines+markers', line: {color: '#00e676', width: 3} }
                    ], { ...darkLayout, margin: {t:20, b:40, l:40, r:20}, legend: {orientation: 'h', y: -0.2} }, {displayModeBar: false});

                    // 3. Stock Chart (Bar)
                    const stockLabels = Object.keys(data.current_stock_kl);
                    const stockValues = Object.values(data.current_stock_kl);
                    Plotly.newPlot('fuel-stock-chart', [{
                        x: stockLabels, y: stockValues, type: 'bar',
                        marker: { color: colors, opacity: 0.8 }
                    }], { ...darkLayout, margin: {t:20, b:40, l:40, r:20} }, {displayModeBar: false});
                });
        }
    