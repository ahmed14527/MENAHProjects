import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MilkRecordList from './components/MilkRecordList';
import QRCodeList from './components/QRCodeList';
import MessageForm from './components/MessageForm';
import RegistrationForm from './components/RegistrationForm';
import LoginForm from './components/LoginForm';  // Add LoginForm here

const App = () => {
  return (
    <Router>
      <div>
        <h1>Milk Management</h1>
        <Routes>
          <Route path="/milk-records" element={<MilkRecordList />} />
          <Route path="/qrcodes" element={<QRCodeList />} />
          <Route path="/send-message" element={<MessageForm />} />
          <Route path="/register" element={<RegistrationForm />} />
          <Route path="/login" element={<LoginForm />} />  {/* Add login route here */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;  // Make sure this is here
