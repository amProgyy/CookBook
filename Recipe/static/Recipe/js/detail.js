document.addEventListener("DOMContentLoaded", function () {

    const personsInput = document.getElementById("personsInput");
    const ingredients = document.querySelectorAll(".ingredient");

    const baseServings = parseFloat(personsInput.dataset.base);

    let isUpdating = false;

    // 🔹 SERVINGS → INGREDIENTS
    personsInput.addEventListener("input", function () {
        if (isUpdating) return;
        isUpdating = true;

        const newServings = parseFloat(this.value);
        if (!newServings || newServings <= 0) {
            isUpdating = false;
            return;
        }

        const scale = newServings / baseServings;

        ingredients.forEach(item => {
            const baseQty = parseFloat(item.dataset.base);
            const input = item.querySelector(".ingredient-input");

            const newQty = (baseQty * scale).toFixed(2);
            input.value = newQty;
        });

        isUpdating = false;
    });

    // 🔹 INGREDIENT → SERVINGS
    ingredients.forEach(item => {
        const input = item.querySelector(".ingredient-input");
        const baseQty = parseFloat(item.dataset.base);

        input.addEventListener("input", function () {
            if (isUpdating) return;
            isUpdating = true;

            const newQty = parseFloat(this.value);
            if (!newQty || newQty <= 0 || baseQty === 0) {
                isUpdating = false;
                return;
            }

            const scale = newQty / baseQty;
            const newServings = (baseServings * scale).toFixed(2);

            personsInput.value = newServings;

            // Update all other ingredients
            ingredients.forEach(other => {
                if (other === item) return;

                const otherBase = parseFloat(other.dataset.base);
                const otherInput = other.querySelector(".ingredient-input");

                otherInput.value = (otherBase * scale).toFixed(2);
            });

            isUpdating = false;
        });
    });

});
