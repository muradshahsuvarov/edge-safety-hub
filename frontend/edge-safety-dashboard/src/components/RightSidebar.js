import React, { useState, useEffect, useRef } from 'react';
import './RightSidebar.css';

const RightSidebar = () => {
  const [visible, setVisible] = useState(true);
  const [alertsVisible, setAlertsVisible] = useState(false);
  const [alerts, setAlerts] = useState([]);
  const [gasReadings, setGasReadings] = useState([]);
  const [hasUnreadAlerts, setHasUnreadAlerts] = useState(false);
  const lastSeenAlertId = useRef(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await fetch("http://localhost:5001/alerts");
        const data = await res.json();
        setAlerts(data.slice(0, 10));

        if (data.length > 0) {
          const latestId = data[0].id;
          if (lastSeenAlertId.current === null) {
            lastSeenAlertId.current = latestId;
          } else if (latestId > lastSeenAlertId.current) {
            setHasUnreadAlerts(true);
          }
        }
      } catch (err) {
        console.error("Failed to fetch alerts:", err);
      }
    };

    const fetchGasReadings = async () => {
      try {
        const res = await fetch("http://localhost:5001/gas-sensors/latest");
        const data = await res.json();
        setGasReadings(data);
      } catch (err) {
        console.error("Failed to fetch gas levels:", err);
      }
    };

    fetchAlerts();
    fetchGasReadings();
    const interval = setInterval(() => {
      fetchAlerts();
      fetchGasReadings();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const toggleSidebar = () => {
    setVisible((prev) => !prev);
  };

  const toggleAlerts = () => {
    setAlertsVisible((prev) => !prev);
    setHasUnreadAlerts(false);
    if (alerts.length > 0) {
      lastSeenAlertId.current = alerts[0].id;
    }
  };

  return (
    <div className={`right-sidebar-wrapper ${visible ? 'visible' : 'hidden'}`}>
      <div className="right-sidebar">
        <div className="user-profile">
          <h3>Kiki Wash</h3>
          <p><strong>Organization:</strong> ACME Corp.</p>
          <p><strong>M:</strong> 403-123-4567</p>
        </div>

        <div className="sensor-readings">
          <h4>📊 Live Gas Readings</h4>
          <ul>
            {gasReadings.map((reading, index) => {
              let gasLevel;
              try {
                const parsed = JSON.parse(reading.latest_gas_level);
                gasLevel = parsed.gas_level;
              } catch (err) {
                gasLevel = null;
              }
              return (
                <li key={reading.device_id}>
                  <div>
                    {`Gas Detector #${index + 1}`}{" "}
                    <strong>{gasLevel !== null && gasLevel !== undefined ? `${gasLevel} ppm` : "N/A ppm"}</strong>
                  </div>
                  <span>{reading.timestamp ? new Date(reading.timestamp).toLocaleString() : 'No data'}</span>
                </li>
              );
            })}
          </ul>
          <p>Next bump test: <strong>2022-05-06 15:29:34 MDT</strong></p>
          <p>Next calibration due: <strong>2022-05-06 15:29:34 MDT</strong></p>
        </div>

        <div className="communication-info">
          <h4>⏰ Last Communication</h4>
          <p><strong>May 06, 2022 at 15:38 MDT</strong></p>
          <p><strong>Battery:</strong> 60%</p>
          <p><strong>Signal Strength:</strong> 80%</p>
        </div>

        <div className="quick-actions">
          <button>📍 Find my G6</button>
          <button>📅 View today's history</button>
          <button>⚙️ Configuration profile</button>
        </div>

        <div className="alerts-section">
          <button onClick={toggleAlerts} className="toggle-alerts-btn">
            {alertsVisible ? "⬆ Hide Alerts" : "⬇ Show Alerts"}
          </button>

          {alertsVisible && (
            <div className="alerts-list">
              {alerts.map((alert) => (
                <div key={alert.id} className="alert-card">
                  <h5>{alert.alert_type.toUpperCase()} ALERT</h5>
                  <p><strong>Device:</strong> {alert.device_id}</p>
                  <p><strong>Time:</strong> {new Date(alert.timestamp).toLocaleString()}</p>
                  <p className="alert-message">{alert.message}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {hasUnreadAlerts && (
        <div
          className="alert-indicator"
          title="New alert! Click to open alerts"
          onClick={toggleAlerts}
        >
          ⚠️
        </div>
      )}

      <button className="toggle-right-sidebar-btn" onClick={toggleSidebar}>
        {visible ? '→' : '←'}
      </button>
    </div>
  );
};

export default RightSidebar;