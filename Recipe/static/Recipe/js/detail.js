document.addEventListener("DOMContentLoaded", function () {
    const personsInput = document.getElementById("personsInput");
    const resetScaleBtn = document.getElementById("resetScaleBtn");
    const scaleInfo = document.getElementById("scaleInfo");
    const ingredients = document.querySelectorAll(".ingredient-display-item");

    if (!personsInput || ingredients.length === 0) return;

    const baseServings = parseFloat(personsInput.dataset.base);
    const snapToHalf = (qty) => Math.round(Number(qty) * 2) / 2;
    const formatIngredientQty = (qty) => {
        const snapped = snapToHalf(qty);
        return Number.isInteger(snapped) ? String(snapped) : snapped.toFixed(1);
    };
    const normalizeServings = (value) => {
        const servings = Math.round(parseFloat(value));
        return Number.isFinite(servings) && servings > 0 ? servings : null;
    };

    let isUpdating = false;

    const formatScaleFactor = (scale) => {
        const fixed = Number(scale).toFixed(2);
        return fixed.replace(/\.00$/, "").replace(/(\.\d)0$/, "$1");
    };

    const baseServingsInt = normalizeServings(baseServings) || 1;
    const updateScaleUI = () => {
        if (!resetScaleBtn) return;

        const currentServings = normalizeServings(personsInput.value) || baseServingsInt;
        const scaled = currentServings !== baseServingsInt;

        resetScaleBtn.style.display = scaled ? "" : "none";

        if (scaleInfo) {
            if (!scaled) {
                scaleInfo.textContent = "";
                scaleInfo.style.display = "none";
            } else {
                const factor = currentServings / baseServingsInt;
                scaleInfo.textContent = `Scaled x${formatScaleFactor(factor)} (${baseServingsInt}→${currentServings})`;
                scaleInfo.style.display = "inline";
            }
        }
    };

    const resetScale = () => {
        if (isUpdating) return;
        isUpdating = true;

        personsInput.value = baseServingsInt;

        ingredients.forEach(item => {
            const input = item.querySelector(".ingredient-input");
            const baseQty = parseFloat(item.dataset.base);
            if (input && !isNaN(baseQty)) {
                input.value = formatIngredientQty(baseQty);
            }
        });

        isUpdating = false;
        updateScaleUI();
    };

    personsInput.value = normalizeServings(personsInput.value) || 1;
    ingredients.forEach(item => {
        const input = item.querySelector(".ingredient-input");
        const baseQty = parseFloat(item.dataset.base);
        if (input && !isNaN(baseQty)) {
            input.value = formatIngredientQty(baseQty);
        }
    });

    if (resetScaleBtn) {
        resetScaleBtn.addEventListener("click", resetScale);
    }
    updateScaleUI();

    // Servings -> Ingredients
    personsInput.addEventListener("input", function () {
        if (isUpdating) return;
        isUpdating = true;

        const newServings = normalizeServings(this.value);
        if (newServings === null) {
            isUpdating = false;
            return;
        }
        this.value = newServings;

        const scale = newServings / baseServings;

        ingredients.forEach(item => {
            const baseQty = parseFloat(item.dataset.base);
            if (isNaN(baseQty)) return;

            const input = item.querySelector(".ingredient-input");
            if (input) {
                input.value = formatIngredientQty(baseQty * scale);
            }
        });

        isUpdating = false;
        updateScaleUI();
    });

    // Ingredient -> Servings
    ingredients.forEach(item => {
        const input = item.querySelector(".ingredient-input");
        if (!input) return;

        const baseQty = parseFloat(item.dataset.base);

        const minusBtn = item.querySelector(".minus-btn");
        const plusBtn = item.querySelector(".plus-btn");

        if (minusBtn) {
            minusBtn.addEventListener("click", () => {
                let currentVal = parseFloat(input.value) || 0;
                let step = parseFloat(input.step) || 0.5;
                let newVal = currentVal - step;
                if (newVal >= 0) {
                    input.value = newVal;
                    input.dispatchEvent(new Event('input'));
                }
            });
        }

        if (plusBtn) {
            plusBtn.addEventListener("click", () => {
                let currentVal = parseFloat(input.value) || 0;
                let step = parseFloat(input.step) || 0.5;
                input.value = currentVal + step;
                input.dispatchEvent(new Event('input'));
            });
        }

        input.addEventListener("input", function () {
            if (isUpdating) return;
            isUpdating = true;

            const newQty = snapToHalf(this.value);
            if (isNaN(newQty) || newQty <= 0 || isNaN(baseQty) || baseQty === 0) {
                isUpdating = false;
                return;
            }

            const scale = newQty / baseQty;
            let newServings = Math.round(baseServings * scale);
            if (newServings <= 0) newServings = 1;
            personsInput.value = newServings;

            const normalizedScale = newServings / baseServings;

            ingredients.forEach(other => {
                if (other === item) return;

                const otherBase = parseFloat(other.dataset.base);
                if (isNaN(otherBase)) return;

                const otherInput = other.querySelector(".ingredient-input");
                if (otherInput) {
                    otherInput.value = formatIngredientQty(otherBase * normalizedScale);
                }
            });

            isUpdating = false;
            updateScaleUI();
        });

        input.addEventListener("change", function () {
            if (isUpdating) return;
            isUpdating = true;

            const newQty = snapToHalf(this.value);
            if (!isNaN(newQty) && newQty > 0 && !isNaN(baseQty) && baseQty > 0) {
                const scale = newQty / baseQty;
                let newServings = Math.round(baseServings * scale);
                if (newServings <= 0) newServings = 1;
                const normalizedScale = newServings / baseServings;
                this.value = formatIngredientQty(baseQty * normalizedScale);
            }

            isUpdating = false;
            updateScaleUI();
        });
    });
});
