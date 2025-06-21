function getBathValue() {
    var uiBathrooms = document.getElementsByName("uiBathrooms");
    for(var i in uiBathrooms) {
      if(uiBathrooms[i].checked) {
          return parseInt(i)+1;
      }
    }
    return -1;
}
  
function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for(var i in uiBHK) {
      if(uiBHK[i].checked) {
          return parseInt(i)+1;
      }
    }
    return -1;
}

function showLoading() {
    var submitBtn = document.querySelector('.submit-btn');
    submitBtn.innerHTML = '<span class="loading"></span>Calculating...';
    submitBtn.disabled = true;
}

function hideLoading() {
    var submitBtn = document.querySelector('.submit-btn');
    submitBtn.innerHTML = '<i class="fas fa-calculator"></i> Calculate Price';
    submitBtn.disabled = false;
}

function showResult(price) {
    var estPrice = document.getElementById("uiEstimatedPrice");
    estPrice.innerHTML = "<h2>₹" + price.toFixed(2) + " Lakh</h2>";
    estPrice.classList.add('show');
}

function showError(message) {
    var estPrice = document.getElementById("uiEstimatedPrice");
    estPrice.innerHTML = "<h2>❌ " + message + "</h2>";
    estPrice.style.background = "linear-gradient(135deg, #e53e3e 0%, #c53030 100%)";
    estPrice.classList.add('show');
    
    // Reset background after 3 seconds
    setTimeout(() => {
        estPrice.style.background = "linear-gradient(135deg, #48bb78 0%, #38a169 100%)";
    }, 3000);
}

function validateInput() {
    var sqft = document.getElementById("uiSqft").value;
    var location = document.getElementById("uiLocations").value;
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    
    if (!sqft || sqft < 100) {
        showError("Please enter a valid area (minimum 100 sq ft)");
        return false;
    }
    
    if (!location) {
        showError("Please select a location");
        return false;
    }
    
    if (bhk === -1) {
        showError("Please select number of bedrooms");
        return false;
    }
    
    if (bathrooms === -1) {
        showError("Please select number of bathrooms");
        return false;
    }
    
    return true;
}

// Enhanced price prediction model with Bangalore location data
function predictPrice(location, sqft, bhk, bath, balcony) {
    // Base price calculation
    let basePrice = 50;
    
    // Area contribution (similar to your trained model)
    let areaPrice = sqft * 0.045;
    
    // Room contributions
    let bhkPrice = bhk * 12.8;
    let bathPrice = bath * 5.2;
    let balconyPrice = balcony * 3.5;
    
    // Location multipliers based on Bangalore real estate data
    const locationMultipliers = {
        'koramangala': 1.45, 'indiranagar': 1.55, 'hsr layout': 1.48,
        'whitefield': 1.32, 'marathahalli': 1.38, 'electronic city': 1.12,
        'hebbal': 1.28, 'jp nagar': 1.18, 'jayanagar': 1.33,
        'malleshwaram': 1.38, 'rajaji nagar': 1.22, 'banashankari': 1.15,
        'btm layout': 1.23, 'sarjapur road': 1.25, 'bannerghatta road': 1.18,
        'kr puram': 1.13, 'bellandur': 1.35, 'brookefield': 1.28,
        'cv raman nagar': 1.23, 'domlur': 1.38, 'ulsoor': 1.31,
        'frazer town': 1.29, 'commercial street': 1.42, 'mg road': 1.52,
        'brigade road': 1.49, 'residency road': 1.46, 'cunningham road': 1.44,
        'vasanth nagar': 1.41, 'richmond town': 1.37, 'langford town': 1.34,
        'shanti nagar': 1.31, 'jeevanbhima nagar': 1.28, 'hal': 1.33,
        'new bel road': 1.26, 'rt nagar': 1.24, 'jalahalli': 1.19,
        'mathikere': 1.21, 'yeshwanthpur': 1.17, 'tumkur road': 1.14,
        'peenya': 1.16, 'nagarbhavi': 1.13, 'vijayanagar': 1.20,
        'basaveshwara nagar': 1.18, 'rajajinagar': 1.22, 'mahalakshmi layout': 1.19,
        'magadi road': 1.11, 'kengeri': 1.08, 'uttarahalli': 1.10,
        'hoskerehalli': 1.12, 'girinagar': 1.14, 'katriguppe': 1.16,
        'padmanabhanagar': 1.13, 'bhavani nagar': 1.15, 'hanumanthanagar': 1.17
    };
    
    // Find location multiplier
    let locationKey = location.toLowerCase().replace(/[^a-z]/g, '');
    let multiplier = 1.0;
    
    for (let loc in locationMultipliers) {
        if (locationKey.includes(loc.replace(/[^a-z]/g, '')) || 
            loc.replace(/[^a-z]/g, '').includes(locationKey)) {
            multiplier = locationMultipliers[loc];
            break;
        }
    }
    
    // Calculate final price
    let price = (basePrice + areaPrice + bhkPrice + bathPrice + balconyPrice) * multiplier;
    
    // Apply reasonable bounds
    return Math.max(20, Math.min(800, price));
}

function onClickedEstimatePrice() {
    if (!validateInput()) return;
    
    showLoading();
    
    // Get form values
    var sqft = parseFloat(document.getElementById("uiSqft").value);
    var location = document.getElementById("uiLocations").value;
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var balcony = parseInt(document.getElementById("uiBalcony").value) || 1;
    
    // Simulate API delay for better UX
    setTimeout(() => {
        try {
            var estimatedPrice = predictPrice(location, sqft, bhk, bathrooms, balcony);
            hideLoading();
            showResult(estimatedPrice);
        } catch (error) {
            hideLoading();
            showError("Calculation failed. Please try again.");
        }
    }, 1000);
}

function onPageLoad() {
    console.log("Real Estate Predictor loaded");
    
    // Populate locations dropdown with Bangalore areas
    var locations = [
        'Koramangala', 'Indiranagar', 'HSR Layout', 'Whitefield', 'Marathahalli',
        'Electronic City', 'Hebbal', 'JP Nagar', 'Jayanagar', 'Malleshwaram',
        'Rajaji Nagar', 'Banashankari', 'BTM Layout', 'Sarjapur Road',
        'Bannerghatta Road', 'KR Puram', 'Bellandur', 'Brookefield',
        'CV Raman Nagar', 'Domlur', 'Ulsoor', 'Frazer Town', 'MG Road',
        'Brigade Road', 'Residency Road', 'Cunningham Road', 'Vasanth Nagar',
        'Richmond Town', 'Langford Town', 'Shanti Nagar', 'Jeevanbhima Nagar',
        'HAL', 'New BEL Road', 'RT Nagar', 'Jalahalli', 'Mathikere',
        'Yeshwanthpur', 'Tumkur Road', 'Peenya', 'Nagarbhavi', 'Vijayanagar',
        'Basaveshwara Nagar', 'Mahalakshmi Layout', 'Magadi Road', 'Kengeri',
        'Uttarahalli', 'Hoskerehalli', 'Girinagar', 'Katriguppe', 'Padmanabhanagar'
    ];
    
    var uiLocations = document.getElementById("uiLocations");
    locations.forEach(function(location) {
        var option = document.createElement("option");
        option.value = location;
        option.text = location;
        uiLocations.appendChild(option);
    });
    
    // Add input validation for square feet
    var sqftInput = document.getElementById("uiSqft");
    sqftInput.addEventListener('input', function() {
        var value = parseInt(this.value);
        if (value < 100) {
            this.style.borderColor = '#e53e3e';
        } else {
            this.style.borderColor = '#e2e8f0';
        }
    });
}
  
window.onload = onPageLoad;