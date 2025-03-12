import React, { useEffect, useState } from 'react';
import Sidebar from './components/Sidebar';
import LiveMap from './components/LiveMap';
import RightSidebar from './components/RightSidebar';

import './App.css';

const App = () => {
  const [devices, setDevices] = useState([]);

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const res = await fetch("http://localhost:5001/devices");
        const data = await res.json();

        const enriched = data.map((d, i) => ({
          ...d,
          latitude: 40.7128 + i * 0.01,
          longitude: -74.0060 + i * 0.01
        }));

        setDevices(enriched);
      } catch (err) {
        console.error("Error fetching devices:", err);
      }
    };

    fetchDevices();
    const interval = setInterval(fetchDevices, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <Sidebar devices={devices} />
      {devices.length > 0 && <LiveMap devices={devices} />}
      <RightSidebar />
    </div>
  );
};

export default App;