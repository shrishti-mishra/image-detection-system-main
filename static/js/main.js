// Main JavaScript for Satellite Detection System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Image upload preview
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const previewContainer = document.getElementById('preview-container');
                    const imagePreview = document.getElementById('image-preview');
                    
                    if (previewContainer && imagePreview) {
                        imagePreview.src = e.target.result;
                        previewContainer.classList.remove('d-none');
                    }
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Form submission handling
    const uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function() {
            const loading = document.getElementById('loading');
            const uploadBtn = document.getElementById('upload-btn');
            
            if (loading && uploadBtn) {
                loading.classList.remove('d-none');
                uploadBtn.disabled = true;
                uploadBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
            }
        });
    }

    // Tab navigation handling
    const resultTabs = document.getElementById('resultTabs');
    if (resultTabs) {
        const tabs = resultTabs.querySelectorAll('button[data-bs-toggle="tab"]');
        tabs.forEach(tab => {
            tab.addEventListener('shown.bs.tab', function (event) {
                // If map tab is shown, trigger resize to fix Google Maps display issues
                if (event.target.id === 'location-tab') {
                    if (window.google && window.google.maps) {
                        const map = document.getElementById('map');
                        if (map) {
                            google.maps.event.trigger(map, 'resize');
                        }
                    }
                }
                
                // Handle visualization tab
                if (event.target.id === 'visualization-tab') {
                    const vizOptions = document.querySelectorAll('.viz-option');
                    if (vizOptions.length > 0) {
                        vizOptions.forEach(option => {
                            option.addEventListener('click', function() {
                                const vizType = this.dataset.viz;
                                document.querySelectorAll('.viz-image').forEach(img => {
                                    img.classList.add('d-none');
                                });
                                document.getElementById(`${vizType}Image`).classList.remove('d-none');
                                
                                // Update active state
                                vizOptions.forEach(opt => opt.classList.remove('active'));
                                this.classList.add('active');
                            });
                        });
                    }
                }
            });
        });
    }

    // Object highlighting on hover (for results page)
    const objectItems = document.querySelectorAll('.object-item');
    if (objectItems.length > 0) {
        objectItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                const objectId = this.dataset.objectId;
                const objectBox = document.querySelector(`.object-box[data-object-id="${objectId}"]`);
                if (objectBox) {
                    objectBox.classList.add('highlight-box');
                }
            });
            
            item.addEventListener('mouseleave', function() {
                const objectId = this.dataset.objectId;
                const objectBox = document.querySelector(`.object-box[data-object-id="${objectId}"]`);
                if (objectBox) {
                    objectBox.classList.remove('highlight-box');
                }
            });
        });
    }

    // API response handling for async requests
    const apiForm = document.getElementById('api-form');
    if (apiForm) {
        apiForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const resultContainer = document.getElementById('api-result');
            const loadingIndicator = document.getElementById('api-loading');
            
            if (resultContainer && loadingIndicator) {
                resultContainer.innerHTML = '';
                loadingIndicator.classList.remove('d-none');
                
                try {
                    const response = await fetch('/api/detect', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const data = await response.json();
                    loadingIndicator.classList.add('d-none');
                    
                    if (data.error) {
                        resultContainer.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                    } else {
                        // Display results
                        let resultsHtml = `
                            <div class="card">
                                <div class="card-header bg-primary text-white">
                                    <h5 class="mb-0">Detection Results</h5>
                                </div>
                                <div class="card-body">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <div class="image-container position-relative">
                                                <img src="data:image/jpeg;base64,${data.annotated_image}" class="img-fluid rounded" alt="Annotated image">
                                                <div class="mt-2">
                                                    <button class="btn btn-sm btn-outline-secondary viz-option active" data-viz="annotated">Annotated</button>
                                                    <button class="btn btn-sm btn-outline-secondary viz-option" data-viz="heatmap">Heatmap</button>
                                                    <button class="btn btn-sm btn-outline-secondary viz-option" data-viz="original">Original</button>
                                                </div>
                                                <div class="mt-2">
                                                    <img id="annotatedImage" class="viz-image img-fluid rounded" src="data:image/jpeg;base64,${data.annotated_image}" alt="Annotated image">
                                                    <img id="heatmapImage" class="viz-image img-fluid rounded d-none" src="data:image/jpeg;base64,${data.heatmap || data.annotated_image}" alt="Heatmap">
                                                    <img id="originalImage" class="viz-image img-fluid rounded d-none" src="data:image/jpeg;base64,${data.original_image || data.annotated_image}" alt="Original image">
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <h5>Description</h5>
                                            <p>${data.description}</p>
                                            <h5>Location</h5>
                                            <p>${data.location.name}</p>
                                            <h5>Objects Detected</h5>
                                            <ul>
                        `;
                        
                        data.detected_objects.forEach(obj => {
                            resultsHtml += `<li>${obj.class_name} (${(obj.confidence * 100).toFixed(2)}%)</li>`;
                        });
                        
                        resultsHtml += `
                                            </ul>
                                            <h5>Tags</h5>
                                            <div class="tags-container">
                                                ${(data.tags || []).map(tag => `<span class="badge bg-secondary me-1">${tag}</span>`).join('')}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                        
                        resultContainer.innerHTML = resultsHtml;
                        
                        // Initialize visualization options
                        const vizOptions = resultContainer.querySelectorAll('.viz-option');
                        vizOptions.forEach(option => {
                            option.addEventListener('click', function() {
                                const vizType = this.dataset.viz;
                                resultContainer.querySelectorAll('.viz-image').forEach(img => {
                                    img.classList.add('d-none');
                                });
                                resultContainer.querySelector(`#${vizType}Image`).classList.remove('d-none');
                                
                                // Update active state
                                vizOptions.forEach(opt => opt.classList.remove('active'));
                                this.classList.add('active');
                            });
                        });
                    }
                } catch (error) {
                    loadingIndicator.classList.add('d-none');
                    resultContainer.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
                }
            }
        });
    }
});