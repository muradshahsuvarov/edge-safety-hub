import React from 'react';
import './DeviceCard.css'; // optional for styling

const DeviceCard = ({ device }) => {
  return (
    <div className="device-card">
      <h4>{device.name}</h4>
      <p><strong>Type:</strong> {device.type}</p>
      <p><strong>ID:</strong> {device.device_id}</p>
      <p><strong>User ID:</strong> {device.user_id}</p>
    </div>
  );
};

export default DeviceCard;