'use client';
import { useState, useEffect } from 'react';

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

  // Simulate a live feed adding a new incident after 5 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      setIncidents(prev => [{
        id: 5, 
        title: 'SQS-DLQ-Spike', 
        desc: 'Triaged 45 corrupted messages and flushed DLQ.', 
        time: 'Just now', 
        type: 'success'
      }, ...prev]);
      
      setLogs(prev => [{
        id: '106', resource: 'payment-dlq-queue', action: 'Flush Queue', justification: 'Malformed JSON payload detected.', status: 'SUCCESS'
      }, ...prev]);
    }, 5000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="header">
        <div>
          <h1>ACRA Command Center</h1>
          <p>Autonomous Cloud Remediation Agent - Live Telemetry</p>
        </div>
        <div className="status-badge">
          <div className="status-dot"></div>
          Agent Online & Monitoring
        </div>
      </header>

      {/* Hero Metrics */}
      <div className="metrics-grid">
        <div className="glass-panel">
          <p>Total Incidents Remediated</p>
          <div className="metric-value" style={{ color: 'var(--accent-primary)' }}>1,284</div>
          <p style={{ fontSize: '0.875rem' }}>+5 this week</p>
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

      <div className="main-grid">
        {/* Live Incident Feed */}
        <section className="glass-panel">
          <h2>
            <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
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
            <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
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
