import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';  // Replace with your Django backend URL

// Function to get MilkRecords
export const getMilkRecords = () => {
  return axios.get(`${API_URL}milk-records/`);
};

// Function to create MilkRecord
export const createMilkRecord = (data) => {
  return axios.post(`${API_URL}milk-records/`, data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
};

// Function to get QR Codes
export const getQRCodes = () => {
  return axios.get(`${API_URL}qrcodes/`);
};

// Function to send Message
export const sendMessage = (data) => {
  return axios.post(`${API_URL}messages/`, data, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
};

// Function to get Login History
export const getLoginHistory = () => {
  return axios.get(`${API_URL}login-history/`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('access_token')}`,
    },
  });
};

// Function to register a new user
export const registerUser = (data) => {
  return axios.post(`${API_URL}register/`, data);
};
