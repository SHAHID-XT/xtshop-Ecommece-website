const priceRange = document.querySelector("#pricerange");
priceRange.addEventListener("input", () => {
  document.querySelector("#max-f-price").textContent =
    "₹ " + document.querySelector("#pricerange").value;
});

priceRange.addEventListener("change", () => {
  updateURLParams({ maxprice: document.querySelector("#pricerange").value });
});

function showNotification(ntext, timeout = 2000) {
  try {
    const notification = document.getElementById("notification");
    notification.style.display = "block";
    notification.textContent = ntext;
    notification.classList.add("hidenotification");
    setTimeout(() => {
      notification.classList.remove("hidenotification");
    }, timeout);
  } catch (e) {
    console.log(e);
  }
}

function getQueryParams() {
  var queryParams = {};
  var queryString = window.location.search.substring(1);
  var params = queryString.split("&");
  for (var i = 0; i < params.length; i++) {
    var pair = params[i].split("=");
    if (pair[0]) {
      // Check if the key is not empty
      queryParams[pair[0]] = decodeURIComponent(pair[1] || "");
    }
  }
  return queryParams;
}

function updateURLParams(newParams) {
  var queryParams = getQueryParams();
  var hasUpdated = false; // Flag to track if any parameter was updated

  // Iterate over the new parameters
  for (var key in newParams) {
    if (queryParams.hasOwnProperty(key)) {
      // If the parameter already exists with a different value
      if (queryParams[key] !== newParams[key]) {
        queryParams[key] = newParams[key]; // Update the value
        hasUpdated = true; // Set flag to true
      }
      // If the parameter already exists with the same value, remove it
      else {
        delete queryParams[key];
        hasUpdated = true; // Set flag to true
      }
    }
    // If the parameter does not exist, add it
    else {
      queryParams[key] = newParams[key];
      hasUpdated = true; // Set flag to true
    }
  }

  // Only update the URL if any parameter was updated
  if (hasUpdated) {
    var queryString = Object.keys(queryParams)
      .map((key) => key + "=" + encodeURIComponent(queryParams[key]))
      .join("&");
    var newURL = window.location.pathname + "?" + queryString;
    history.pushState({}, "", newURL);
    window.location.reload();
  }
}

document.querySelectorAll(".sort-by a").forEach((el) => {
  el.addEventListener("click", function () {
    updateURLParams({ sort: el.textContent.toString() });
    // window.location.reload();
  });
});

async function addToCart(btnelement, productid) {
  try {
    const response = await fetch(`/add-to-cart/${productid}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      showNotification("Failed to add to cart");
      console.log(response);
      return;
    }

    const data = await response.json();
    if (data["status"]) {
      showNotification("Successfully added to cart...");
      btnelement.innerHTML = "Added to cart...";
    } else {
      showNotification("Failed to add to cart");
    }
    if (data["error"]){
      console.log(data)
      showNotification(data["error"]);
    }


    return data; // Return any data received from the server
  } catch (error) {
    showNotification("Failed to add to cart");
    console.log(error);
  }
}

document.querySelectorAll(".product-cart-btn").forEach((el) => {
  el.addEventListener("click", (e) => {
    let itemid = el.getAttribute("data-item");
    addToCart(el, itemid);
  });
});

document.querySelectorAll(".ftr-category-item.event").forEach((el) => {
  el.addEventListener("click", () => {
    let href = el.getAttribute("data-href");
    let values = el.getAttribute("data-value");
    let params = {};
    params[values] = href;
    updateURLParams(params);
  });
});
