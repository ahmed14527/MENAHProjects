import React, { useState, useEffect } from 'react';
import { getQRCodes } from '../api';

const QRCodeList = () => {
  const [qrcodes, setQRCodes] = useState([]);

  useEffect(() => {
    const fetchQRCodes = async () => {
      const response = await getQRCodes();
      setQRCodes(response.data);
    };

    fetchQRCodes();
  }, []);

  return (
    <div>
      <h2>QR Codes</h2>
      <ul>
        {qrcodes.map((qr) => (
          <li key={qr.code}>
            {qr.code} - {qr.milk_record.baby_name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default QRCodeList;
