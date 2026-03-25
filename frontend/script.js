// Global variables to track data
let extractedData = [];
let totalFilesProcessed = 0;
let successfulExtractions = 0;
let aiProcessed = 0;
let apiStatus = { gemini: false, backend: false };

// DOM elements
const fileInput = document.getElementById('files');
const fileCount = document.getElementById('file-count');
const extractBtn = document.getElementById('extract-btn');
const progressSection = document.getElementById('progress-section');
const progressFill = document.getElementById('progress-fill');
const progressText = document.getElementById('progress-text');
const resultTable = document.getElementById('result-table');
const resultTbody = document.getElementById('result-tbody');
const noDataRow = document.getElementById('no-data-row');
const statsSection = document.getElementById('stats-section');
const exportBtn = document.getElementById('export-btn');
const clearBtn = document.getElementById('clear-btn');
const aiStatus = document.getElementById('ai-status');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');

// File input change handler
fileInput.addEventListener('change', function() {
    const files = this.files;
    updateFileCount(files.length);
    extractBtn.disabled = files.length === 0;
});

function updateFileCount(count) {
    if (count === 0) {
        fileCount.textContent = 'No files selected';
        fileCount.className = 'file-count';
    } else {
        fileCount.textContent = `${count} file${count > 1 ? 's' : ''} selected`;
        fileCount.className = 'file-count selected';
    }
}

function updateAIStatus(status) {
    apiStatus = { ...apiStatus, ...status };
    
    if (apiStatus.backend && apiStatus.gemini) {
        statusIndicator.textContent = '✅';
        statusText.textContent = 'AI Ready - Gemini Configured';
        aiStatus.className = 'ai-status ready';
        extractBtn.innerHTML = '<span class="btn-icon">🤖</span>Extract with AI';
    } else if (apiStatus.backend) {
        statusIndicator.textContent = '⚠️';
        statusText.textContent = 'Traditional Mode - Configure Gemini API';
        aiStatus.className = 'ai-status warning';
        extractBtn.innerHTML = '<span class="btn-icon">🔍</span>Extract (Traditional)';
    } else {
        statusIndicator.textContent = '❌';
        statusText.textContent = 'Backend Offline';
        aiStatus.className = 'ai-status error';
        extractBtn.disabled = true;
    }
}

function showProgress() {
    progressSection.style.display = 'block';
    progressFill.style.width = '0%';
    progressText.textContent = 'Uploading files...';
}

function updateProgress(percent, text) {
    progressFill.style.width = `${percent}%`;
    progressText.textContent = text;
}

function hideProgress() {
    setTimeout(() => {
        progressSection.style.display = 'none';
    }, 1000);
}

async function upload() {
    const files = fileInput.files;
    
    if (!files || files.length === 0) {
        alert('Please select at least one file');
        return;
    }

    // Reset counters
    totalFilesProcessed = 0;
    successfulExtractions = 0;
    aiProcessed = 0;

    // Disable upload button and show progress
    extractBtn.disabled = true;
    showProgress();

    try {
        const formData = new FormData();
        
        // Add all files to form data
        for (let file of files) {
            formData.append("files", file);
        }

        updateProgress(25, 'Uploading files...');

        // Send request to backend
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });

        updateProgress(75, apiStatus.gemini ? 'Processing with AI...' : 'Processing...');

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        updateProgress(100, 'Complete!');

        // DEBUG: Log the full response
        console.log('API Response:', result);
        console.log('Data array:', result.data);
        console.log('Stats:', result.stats);
        console.log('Results:', result.results);

        // Process results
        totalFilesProcessed = files.length;
        
        if (result.data && Array.isArray(result.data)) {
            console.log('Processing', result.data.length, 'data items');
            processResults(result.data, result.stats, result.results);
            
            // Update AI status based on response
            updateAIStatus({ 
                gemini: result.gemini_status === 'available',
                backend: true 
            });
        } else {
            throw new Error('Invalid response format');
        }

    } catch (error) {
        console.error('Error:', error);
        updateProgress(0, 'Error occurred');
        alert(`Error processing files: ${error.message}. Make sure the backend server is running.`);
        updateAIStatus({ backend: false });
    } finally {
        extractBtn.disabled = false;
        hideProgress();
    }
}

function processResults(data, stats, detailedResults) {
    // DEBUG: Log processing details
    console.log('processResults called with:');
    console.log('- data:', data);
    console.log('- stats:', stats); 
    console.log('- detailedResults:', detailedResults);
    
    // Clear existing data if this is a new upload
    if (extractedData.length === 0) {
        clearTable();
    }

    // Add new data to existing data
    extractedData = [...extractedData, ...data];
    successfulExtractions = extractedData.length;

    // Update stats from server response
    if (stats) {
        aiProcessed = stats.ai_processed || 0;
        totalFilesProcessed = stats.total_files || totalFilesProcessed;
    }

    // Display results with source file information
    displayResultsWithSource(data, detailedResults);
    updateStats();
    showControls();
}

function displayResultsWithSource(data, detailedResults) {
    // Always query live DOM — the global noDataRow ref becomes stale after clearTable()
    document.getElementById('no-data-row')?.remove();

    const addRow = (invoice, source, index) => {
        const row = resultTbody.insertRow();
        row.className = 'data-row';

        setTimeout(() => {
            row.classList.add('fade-in');
        }, index * 100);

        const customerCell = row.insertCell(0);
        const dateCell = row.insertCell(1);
        const itemCell = row.insertCell(2);
        const amountCell = row.insertCell(3);
        const confidenceCell = row.insertCell(4);
        const sourceCell = row.insertCell(5);

        customerCell.textContent = invoice.customer || 'N/A';
        dateCell.textContent = invoice.date || 'N/A';
        itemCell.textContent = invoice.item || 'N/A';
        amountCell.textContent = invoice.amount !== null && invoice.amount !== undefined && invoice.amount !== ''
            ? invoice.amount
            : 'N/A';

        const confidence = invoice.confidence || 'Low';
        confidenceCell.textContent = confidence;
        confidenceCell.className = `confidence confidence-${confidence.toLowerCase()}`;

        sourceCell.textContent = source;
        sourceCell.className = 'source-file';

        [customerCell, dateCell, itemCell, amountCell].forEach(cell => {
            if (cell.textContent === 'N/A') {
                cell.classList.add('empty-cell');
            }
        });
    };

    if (Array.isArray(detailedResults) && detailedResults.length > 0) {
        let index = 0;
        detailedResults.forEach(fileResult => {
            if (fileResult.status === 'success' && fileResult.data) {
                addRow(fileResult.data, fileResult.filename || 'Unknown', index);
                index++;
            }
        });
        return;
    }

    if (Array.isArray(data) && data.length > 0) {
        data.forEach((invoice, index) => {
            addRow(invoice, 'File ' + (index + 1), index);
        });
    }
}

function updateStats() {
    document.getElementById('total-files').textContent = totalFilesProcessed;
    document.getElementById('total-records').textContent = extractedData.length;
    document.getElementById('ai-processed').textContent = aiProcessed;
    
    const successRate = totalFilesProcessed > 0 
        ? Math.round((successfulExtractions / totalFilesProcessed) * 100)
        : 0;
    document.getElementById('success-rate').textContent = `${successRate}%`;
    
    statsSection.style.display = 'flex';
}

function showControls() {
    exportBtn.style.display = 'inline-block';
    clearBtn.style.display = 'inline-block';
}

function clearResults() {
    if (extractedData.length === 0) return;
    
    if (confirm('Are you sure you want to clear all results?')) {
        extractedData = [];
        totalFilesProcessed = 0;
        successfulExtractions = 0;
        aiProcessed = 0;
        
        clearTable();
        
        // Hide controls and stats
        exportBtn.style.display = 'none';
        clearBtn.style.display = 'none';
        statsSection.style.display = 'none';
        
        // Reset file input
        fileInput.value = '';
        updateFileCount(0);
        extractBtn.disabled = true;
    }
}

function clearTable() {
    // Remove all existing data rows
    const dataRows = resultTbody.querySelectorAll('.data-row');
    dataRows.forEach(row => row.remove());

    // Remove existing no-data row before re-adding (prevents duplicates)
    document.getElementById('no-data-row')?.remove();

    // Add "no data" row back
    const noDataRow = resultTbody.insertRow();
    noDataRow.id = 'no-data-row';
    const noDataCell = noDataRow.insertCell(0);
    noDataCell.colSpan = 6;
    noDataCell.className = 'no-data';
    noDataCell.textContent = 'No data extracted yet. Upload files to get started with AI extraction.';
}

function exportData() {
    if (extractedData.length === 0) {
        alert('No data to export');
        return;
    }

    // Create CSV content with enhanced fields
    const headers = ['Customer', 'Date', 'Item/Service', 'Amount', 'Confidence', 'Currency', 'Invoice Number'];
    const csvContent = [
        headers.join(','),
        ...extractedData.map(row => [
            `"${(row.customer || '').replace(/"/g, '""')}"`,
            `"${(row.date || '').replace(/"/g, '""')}"`,
            `"${(row.item || '').replace(/"/g, '""')}"`,
            `"${(row.amount || '').replace(/"/g, '""')}"`,
            `"${(row.confidence || '').replace(/"/g, '""')}"`,
            `"${(row.currency || '').replace(/"/g, '""')}"`,
            `"${(row.invoice_number || '').replace(/"/g, '""')}"`
        ].join(','))
    ].join('\n');

    // Create and download file
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ai_invoice_data_${new Date().toISOString().slice(0, 19).replace(/[:.]/g, '-')}.csv`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Enhanced drag and drop functionality
const container = document.querySelector('.container');

container.addEventListener('dragover', function(e) {
    e.preventDefault();
    this.classList.add('drag-over');
});

container.addEventListener('dragleave', function(e) {
    e.preventDefault();
    this.classList.remove('drag-over');
});

container.addEventListener('drop', function(e) {
    e.preventDefault();
    this.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        fileInput.files = files;
        updateFileCount(files.length);
        extractBtn.disabled = false;
    }
});

// Check backend and AI status on load
async function checkSystemStatus() {
    try {
        // Check main API endpoint
        const response = await fetch('http://127.0.0.1:8000/');
        const data = await response.json();
        
        updateAIStatus({
            backend: true,
            gemini: data.features?.ai_parsing || false
        });
        
        console.log('System status:', data);
    } catch (error) {
        console.warn('Backend connection failed:', error);
        updateAIStatus({ backend: false, gemini: false });
        console.log('Make sure to start the backend with: uvicorn app:app --reload');
    }
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    console.log('AI Invoice Parser Frontend Loaded');
    checkSystemStatus();
});