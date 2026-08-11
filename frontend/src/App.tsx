// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Sidebar from './components/ui/Sidebar';
import LoginPage from './pages/Login';

// Placeholder components for now
function Dashboard() {
  return <div className="p-6">Dashboard Page</div>;
}
function News() {
  return <div className="p-6">News Page</div>;
}
function Sources() {
  return <div className="p-6">Sources Page</div>;
}
function Scoring() {
  return <div className="p-6">Scoring Page</div>;
}
function Reports() {
  return <div className="p-6">Reports Page</div>;
}
function Recipients() {
  return <div className="p-6">Recipients Page</div>;
}
function Channels() {
  return <div className="p-6">Channels Page</div>;
}
function Audit() {
  return <div className="p-6">Audit Page</div>;
}

export default function App() {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="flex min-h-screen bg-[#E0F2F7] font-sans">
          <Sidebar />
          <main className="flex-1 overflow-auto">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/news" element={<News />} />
              <Route path="/sources" element={<Sources />} />
              <Route path="/scoring" element={<Scoring />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/recipients" element={<Recipients />} />
              <Route path="/channels" element={<Channels />} />
              <Route path="/audit" element={<Audit />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="*" element={<Navigate to="/login" />} />
            </Routes>
          </main>
        </div>
      </Router>
    </QueryClientProvider>
  );
}
