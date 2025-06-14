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
  
function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    
    // Hide previous results
    var estPrice = document.getElementById("uiEstimatedPrice");
    estPrice.classList.remove('show');
    
    // Validate input
    if (!validateInput()) {
        return;
    }
    
    var sqft = document.getElementById("uiSqft").value;
    var bhk = getBHKValue();
    var bathrooms = getBathValue();
    var location = document.getElementById("uiLocations").value;
    
    showLoading();
    
    var url = "/predict_home_price";
    
    $.post(url, {
        total_sqft: parseFloat(sqft),
        bhk: bhk,
        bath: bathrooms,
        location: location
    })
    .done(function(data) {
        console.log("Prediction successful:", data.estimated_price);
        hideLoading();
        showResult(data.estimated_price);
    })
    .fail(function(xhr, status, error) {
        console.error("Prediction failed:", error);
        hideLoading();
        showError("Unable to calculate price. Please try again.");
    });
}
  
function onPageLoad() {
    console.log("Document loaded");
    
    // Add loading state for location dropdown
    var locationSelect = document.getElementById("uiLocations");
    locationSelect.innerHTML = '<option value="" disabled selected>Loading locations...</option>';
    
    var url = "/get_location_names";
    $.get(url)
    .done(function(data) {
        console.log("Got response for get_location_names request");
        if(data && data.locations) {
            var locations = data.locations;
            locationSelect.innerHTML = '<option value="" disabled selected>Choose a location...</option>';
            
            // Sort locations alphabetically
            locations.sort();
            
            for(var i = 0; i < locations.length; i++) {
                var opt = new Option(locations[i], locations[i]);
                locationSelect.appendChild(opt);
            }
        } else {
            locationSelect.innerHTML = '<option value="" disabled selected>No locations available</option>';
        }
    })
    .fail(function() {
        console.error("Failed to load locations");
        locationSelect.innerHTML = '<option value="" disabled selected>Failed to load locations</option>';
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
    
    // Add smooth scrolling to result when it appears
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                var target = mutation.target;
                if (target.classList.contains('show')) {
                    setTimeout(() => {
                        target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }, 100);
                }
            }
        });
    });
    
    observer.observe(document.getElementById("uiEstimatedPrice"), {
        attributes: true,
        attributeFilter: ['class']
    });
}
  
window.onload = onPageLoad;