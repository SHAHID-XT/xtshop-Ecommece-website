const mainImg = document.querySelector(".main-image img");

const removeActive = () => {
  document.querySelectorAll(".other-images img").forEach((el) => {
    el.classList.remove("activeimage");
  });
};
document.querySelectorAll(".other-images img").forEach((el) => {
  el.addEventListener("mouseover", () => {
    removeActive();
    mainImg.src = el.src;
    el.classList.add("activeimage");
  });
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
    } if (data["error"]) {
      showNotification(data["error"]);
    }


    return data; // Return any data received from the server
  } catch (error) {
    showNotification("Failed to add to cart");
    console.log(error);
  }
}
try{

    const pcartbtn = document.querySelector(".cart-btnn");
    pcartbtn.addEventListener("click", () => {
      let itemid = pcartbtn.getAttribute("data-item");
      addToCart(pcartbtn, itemid);
    });
}catch{}

