import React, { useState } from 'react';
import DeviceCard from './DeviceCard';
import './Sidebar.css';

const Sidebar = ({ devices }) => {
  const [visible, setVisible] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  const toggleSidebar = () => {
    setVisible(prev => !prev);
  };

  const handleSearch = () => {
    // Filtering happens automatically via filteredDevices
  };

  const clearSearch = () => {
    setSearchTerm('');
  };

  const filteredDevices = devices.filter(device =>
    device.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className={`left-sidebar-wrapper ${visible ? 'visible' : 'hidden'}`}>
      <div className="sidebar">
        <h1 className="company-title">Blackline safety corp.</h1>

        <div className="view-toggle">
          <button className="active">Live View</button>
          <button>History View</button>
        </div>

        <div className="filter-options">
          <h4 className="filter-title">Filter by Type</h4>
          <div className="filter-checkbox-group">
            <label className="filter-checkbox">
              <input type="checkbox" defaultChecked />
              <span>🧪 Gas Detector</span>
            </label>
            <label className="filter-checkbox">
              <input type="checkbox" defaultChecked />
              <span>❤️ Heart Rate Detector</span>
            </label>
            <label className="filter-checkbox">
              <input type="checkbox" defaultChecked />
              <span>🏃 Motion Detector</span>
            </label>
          </div>
        </div>

        <div className="search-box">
          <input
            type="text"
            placeholder="Search"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
          <a className="clear-link" onClick={clearSearch}>Clear search</a>
        </div>

        <div className="locate-toggle">
          <span>Locate once</span>
          <span>Continuous locate</span>
        </div>

        <h3 className="live-feed-title">Live Feed</h3>
        <label className="checkbox">
          <input type="checkbox" /> Show bridges
        </label>
        <label className="checkbox">
          <input type="checkbox" defaultChecked /> Show offline
        </label>

        <div className="device-list">
          {filteredDevices.map(device => (
            <DeviceCard key={device.device_id} device={device} />
          ))}
        </div>
      </div>

      <button className="toggle-left-sidebar-btn" onClick={toggleSidebar}>
        {visible ? '←' : '→'}
      </button>
    </div>
  );
};

export default Sidebar;