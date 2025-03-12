import React, { useEffect, useState, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import './LiveMap.css';

import workerIconImg from '../assets/worker-icon.png';
import gasSensorIconImg from '../assets/gas-sensor-icon.png';

import { ZoomControl } from 'react-leaflet';

const createIcon = (iconUrl) =>
  new L.Icon({
    iconUrl,
    iconSize: [48, 48],
    iconAnchor: [24, 48],
    popupAnchor: [0, -48]
  });

const workerIcon = createIcon(workerIconImg);
const gasSensorIcon = createIcon(gasSensorIconImg);

const RecenterMap = ({ lat, lng, onCenter }) => {
  const map = useMap();
  useEffect(() => {
    map.setView([lat, lng]);
    if (onCenter) onCenter();
  }, [lat, lng]);
  return null;
};

// 🟢 Predefined gas sensor positions (static in park)
const staticGasSensorCoordinates = [
  [40.71315, -74.00565],
  [40.7129, -74.0058],
  [40.71277, -74.00615],
  [40.71325, -74.00595],
  [40.71255, -74.0055],
  [40.71265, -74.00625],
];

const LiveMap = ({ devices }) => {
  const [userMap, setUserMap] = useState({});
  const [mapCenter, setMapCenter] = useState(null);
  const [gasSensors, setGasSensors] = useState([]); // ✅ Static gas sensor list
  const hasCenteredMap = useRef(false);

  useEffect(() => {
    if (!devices || devices.length === 0) return;

    const grouped = {};
    devices.forEach((device) => {
      if (!grouped[device.user_id]) {
        grouped[device.user_id] = {
          user_id: device.user_id,
          devices: [],
        };
      }
      grouped[device.user_id].devices.push(device);
    });

    const enrichUsers = async () => {
      const enriched = await Promise.all(
        Object.values(grouped).map(async (user) => {
          try {
            const res = await fetch(`http://localhost:5001/users/${user.user_id}/latest-motion`);
            if (!res.ok) throw new Error("No motion data");
            const loc = await res.json();

            return {
              ...user,
              lat: loc.latitude,
              lng: loc.longitude
            };
          } catch (e) {
            console.warn(`Skipping user ${user.user_id} (no location)`);
            return null;
          }
        })
      );

      const result = enriched.filter(Boolean);
      const mapped = {};
      result.forEach((u) => (mapped[u.user_id] = u));
      setUserMap(mapped);

      if (result.length > 0 && !hasCenteredMap.current) {
        setMapCenter([result[0].lat, result[0].lng]);
      }
    };

    enrichUsers();
  }, [devices]);

  // ✅ Only generate gas sensors once
  useEffect(() => {
    const assignedSensors = [];
    const numSensors = 2;
    for (let i = 0; i < numSensors; i++) {
      const randomIndex = Math.floor(Math.random() * staticGasSensorCoordinates.length);
      assignedSensors.push(staticGasSensorCoordinates[randomIndex]);
    }
    setGasSensors(assignedSensors);
  }, []);

  if (!mapCenter) return <div>Loading map...</div>;

  const users = Object.values(userMap);
  const mapKey = `${mapCenter[0]}-${mapCenter[1]}`;

  return (
    <div className="map-container" key={mapKey}>
      <MapContainer
        center={mapCenter}
        zoom={13}
        scrollWheelZoom={true}
        zoomControl={false} // disables top-left controls
        style={{ height: '100vh', width: '100%' }}
      >
        <ZoomControl position="bottomleft" />
        {!hasCenteredMap.current && (
          <RecenterMap
            lat={mapCenter[0]}
            lng={mapCenter[1]}
            onCenter={() => (hasCenteredMap.current = true)}
          />
        )}

        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* 👷 Worker icons (live) */}
        {users.map((user) => (
          <Marker
            key={`user-${user.user_id}`}
            position={[user.lat, user.lng]}
            icon={workerIcon}
          >
            <Popup>
              <strong>User ID: {user.user_id}</strong>
              <ul>
                {user.devices.map((device) => (
                  <li key={device.device_id}>
                    <strong>{device.name}</strong> ({device.type})
                  </li>
                ))}
              </ul>
            </Popup>
          </Marker>
        ))}

        {/* 🟡 Static gas sensors (park) */}
        {gasSensors.map(([lat, lng], idx) => (
          <Marker
            key={`gas-sensor-static-${idx}`}
            position={[lat, lng]}
            icon={gasSensorIcon}
          >
            <Popup>
              <strong>Gas Sensor #{idx + 1}</strong>
              <div>Located in City Hall Park</div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default LiveMap;