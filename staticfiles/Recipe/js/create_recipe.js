document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // INGREDIENTS
    // =========================

    const ingContainer = document.getElementById("ingredient-container");
    const ingAddBtn = document.getElementById("add-ingredient");
    const ingTotal = document.getElementById("id_ingredients-TOTAL_FORMS");

    function updateIngredientNumbers() {
        ingContainer.querySelectorAll(".ingredient-form").forEach((item, i) => {
            const span = item.querySelector(".ingredient-number");
            if (span) span.textContent = `${i + 1}. `;
        });
    }

    ingAddBtn.addEventListener("click", () => {
        const count = parseInt(ingTotal.value);
        const last = ingContainer.querySelector(".ingredient-form:last-child");
        const newForm = last.cloneNode(true);

        newForm.querySelectorAll("input, select, textarea").forEach(input => {
            input.name = input.name.replace(/-\d+-/, `-${count}-`);
            input.id = input.id.replace(/-\d+-/, `-${count}-`);

            if (input.type === "checkbox") {
                input.checked = false;
            } else {
                input.value = "";
            }
        });

        ingContainer.appendChild(newForm);
        ingTotal.value = count + 1;
        updateIngredientNumbers();
    });

    ingContainer.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-ingredient")) {

            const forms = ingContainer.querySelectorAll(".ingredient-form");

            if (forms.length > 1) {

                e.target.closest(".ingredient-form").remove();

                // Recalculate TOTAL_FORMS properly
                const updatedForms = ingContainer.querySelectorAll(".ingredient-form");
                ingTotal.value = updatedForms.length;

                updateIngredientNumbers();
            }
        }
    });


    updateIngredientNumbers();


    // =========================
    // STEPS (FORMSET SAFE)
    // =========================

    const stepContainer = document.getElementById("step-container");
    const addStepBtn = document.getElementById("add-step");
    const totalForms = document.getElementById("id_steps-TOTAL_FORMS");
    const emptyFormTemplate = document.getElementById("empty-step-form").innerHTML;

    function updateStepNumbers() {
        const forms = stepContainer.querySelectorAll(".step-form:not([style*='display: none'])");
        forms.forEach((form, index) => {
            const number = form.querySelector(".step-number");
            if (number) number.textContent =  (index + 1) + ".";
        });
    }

    addStepBtn.addEventListener("click", function () {

        let formIndex = parseInt(totalForms.value);

        let newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formIndex);

        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = newFormHtml;

        const newForm = tempDiv.firstElementChild;

        // CLEAR FILE INPUT SAFELY
        const fileInput = newForm.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.value = "";
        }

        stepContainer.appendChild(newForm);

        totalForms.value = formIndex + 1;

        updateStepNumbers();
    });

    stepContainer.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-step")) {

            const form = e.target.closest(".step-form");
            const deleteInput = form.querySelector('input[type="checkbox"][name$="-DELETE"]');

            if (deleteInput) {
                deleteInput.checked = true;
                form.style.display = "none";
            }

            updateStepNumbers();
        }
    });


    updateStepNumbers();
});
