document.addEventListener("DOMContentLoaded", function () {

    // --- Ingredients ---
    const ingContainer = document.getElementById("ingredient-container");
    const ingAddBtn = document.getElementById("add-ingredient");
    const ingTotal = document.getElementById("id_ingredients-TOTAL_FORMS");

    function updateIngredientNumbers() {
        ingContainer.querySelectorAll(".ingredient-form").forEach((item, i) => {
            const span = item.querySelector(".ingredient-number");
            if(span) span.textContent = `${i + 1}. `;
        });
    }

    ingAddBtn.addEventListener("click", () => {
        const count = parseInt(ingTotal.value);
        const last = ingContainer.querySelector(".ingredient-form:last-child");
        const newForm = last.cloneNode(true);

        newForm.querySelectorAll("input, select").forEach(input => {
            input.name = input.name.replace(/-\d+-/, `-${count}-`);
            input.id = input.id.replace(/-\d+-/, `-${count}-`);
            if(input.type !== "checkbox") input.value = "";
            else input.checked = false;
        });

        ingContainer.appendChild(newForm);
        ingTotal.value = count + 1;
        updateIngredientNumbers();
    });

    ingContainer.addEventListener("click", e => {
        if(e.target.classList.contains("remove-ingredient")) {
            const forms = ingContainer.querySelectorAll(".ingredient-form");
            if(forms.length > 1){
                e.target.closest(".ingredient-form").remove();
                ingTotal.value = forms.length;
                updateIngredientNumbers();
            }
        }
    });

    updateIngredientNumbers();


    // --- Steps ---
    const stepContainer = document.getElementById("step-container");
    const stepAddBtn = document.getElementById("add-step");
    const stepTotal = document.getElementById("id_steps-TOTAL_FORMS");

    function updateStepNumbers() {
        stepContainer.querySelectorAll(".step-form").forEach((item, i) => {
            const span = item.querySelector(".step-number");
            if(span) span.textContent = ` ${i + 1}: `;
            const hidden = item.querySelector('input[type="hidden"]');
            if(hidden) hidden.value = i + 1; // step_number
        });
    }

    stepAddBtn.addEventListener("click", () => {
        const count = parseInt(stepTotal.value);
        const last = stepContainer.querySelector(".step-form:last-child");
        const newForm = last.cloneNode(true);

        newForm.querySelectorAll('input, textarea').forEach(input => {
            input.name = input.name.replace(/-\d+-/, `-${count}-`);
            input.id = input.id.replace(/-\d+-/, `-${count}-`);
            if(input.tagName === "TEXTAREA") input.value = "";
            if(input.type === "hidden") input.value = count + 1;
        });

        stepContainer.appendChild(newForm);
        stepTotal.value = count + 1;
        updateStepNumbers();
    });

    stepContainer.addEventListener("click", e => {
        if(e.target.classList.contains("remove-step")){
            const forms = stepContainer.querySelectorAll(".step-form");
            if(forms.length > 1){
                e.target.closest(".step-form").remove();
                stepTotal.value = forms.length;
                updateStepNumbers();
            }
        }
    });

    updateStepNumbers();

});
