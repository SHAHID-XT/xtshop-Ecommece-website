document.querySelectorAll(".cart-delete-icon.delete").forEach((el) => {
  el.addEventListener("click", () => {
    const cartid = el.getAttribute("data-cartid");
    deleteFromCart(cartid);
  });
});


document.querySelectorAll(".cart-left .add").forEach((el)=>{
    el.addEventListener("click",()=>{
        const cartid = el.getAttribute("data-cartid")
        AddQuantitlyFromCart(cartid)
    })
})



document.querySelectorAll(".cart-left .remove").forEach((el)=>{
    el.addEventListener("click",()=>{
        const cartid = el.getAttribute("data-cartid")
        removeQuantitlyFromCart(cartid)
    })
})

