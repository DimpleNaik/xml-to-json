import React, { useState } from 'react';

export default function XmlToJsonUploader() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [jsonResult, setJsonResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setJsonResult(null);
    setErrorMsg('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setErrorMsg('Please select an XML file to upload.');
      return;
    }
    setLoading(true);
    setErrorMsg('');
    setJsonResult(null);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/api/xmlToJson', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data = await response.json();
      setJsonResult(data);
    } catch (err) {
      setErrorMsg(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadJson = () => {
    if (!jsonResult) return;
    const blob = new Blob([JSON.stringify(jsonResult, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'output.json';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>XML to JSON Converter</h1>
      <div style={styles.uploadSection}>
        <label htmlFor="file-upload" style={styles.customFileLabel}>
          {selectedFile ? selectedFile.name : "Choose XML File"}
          <input
            id="file-upload"
            type="file"
            accept=".xml"
            onChange={handleFileChange}
            style={styles.hiddenFileInput}
          />
        </label>
        <button onClick={handleUpload} disabled={loading} style={styles.uploadButton}>
          {loading ? 'Uploading...' : 'Upload and Convert'}
        </button>
      </div>

      {errorMsg && <p style={styles.errorText}>{errorMsg}</p>}

      {jsonResult && (
        <div style={styles.resultSection}>
          <h3 style={styles.resultTitle}>JSON Output</h3>
          <pre style={styles.jsonOutput}>
            {JSON.stringify(jsonResult, null, 2)}
          </pre>
          <button onClick={handleDownloadJson} style={styles.downloadButton}>
            Download JSON
          </button>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 700,
    margin: '40px auto',
    padding: 30,
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    backgroundColor: '#ffffff',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
    borderRadius: 12,
  },
  title: {
    textAlign: 'center',
    color: '#333',
    marginBottom: 30,
  },
  uploadSection: {
    display: 'flex',
    gap: 15,
    marginBottom: 20,
    justifyContent: 'center',
  },
  customFileLabel: {
    display: 'inline-block',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    borderRadius: 6,
    cursor: 'pointer',
    userSelect: 'none',
    fontWeight: '600',
    boxShadow: '0 2px 6px rgba(0,123,255,0.4)',
  },
  hiddenFileInput: {
    display: 'none',
  },
  uploadButton: {
    padding: '10px 25px',
    backgroundColor: '#28a745',
    border: 'none',
    color: 'white',
    borderRadius: 6,
    cursor: 'pointer',
    fontWeight: '600',
    boxShadow: '0 2px 6px rgba(40,167,69,0.4)',
    transition: 'background-color 0.3s ease',
  },
  errorText: {
    color: '#dc3545',
    fontWeight: '600',
    textAlign: 'center',
  },
  resultSection: {
    marginTop: 20,
    padding: 20,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  },
  resultTitle: {
    marginBottom: 10,
    color: '#555',
    fontWeight: '600',
  },
  jsonOutput: {
    maxHeight: 350,
    overflowY: 'auto',
    backgroundColor: '#272822',
    color: '#f8f8f2',
    padding: 15,
    borderRadius: 8,
    fontFamily: 'Consolas, monospace',
    fontSize: 14,
  },
  downloadButton: {
    marginTop: 15,
    padding: '10px 20px',
    backgroundColor: '#0069d9',
    border: 'none',
    color: 'white',
    borderRadius: 6,
    cursor: 'pointer',
    fontWeight: '600',
    boxShadow: '0 2px 6px rgba(0,105,217,0.5)',
  },
};
