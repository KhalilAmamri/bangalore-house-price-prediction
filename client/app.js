// API Base URL
const API_URL = 'https://bangalore-house-price-predictor-hr8e.onrender.com';

// DOM Elements
const form = document.getElementById('priceForm');
const locationSelect = document.getElementById('location');
const sqftInput = document.getElementById('sqft');
const bhkSelect = document.getElementById('bhk');
const bathSelect = document.getElementById('bath');
const predictBtn = document.getElementById('predictBtn');
const btnText = document.getElementById('btnText');
const btnLoader = document.getElementById('btnLoader');
const resultCard = document.getElementById('result');
const errorCard = document.getElementById('error');
const priceValue = document.getElementById('priceValue');
const resultLocation = document.getElementById('resultLocation');
const resultSqft = document.getElementById('resultSqft');
const resultConfig = document.getElementById('resultConfig');
const errorMessage = document.getElementById('errorMessage');

// Load locations on page load
document.addEventListener('DOMContentLoaded', () => {
    loadLocations();
});

// Fetch locations from API
async function loadLocations() {
    try {
        const response = await fetch(`${API_URL}/get_location_names`);
        const data = await response.json();
        
        if (data.locations && data.locations.length > 0) {
            data.locations.forEach(location => {
                const option = document.createElement('option');
                option.value = location;
                option.textContent = location;
                locationSelect.appendChild(option);
            });
        } else {
            showError('No locations available. Please check if the server is running.');
        }
    } catch (error) {
        console.error('Error loading locations:', error);
        showError('Failed to load locations. Please check if the server is running on port 5000.');
    }
}

// Handle form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Hide previous results/errors
    hideResult();
    hideError();
    
    // Show loading state
    setLoading(true);
    
    // Get form data
    const formData = new FormData();
    formData.append('location', locationSelect.value);
    formData.append('sqft', sqftInput.value);
    formData.append('bhk', bhkSelect.value);
    formData.append('bath', bathSelect.value);
    
    try {
        const response = await fetch(`${API_URL}/predict_price`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Failed to get prediction');
        }
        
        const data = await response.json();
        
        if (data.estimated_price) {
            showResult(data.estimated_price);
        } else {
            throw new Error('Invalid response from server');
        }
    } catch (error) {
        console.error('Error predicting price:', error);
        showError('Failed to predict price. Please try again.');
    } finally {
        setLoading(false);
    }
});

// Show result
function showResult(price) {
    priceValue.textContent = price.toFixed(2);
    resultLocation.textContent = locationSelect.options[locationSelect.selectedIndex].text;
    resultSqft.textContent = `${sqftInput.value} sq ft`;
    resultConfig.textContent = `${bhkSelect.value} BHK, ${bathSelect.value} Bath`;
    
    resultCard.style.display = 'block';
    
    // Scroll to result
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Hide result
function hideResult() {
    resultCard.style.display = 'none';
}

// Show error
function showError(message) {
    errorMessage.textContent = message;
    errorCard.style.display = 'block';
    
    // Auto-hide error after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

// Hide error
function hideError() {
    errorCard.style.display = 'none';
}

// Set loading state
function setLoading(loading) {
    if (loading) {
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';
        predictBtn.disabled = true;
    } else {
        btnText.style.display = 'block';
        btnLoader.style.display = 'none';
        predictBtn.disabled = false;
    }
}

// Input validation
sqftInput.addEventListener('input', () => {
    if (sqftInput.value < 300) {
        sqftInput.setCustomValidity('Area must be at least 300 sq ft');
    } else {
        sqftInput.setCustomValidity('');
    }
});
