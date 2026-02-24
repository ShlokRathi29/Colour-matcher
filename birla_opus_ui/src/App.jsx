import { useState, useRef } from 'react';
import logo from "./logo.png"

function App() {
  const [dragActive, setDragActive] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (file) => {
    if (!file.type.match('image.*')) {
      setError('Please upload an image file (JPG or PNG)');
      return;
    }

    setError(null);
    setResult(null);

    const reader = new FileReader();
    reader.onload = (e) => {
      setImagePreview(e.target.result);
    };
    reader.readAsDataURL(file);

    setLoading(true);

    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/match?k=5', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to process image. Please try again.');
      setImagePreview(null);
    } finally {
      setLoading(false);
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  const handleReset = () => {
    setImagePreview(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-cream-50 via-cream-100 to-warm-50 py-8 px-4 sm:py-12 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 sm:mb-12 animate-fade-in">
          <img
            src={logo}
            alt="Birla Opus"
            className="h-10"
          />
          <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-900 mb-3 tracking-tight">
            Birla Opus
          </h1>
          <p className="font-body text-lg sm:text-xl text-slate-600 font-light tracking-wide">
            Shade Matcher
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-elegant p-6 sm:p-8 lg:p-10 border border-slate-100 animate-slide-up">
          {/* Upload Zone */}
          {!imagePreview && (
            <div
              className={`upload-zone relative border-2 border-dashed rounded-xl p-8 sm:p-12 text-center transition-all duration-300 ${dragActive
                  ? 'border-accent-500 bg-accent-50'
                  : 'border-slate-300 bg-slate-50 hover:border-slate-400 hover:bg-slate-100'
                } ${loading ? 'opacity-50 pointer-events-none' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                accept="image/*"
                onChange={handleChange}
                disabled={loading}
              />

              <div className="upload-icon mx-auto mb-4">
                <svg
                  className="w-16 h-16 sm:w-20 sm:h-20 mx-auto text-slate-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
              </div>

              <p className="font-body text-lg sm:text-xl text-slate-700 mb-2 font-medium">
                Drop your image here
              </p>
              <p className="font-body text-sm text-slate-500 mb-6">
                or click to browse
              </p>

              <button
                onClick={handleButtonClick}
                disabled={loading}
                className="btn-primary px-6 py-3 bg-accent-600 hover:bg-accent-700 text-white font-medium rounded-lg transition-all duration-200 shadow-sm hover:shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Processing...' : 'Choose Image'}
              </button>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg animate-fade-in">
              <p className="font-body text-red-700 text-sm">{error}</p>
            </div>
          )}

          {/* Image Preview */}
          {imagePreview && (
            <div className="mb-8 animate-fade-in">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-display text-lg font-semibold text-slate-800">
                  Uploaded Image
                </h3>
                <button
                  onClick={handleReset}
                  className="text-sm text-slate-600 hover:text-slate-900 font-medium transition-colors"
                >
                  Upload New
                </button>
              </div>
              <div className="relative rounded-lg overflow-hidden bg-slate-100 max-h-64">
                <img
                  src={imagePreview}
                  alt="Uploaded preview"
                  className="w-full h-full object-contain"
                />
              </div>
            </div>
          )}

          {/* Loading Spinner */}
          {loading && (
            <div className="py-12 flex flex-col items-center justify-center animate-fade-in">
              <div className="spinner w-12 h-12 border-4 border-slate-200 border-t-accent-600 rounded-full animate-spin mb-4"></div>
              <p className="font-body text-slate-600">Analyzing color...</p>
            </div>
          )}

          {/* Results */}
          {result && !loading && (
            <div className="space-y-8 animate-fade-in">
              {/* Detected Color */}
              <div>
                <h3 className="font-display text-lg font-semibold text-slate-800 mb-4">
                  Detected Color
                </h3>
                <div className="bg-slate-50 rounded-lg p-6 border border-slate-200">
                  <div className="flex items-center gap-6">
                    <div
                      className="w-20 h-20 rounded-lg shadow-color border border-slate-200"
                      style={{
                        backgroundColor: `rgb(${result.input_rgb.r}, ${result.input_rgb.g}, ${result.input_rgb.b})`,
                      }}
                    ></div>
                    <div className="flex-1 grid grid-cols-2 gap-4">
                      <div>
                        <p className="font-body text-xs text-slate-500 uppercase tracking-wide mb-1">
                          RGB
                        </p>
                        <p className="font-mono text-sm text-slate-900">
                          {result.input_rgb.r}, {result.input_rgb.g},{' '}
                          {result.input_rgb.b}
                        </p>
                      </div>
                      <div>
                        <p className="font-body text-xs text-slate-500 uppercase tracking-wide mb-1">
                          LAB
                        </p>
                        <p className="font-mono text-sm text-slate-900">
                          {result.input_lab.L.toFixed(1)},{' '}
                          {result.input_lab.a.toFixed(1)},{' '}
                          {result.input_lab.b.toFixed(1)}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Best Match */}
              <div>
                <h3 className="font-display text-lg font-semibold text-slate-800 mb-4">
                  Best Match
                </h3>
                <div className="bg-gradient-to-br from-accent-50 to-warm-50 rounded-lg p-6 border border-accent-200 shadow-sm">
                  <div className="flex items-center gap-6 mb-6">
                    <div
                      className="w-24 h-24 rounded-lg shadow-color-lg border-2 border-white"
                      style={{
                        backgroundColor: `rgb(${result.best_match.rgb.r}, ${result.best_match.rgb.g}, ${result.best_match.rgb.b})`,
                      }}
                    ></div>
                    <div className="flex-1">
                      <h4 className="font-display text-xl font-bold text-slate-900 mb-1">
                        {result.best_match.shade_name}
                      </h4>
                      <p className="font-mono text-sm text-slate-600 mb-3">
                        {result.best_match.shade_id}
                      </p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 pt-4 border-t border-accent-200">
                    <div className="text-center">
                      <p className="font-body text-xs text-slate-600 uppercase tracking-wide mb-1">
                        Confidence
                      </p>
                      <p className="font-display text-2xl font-bold text-accent-700">
                        {(result.best_match.confidence * 100).toFixed(1)}%
                      </p>
                    </div>
                    <div className="text-center">
                      <p className="font-body text-xs text-slate-600 uppercase tracking-wide mb-1">
                        ΔE 2000
                      </p>
                      <p className="font-display text-2xl font-bold text-slate-700">
                        {result.best_match.delta_e_2000.toFixed(2)}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Top Matches */}
              {result.top_matches && result.top_matches.length > 0 && (
                <div>
                  <h3 className="font-display text-lg font-semibold text-slate-800 mb-4">
                    Other Matches
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    {result.top_matches.map((match, index) => (
                      <div
                        key={index}
                        className="bg-slate-50 rounded-lg p-4 border border-slate-200 hover:border-slate-300 transition-colors"
                      >
                        <div className="flex items-center gap-4">
                          <div
                            className="w-12 h-12 rounded-md shadow-sm border border-slate-200 flex-shrink-0"
                            style={{
                              backgroundColor: `rgb(${match.rgb.r}, ${match.rgb.g}, ${match.rgb.b})`,
                            }}
                          ></div>
                          <div className="flex-1 min-w-0">
                            <h5 className="font-body text-sm font-semibold text-slate-900 truncate">
                              {match.shade_name}
                            </h5>
                            <p className="font-mono text-xs text-slate-600 mb-1">
                              {match.shade_id}
                            </p>
                            <p className="font-body text-xs text-slate-500">
                              {(match.confidence * 100).toFixed(1)}% match
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Disclaimer */}
        <p className="font-body text-xs text-center text-slate-500 mt-6 animate-fade-in">
          Results may vary based on lighting and image quality.
        </p>
      </div>
    </div>
  );
}

export default App;