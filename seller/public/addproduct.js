const imagePlaceholders = document.querySelectorAll(".form-body-images img");
const productImages = document.querySelectorAll(".form-body-images .product-images");

for (let index = 0; index < imagePlaceholders.length; index++) {
    imagePlaceholders[index].addEventListener("click", () => {
        productImages[index].click();
        
    });
}

for (let index = 0; index < productImages.length; index++) {
    const element = productImages[index];
    const placeholder = imagePlaceholders[index];
    element.addEventListener("change", () => {
        console.log(element)

        const file = element.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                placeholder.src = reader.result;
                console.log(file.path); // This will log the file path to the console
            };
            reader.readAsDataURL(file);
        }
    });
}
