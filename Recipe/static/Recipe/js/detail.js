document.addEventListener("DOMContentLoaded", function () {
    const personsInput = document.getElementById("personsInput");
    const ingredientsList = document.getElementById("ingredientsList");

    if (!personsInput) return;

    const url = personsInput.dataset.url; // <-- correct

    personsInput.addEventListener("input", function () {
        fetch(`${url}?persons=${this.value}`)
            .then(response => response.json())
            .then(data => {
                ingredientsList.innerHTML = "";

                data.ingredients.forEach(ing => {
                    const li = document.createElement("li");
                    li.innerHTML = `
                        ${ing.name} :
                        <span class="qty">${ing.quantity}</span>
                        ${ing.unit}
                    `;
                    ingredientsList.appendChild(li);
                });
            });
    });
});
