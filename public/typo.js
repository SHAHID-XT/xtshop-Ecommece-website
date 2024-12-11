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

function updateURLParams(newParams, reload = true) {
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
    if (reload) {
      window.location.reload();
    }
  }
}

try {
  const rotateElements = document.querySelectorAll(".has_child");
  rotateElements.forEach((el) => {
    el.addEventListener("click", () => {
      el.classList.toggle("rotateicon");
      const ell = el.parentElement.querySelector(".widget_childs");
      ell.classList.toggle("open_child");
    });
  });
} catch (e) {
  console.log(e);
}
try {
  const leftMenu = document.querySelector("#left-hide-show");
  const leftmenuspan = leftMenu.querySelector("span");

  leftMenu.addEventListener("click", (e) => {
    console.log(e.target);
    document.querySelector(".left-bar-ul").classList.toggle("doshow");
    document.querySelector(".left-bar").style.flex = "none";
    document.querySelector(".left-bar").classList.toggle("hidenleft");
    const iconbox = leftMenu.querySelector(".material-symbols-outlined");
    if (iconbox.textContent == "close") {
      iconbox.textContent = "menu_open";
    } else {
      iconbox.textContent = "close";
    }
  });
} catch (e) {
  console.log(e);
}
try {
  const profilembtoggle = document.querySelector(".flex-top");
  profilembtoggle.addEventListener("click", () => {
    profilembtoggle.parentElement.classList.toggle("showmbhide");
  });
} catch (e) {
  console.log(e);
}

if (
  window.innerWidth >= 1127 &&
  !window.location.href.includes("/view-orders/")
) {
  document.querySelector("#left-hide-show").click();
}

try {
  pass;
} catch {}

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

async function removeQuantitlyFromCart(
  cart_item_id,
  updateCartValueEl = false
) {
  try {
    const response = await fetch(`/remove-from-cart-qty/${cart_item_id}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      showNotification("Failed to remove item from cart.");
      console.log(response);
      return;
    }

    const data = await response.json();
    if (data["status"]) {
      window.location.reload();
      if (updateCartValueEl) {
        btnelement.innerText = data["quantity"];
      }
    } else {
      showNotification("Failed to remove item from cart.");
    }

    return data; // Return any data received from the server
  } catch (error) {
    showNotification("Failed to add to cart");
    console.log(error);
  }
}

async function deleteFromCart(cart_item_id, removeEl = false) {
  try {
    const response = await fetch(`/delete-from-cart/${cart_item_id}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      showNotification("Failed to remove item from cart.");
      console.log(response);
      return;
    }

    const data = await response.json();
    if (data["status"]) {
      window.location.reload();
    } else {
      showNotification("Failed to remove item from cart.");
    }

    return data; // Return any data received from the server
  } catch (error) {
    showNotification("Failed to add to cart");
    console.log(error);
  }
}

async function AddQuantitlyFromCart(cart_item_id, updateCartValueEl = false) {
  try {
    const response = await fetch(`/add-from-cart-qty/${cart_item_id}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      showNotification("Failed to remove item from cart.");
      console.log(response);
      return;
    }

    const data = await response.json();
    if (data["status"]) {
      window.location.reload();
      if (updateCartValueEl) {
        btnelement.innerText = data["quantity"];
      }
    } else {
      showNotification("Failed to remove item from cart.");
    }

    return data; // Return any data received from the server
  } catch (error) {
    showNotification("Failed to add to cart");
    console.log(error);
  }
}

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
      if (btnelement) {
        btnelement.innerHTML = "Added to cart...";
      }
    } else {
      showNotification("Failed to add to cart");
    }
    if (data["error"]) {
      console.log(data);
      showNotification(data["error"]);
    }

    return data; // Return any data received from the server
  } catch (error) {
    showNotification("Failed to add to cart");
    console.log(error);
  }
}

try {
  var currentUrl = window.location.href;

  // Remove the message parameter from the URL
  var newUrl = currentUrl.replace(/[?&]message=([^&#]*)/g, "");

  // Replace the current URL with the modified URL
  window.history.replaceState({}, document.title, newUrl);
} catch (e) {}

try {
  document.querySelectorAll(".sale-filter span").forEach((el) => {
    const elementText = el.textContent;
    el.addEventListener("click", () => {
      updateURLParams({ by: elementText.toString() });
    });
  });
} catch {}

try {
  document.querySelectorAll(".myorder-header .label").forEach((el) => {
    const params_value = el.getAttribute("data-status");

    el.addEventListener("click", () => {
      updateURLParams({ status: params_value });
    });
  });
} catch {}

try {
  document.querySelector("#checkedall").addEventListener("click", (e) => {
    if (e.target.checked) {
      document.querySelectorAll("input[type='checkbox']").forEach((el) => {
        el.checked = true;
      });
    } else {
      document.querySelectorAll("input[type='checkbox']").forEach((el) => {
        el.checked = false;
      });
    }
  });
} catch (e) {
  console.log(e);
}

try {
  document.querySelector(".down-label-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const order_ids = [];
    document.querySelectorAll(".checkboxx").forEach((ell) => {
      if (ell.querySelector("input[type='checkbox'").checked) {
        order_ids.push(ell.getAttribute("data-order-id"));
      }
    });
    if (order_ids.length >= 1) {
      window.location.href = `/download-labels/?id=${JSON.stringify(
        (value = order_ids)
      )}`;
    } else {
    }
  });
} catch {}
