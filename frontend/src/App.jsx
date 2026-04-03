import React, { useState, useCallback } from 'react';
import axios from 'axios';
import { 
  CloudArrowUpIcon, 
  DocumentTextIcon, 
  CurrencyDollarIcon, 
  TagIcon, 
  FaceSmileIcon, 
  FaceFrownIcon, 
  HandThumbUpIcon,
  ClipboardIcon,
  ArrowDownTrayIcon
} from '@heroicons/react/24/outline';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const onFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      // Convert file to Base64 to match new API spec
      const reader = new FileReader();
      reader.readAsDataURL(file);
      
      reader.onload = async () => {
        const base64String = reader.result.split(',')[1];
        const fileType = file.name.split('.').pop().toLowerCase();
        
        const payload = {
          fileName: file.name,
          fileType: fileType,
          fileBase64: base64String
        };

        try {
          const response = await axios.post(`${API_URL}/api/document-analyze`, payload, {
            headers: {
              'Content-Type': 'application/json',
              'X-API-Key': import.meta.env.VITE_API_KEY || 'GUVI-AI-2026'
            },
          });
          setResults(response.data);
        } catch (err) {
          console.error('Upload error:', err);
          setError(err.response?.data?.detail || 'An error occurred while processing the document.');
        } finally {
          setLoading(false);
        }
      };

      reader.onerror = (error) => {
        console.error('Error reading file:', error);
        setError('Error reading file for upload');
        setLoading(false);
      };

    } catch (err) {
      console.error('Processing error:', err);
      setError('An error occurred during file processing');
      setLoading(false);
    }
  };

  const getSentimentEmoji = (sentiment) => {
    switch (sentiment?.toUpperCase()) {
      case 'POSITIVE': return <FaceSmileIcon className="w-8 h-8 text-green-500" />;
      case 'NEGATIVE': return <FaceFrownIcon className="w-8 h-8 text-red-500" />;
      default: return <HandThumbUpIcon className="w-8 h-8 text-gray-500" />;
    }
  };

  const getEntityColor = (label) => {
    switch (label) {
      case 'NAMES': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'ORGANIZATIONS': return 'bg-green-100 text-green-800 border-green-200';
      case 'GPE': return 'bg-purple-100 text-purple-800 border-purple-200';
      case 'AMOUNTS': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'DATES': return 'bg-orange-100 text-orange-800 border-orange-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  const downloadJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(results, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href",     dataStr);
    downloadAnchorNode.setAttribute("download", "analysis_results.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100">
      {/* Hero Section */}
      <header className="bg-gradient-to-r from-blue-600 to-indigo-700 py-16 px-4 text-center text-white shadow-lg">
        <h1 className="text-4xl md:text-6xl font-extrabold mb-4">DocuAI Extractor</h1>
        <p className="text-xl opacity-90">AI-Powered Document Analysis & Extraction for GUVI Hackathon</p>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-12">
        {/* Upload Section */}
        <section className="mb-12">
          <div className="bg-white dark:bg-gray-800 p-8 rounded-2xl shadow-xl border-2 border-dashed border-gray-300 dark:border-gray-700 flex flex-col items-center justify-center">
            <CloudArrowUpIcon className="w-16 h-16 text-indigo-500 mb-4" />
            <h2 className="text-2xl font-semibold mb-2">Upload Document</h2>
            <p className="text-gray-500 dark:text-gray-400 mb-6 text-center">PDF, DOCX, JPG, PNG (Max 10MB)</p>
            
            <input 
              type="file" 
              onChange={onFileChange} 
              className="hidden" 
              id="fileInput" 
              accept=".pdf,.docx,.jpg,.jpeg,.png"
            />
            <label 
              htmlFor="fileInput"
              className="cursor-pointer bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-8 rounded-lg transition-colors mb-4"
            >
              {file ? file.name : 'Select File'}
            </label>

            {file && (
              <button 
                onClick={handleUpload}
                disabled={loading}
                className={`flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-12 rounded-lg transition-all ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Processing...
                  </>
                ) : (
                  'Analyze Now'
                )}
              </button>
            )}
            
            {error && <p className="text-red-500 mt-4 font-medium">{error}</p>}
          </div>
        </section>

        {/* Results Section */}
        {results && (
          <section className="animate-fade-in">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-3xl font-bold">Analysis Results</h2>
              <div className="flex gap-3">
                <button 
                  onClick={downloadJSON}
                  className="flex items-center gap-2 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 px-4 py-2 rounded-lg transition-colors font-medium"
                >
                  <ArrowDownTrayIcon className="w-5 h-5" /> Export JSON
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {/* Summary & Sentiment */}
              <div className="md:col-span-2 space-y-8">
                <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-100 dark:border-gray-700 relative group">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400">
                      <DocumentTextIcon className="w-6 h-6" />
                      <h3 className="text-xl font-bold uppercase tracking-wider">AI Summary</h3>
                    </div>
                    <button 
                      onClick={() => copyToClipboard(results.summary)}
                      className="opacity-0 group-hover:opacity-100 transition-opacity p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-full"
                    >
                      <ClipboardIcon className="w-5 h-5 text-gray-500" />
                    </button>
                  </div>
                  <p className="text-lg leading-relaxed text-gray-700 dark:text-gray-300">{results.summary}</p>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
                  {/* Sentiment */}
                  <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-100 dark:border-gray-700 flex flex-col items-center justify-center text-center">
                    <div className="mb-4">{getSentimentEmoji(results.sentiment)}</div>
                    <h3 className="text-lg font-bold text-gray-500 uppercase mb-1">Sentiment</h3>
                    <p className={`text-2xl font-black ${results.sentiment === 'POSITIVE' ? 'text-green-500' : results.sentiment === 'NEGATIVE' ? 'text-red-500' : 'text-gray-500'}`}>
                      {results.sentiment}
                    </p>
                  </div>

                  {/* Money - Remove this section as it's now part of Entities */}
                  <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-100 dark:border-gray-700">
                    <div className="flex items-center gap-2 text-yellow-600 mb-4">
                      <CurrencyDollarIcon className="w-6 h-6" />
                      <h3 className="text-xl font-bold uppercase tracking-wider">Top Entities</h3>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {results.entities.amounts.length > 0 ? (
                        <span className="bg-yellow-100 text-yellow-800 px-4 py-2 rounded-full font-bold text-lg border border-yellow-200">
                          Total Extracted: {results.entities.amounts.length}
                        </span>
                      ) : (
                        <p className="text-gray-500 italic">Financial data listed in entities.</p>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Entities */}
              <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg border border-gray-100 dark:border-gray-700 h-fit">
                <div className="flex items-center gap-2 text-indigo-600 dark:text-indigo-400 mb-6">
                  <TagIcon className="w-6 h-6" />
                  <h3 className="text-xl font-bold uppercase tracking-wider">Entities Detected</h3>
                </div>
                <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                  {Object.entries(results.entities).some(([_, list]) => list.length > 0) ? (
                    Object.entries(results.entities).map(([category, list]) => (
                      list.map((item, idx) => (
                        <div key={`${category}-${idx}`} className={`p-3 rounded-lg border flex justify-between items-center ${getEntityColor(category.toUpperCase())}`}>
                          <span className="font-semibold">{item}</span>
                          <span className="text-xs font-bold px-2 py-1 rounded-md opacity-70 bg-white dark:bg-gray-900 border">{category.toUpperCase()}</span>
                        </div>
                      ))
                    ))
                  ) : (
                    <p className="text-gray-500 italic text-center py-12">No entities identified.</p>
                  )}
                </div>
              </div>
            </div>
          </section>
        )}
      </main>

      <footer className="mt-20 py-8 border-t border-gray-200 dark:border-gray-800 text-center text-gray-500">
        <p>© 2026 DocuAI-Extractor - Built for GUVI Hackathon</p>
      </footer>
    </div>
  );
}

export default App;
