const machinesEl = document.getElementById('machines');
const incidentsEl = document.getElementById('incidents');
const connectionEl = document.getElementById('connection');
const dot = document.getElementById('dot');
const fleetHealth = document.getElementById('fleetHealth');
const incidentCount = document.getElementById('incidentCount');

const labels = {temperature:'Temperature', vibration:'Vibration', current:'Current', rpm:'RPM'};
const units = {temperature:'°C', vibration:'g', current:'A', rpm:'rpm'};

function renderMachines(data){
  machinesEl.innerHTML = data.map(m => `
    <article class="card ${m.state !== 'normal' ? 'alert' : ''}">
      <div class="card-top">
        <div class="machine">${m.machine}</div>
        <div class="state ${m.state}">${m.state}</div>
      </div>
      <div class="health">
        <div class="health-line"><span>HEALTH</span><span>${m.health}%</span></div>
        <div class="bar"><i style="width:${m.health}%"></i></div>
      </div>
      <div class="sensors">
        ${Object.entries(m.values).map(([key,value]) => `
          <div class="sensor">
            <label>${labels[key]}</label>
            <b>${value} <em>${units[key]}</em></b>
            <em>anomaly ${m.scores[key].toFixed(1)}σ</em>
          </div>`).join('')}
      </div>
      <button class="fault" onclick="simulateFault('${m.machine}')">⚠ Simulate Fault</button>
    </article>`).join('');

  const health = data.reduce((a,m)=>a+m.health,0)/data.length;
  fleetHealth.textContent = `${Math.round(health)}%`;
}

function renderIncidents(items){
  incidentCount.textContent = items.length;
  if(!items.length){ incidentsEl.innerHTML = '<p class="empty">No anomalies detected.</p>'; return; }
  incidentsEl.innerHTML = items.map(i => `
    <div class="incident">
      <div class="incident-head"><strong>${i.machine} · ${i.sensor}</strong><span class="sev ${i.severity}">${i.severity.toUpperCase()}</span></div>
      <p>${i.value} detected · anomaly score ${i.score}σ</p>
    </div>`).join('');
}

async function simulateFault(machine){
  await fetch(`/api/fault/${machine}`, {method:'POST'});
}
window.simulateFault = simulateFault;

function connect(){
  const ws = new WebSocket(`${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws`);
  ws.onopen = () => { connectionEl.textContent='CONNECTED'; dot.style.background='#72f0c0'; };
  ws.onclose = () => { connectionEl.textContent='RECONNECTING'; dot.style.background='#e5a64d'; setTimeout(connect,1500); };
  ws.onmessage = event => {
    const payload = JSON.parse(event.data);
    renderMachines(payload.data);
    renderIncidents(payload.incidents);
  };
}
connect();
