'use client';
import { useState, useEffect } from 'react';

const PREDICTIONS = [
  {
    id: 'p1',
    instance: 'i-prod-web-server-01',
    label: 'Prod Web Server',
    region: 'ap-south-1',
    cpuPoints: [55, 63, 70, 76, 83, 88],
    minutesToFailure: 18,
    confidence: 92,
    urgency: 'critical',
  },
  {
    id: 'p2',
    instance: 'i-staging-api-server-03',
    label: 'Staging API Server',
    region: 'us-east-1',
    cpuPoints: [40, 44, 49, 54, 58, 63],
    minutesToFailure: 55,
    confidence: 71,
    urgency: 'warning',
  },
];

function Sparkline({ points, urgency }) {
  const max = 100;
  const width = 120;
  const height = 36;
  const step = width / (points.length - 1);
  const coords = points.map((v, i) => `${i * step},${height - (v / max) * height}`).join(' ');
  const colorMap = { critical: '#ef4444', warning: '#f59e0b', stable: '#10b981' };
  const color = colorMap[urgency] || '#6366f1';
  return (
    <svg width={width} height={height} style={{ overflow: 'visible' }}>
      <polyline
        fill="none"
        stroke={color}
        strokeWidth="2"
        strokeLinejoin="round"
        points={coords}
      />
      {points.map((v, i) => (
        <circle key={i} cx={i * step} cy={height - (v / max) * height} r="2.5" fill={color} />
      ))}
    </svg>
  );
}

function Countdown({ initialMinutes, urgency }) {
  const [mins, setMins] = useState(initialMinutes);
  useEffect(() => {
    const iv = setInterval(() => setMins(m => Math.max(0, m - 1)), 60000);
    return () => clearInterval(iv);
  }, []);
  const colorMap = { critical: 'var(--danger)', warning: 'var(--warning)' };
  return (
    <span style={{ color: colorMap[urgency] || 'var(--text-muted)', fontWeight: 700, fontSize: '1.1rem' }}>
      ~{mins} min
    </span>
  );
}

export default function Dashboard() {
  const [incidents, setIncidents] = useState([
    { id: 1, title: 'Cost-Anomaly-Detected', desc: 'Terminated idle EC2 i-dev-sandbox-999 and deleted 3 unattached EBS volumes.', time: 'Just now', type: 'success' },
    { id: 2, title: 'S3-Public-Access-Drift', desc: 'Bucket acra-vulnerable-production-data locked down.', time: '1 hr ago', type: 'danger' },
    { id: 3, title: 'RDS-High-Database-Connections', desc: 'Cleared 12 hanging database connections.', time: '3 hrs ago', type: 'warning' },
    { id: 4, title: 'Disk-Space-Critical-AppServer', desc: 'Archived 40GB of logs to S3 bucket.', time: '6 hrs ago', type: 'warning' },
  ]);

  const [logs, setLogs] = useState([
    { id: '101', resource: 'i-dev-sandbox-999', action: 'Terminate Instance', justification: 'CPU < 5% for 14 days. Wasting $145/mo.', status: 'SUCCESS' },
    { id: '102', resource: 'acra-vulnerable-production-data', action: 'BPA Enabled', justification: 'Human approval received. Securing exposed bucket.', status: 'SUCCESS' },
    { id: '103', resource: 'production-db-cluster-1', action: 'Connections Dropped', justification: 'Connection pool hit 100%. Deadlock mitigation.', status: 'SUCCESS' },
    { id: '104', resource: 'i-99988877766655544', action: 'Archive to S3', justification: 'Disk space at 95% due to application logs.', status: 'SUCCESS' },
    { id: '105', resource: 'i-1234567890abcdef0', action: 'Reboot Aborted', justification: 'Instance ID not found in current region. Cannot proceed.', status: 'INFO' },
  ]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIncidents(prev => [{
        id: 5,
        title: 'Predictive-CPU-Spike',
        desc: 'Pre-emptive restart of i-prod-web-server-01 executed before crash.',
        time: 'Just now',
        type: 'success'
      }, ...prev]);
      setLogs(prev => [{
        id: '106', resource: 'i-prod-web-server-01', action: 'Pre-emptive Restart', justification: 'AI predicted crash in 18 min. Human approved early restart.', status: 'SUCCESS'
      }, ...prev]);
    }, 7000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="header">
        <div>
          <h1>ACRA Command Center</h1>
          <p>Autonomous Cloud Remediation Agent — Live Telemetry</p>
        </div>
        <div className="status-badge">
          <div className="status-dot"></div>
          Agent Online &amp; Monitoring
        </div>
      </header>

      {/* Hero Metrics */}
      <div className="metrics-grid">
        <div className="glass-panel">
          <p>Total Incidents Remediated</p>
          <div className="metric-value" style={{ color: 'var(--accent-primary)' }}>1,285</div>
          <p style={{ fontSize: '0.875rem' }}>+6 this week</p>
        </div>
        <div className="glass-panel">
          <p>Downtime Prevented</p>
          <div className="metric-value" style={{ color: 'var(--success)' }}>342 hrs</div>
          <p style={{ fontSize: '0.875rem' }}>Estimated $45,000 saved</p>
        </div>
        <div className="glass-panel">
          <p>Estimated Monthly Savings</p>
          <div className="metric-value" style={{ color: 'var(--warning)' }}>$1,245</div>
          <p style={{ fontSize: '0.875rem' }}>Via autonomous cleanups</p>
        </div>
      </div>

      {/* Predictive Alerts Banner */}
      <section className="glass-panel prediction-section">
        <h2>
          <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
            <path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
            <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
          </svg>
          Predictive Failure Analysis
          <span className="pred-badge">{PREDICTIONS.length} Active Warnings</span>
        </h2>
        <div className="prediction-grid">
          {PREDICTIONS.map(p => (
            <div key={p.id} className={`prediction-card pred-${p.urgency}`}>
              <div className="pred-header">
                <div>
                  <div className="pred-instance">{p.label}</div>
                  <div className="pred-id">{p.instance} · {p.region}</div>
                </div>
                <div className="pred-confidence">
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '2px' }}>Confidence</div>
                  <div style={{ fontWeight: 700 }}>{p.confidence}%</div>
                </div>
              </div>

              <div className="pred-body">
                <div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '4px' }}>CPU Trend (last 30 min)</div>
                  <Sparkline points={p.cpuPoints} urgency={p.urgency} />
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                    {p.cpuPoints[0]}% → {p.cpuPoints[p.cpuPoints.length - 1]}%
                  </div>
                </div>
                <div className="pred-countdown">
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '4px' }}>Predicted crash in</div>
                  <Countdown initialMinutes={p.minutesToFailure} urgency={p.urgency} />
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '6px' }}>Pre-emptive action pending</div>
                </div>
              </div>

              <button className={`pred-action-btn ${p.urgency}`}>
                Approve Pre-emptive Restart
              </button>
            </div>
          ))}
        </div>
      </section>

      <div className="main-grid">
        {/* Live Incident Feed */}
        <section className="glass-panel">
          <h2>
            <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            Live Incident Feed
          </h2>
          <div className="feed-list">
            {incidents.map((incident) => (
              <div key={incident.id} className={`feed-item ${incident.type}`}>
                <div className="feed-header">
                  <span className="feed-title">{incident.title}</span>
                  <span className="feed-time">{incident.time}</span>
                </div>
                <p style={{ fontSize: '0.875rem', color: '#fff' }}>{incident.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Audit Logs */}
        <section className="glass-panel">
          <h2>
            <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            DynamoDB Audit Log
          </h2>
          <div style={{ overflowX: 'auto' }}>
            <table className="audit-table">
              <thead>
                <tr>
                  <th>Log ID</th>
                  <th>Resource</th>
                  <th>Action Taken</th>
                  <th>Justification / Reason</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr key={log.id}>
                    <td style={{ color: 'var(--text-muted)' }}>#{log.id}</td>
                    <td style={{ fontFamily: 'monospace', color: 'var(--accent-secondary)' }}>{log.resource}</td>
                    <td style={{ fontWeight: '500' }}>{log.action}</td>
                    <td>{log.justification}</td>
                    <td>
                      <span className={`badge b-${log.status === 'SUCCESS' ? 'success' : 'info'}`}>
                        {log.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}
