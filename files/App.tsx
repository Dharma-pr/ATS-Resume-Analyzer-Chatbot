import React, { useState } from 'react';
import { UploadSection } from './components/UploadSection';
import { AnalysisPage } from './pages/Analysis';
import './styles/globals.css';

function App() {
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [jobId, setJobId] = useState<number | null>(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            🤖 ATS Resume Analyzer
          </h1>
          <p className="text-gray-600 mt-2">
            Get AI-powered feedback on your resume with semantic analysis and interactive chatbot
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {!resumeId || !jobId ? (
          <UploadSection onResumeUploaded={setResumeId} onJobUploaded={setJobId} />
        ) : (
          <AnalysisPage resumeId={resumeId} jobId={jobId} />
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center text-gray-600">
          <p>© 2024 ATS Resume Analyzer. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;