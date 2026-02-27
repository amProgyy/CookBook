document.addEventListener("DOMContentLoaded", function () {
    // =========================
    // INGREDIENTS
    // =========================

    const ingContainer = document.getElementById("ingredient-container");
    const ingAddBtn = document.getElementById("add-ingredient");
    const ingTotal = document.getElementById("id_ingredients-TOTAL_FORMS");
    const recipeForm = document.getElementById("recipeForm");
    const titleInput = document.getElementById("id_title");
    const servingsInput = document.getElementById("id_number_of_servings");
    const mainWarning = document.getElementById("main-warning");
    const ingredientWarning = document.getElementById("ingredient-warning");

    function isDeletedIngredientForm(form) {
        const deleteInput = form.querySelector('input[type="checkbox"][name$="-DELETE"]');
        return form.classList.contains("deleted-ingredient") ||
            form.style.display === "none" ||
            (deleteInput && deleteInput.checked);
    }

    function getIngredientNumber(form, index) {
        const numberEl = form.querySelector(".ingredient-number");
        if (numberEl && numberEl.textContent.trim()) {
            return numberEl.textContent.replace(".", "").trim();
        }
        return String(index + 1);
    }

    function getRowWarning(form) {
        const next = form.nextElementSibling;
        if (next && next.classList.contains("ingredient-row-warning")) {
            return next;
        }
        const warning = document.createElement("p");
        warning.className = "ingredient-row-warning";
        warning.setAttribute("aria-live", "polite");
        warning.style.display = "none";
        warning.style.color = "#B42318";
        warning.style.margin = "0 0 10px 30px";
        warning.style.fontWeight = "600";
        warning.style.fontSize = "13px";
        form.insertAdjacentElement("afterend", warning);
        return warning;
    }

    function clearFieldError(field) {
        if (!field) return;
        field.classList.remove("input-error");
        field.removeAttribute("aria-invalid");
        field.style.borderBottomColor = "";
        field.style.borderBottomWidth = "";
    }

    function markFieldError(field) {
        if (!field) return;
        field.classList.add("input-error");
        field.setAttribute("aria-invalid", "true");
        field.style.borderBottomColor = "#B42318";
        field.style.borderBottomWidth = "2px";
    }

    function clearRowWarning(form) {
        const next = form.nextElementSibling;
        if (next && next.classList.contains("ingredient-row-warning")) {
            next.textContent = "";
            next.classList.remove("show");
            next.style.display = "none";
        }
    }

    function showRowWarning(form, message) {
        const warning = getRowWarning(form);
        warning.textContent = message;
        warning.classList.add("show");
        warning.style.display = "block";
    }

    function clearSectionWarning() {
        if (!ingredientWarning) return;
        ingredientWarning.textContent = "";
        ingredientWarning.classList.remove("show");
        ingredientWarning.style.display = "none";
    }

    function showSectionWarning(message) {
        if (!ingredientWarning) return;
        ingredientWarning.textContent = message;
        ingredientWarning.classList.add("show");
        ingredientWarning.style.display = "block";
        ingredientWarning.style.color = "#B42318";
        ingredientWarning.style.fontWeight = "700";
        ingredientWarning.style.fontSize = "14px";
    }

    function clearMainWarning() {
        if (!mainWarning) return;
        mainWarning.textContent = "";
        mainWarning.classList.remove("show");
        mainWarning.style.display = "none";
    }

    function showMainWarning(message) {
        if (!mainWarning) return;
        mainWarning.textContent = message;
        mainWarning.classList.add("show");
        mainWarning.style.display = "block";
        mainWarning.style.color = "#B42318";
        mainWarning.style.fontWeight = "700";
        mainWarning.style.fontSize = "14px";
    }

    function updateIngredientNumbers() {
        ingContainer.querySelectorAll(".ingredient-form:not(.deleted-ingredient)").forEach((item, i) => {
            const span = item.querySelector(".ingredient-number");
            if (span) span.textContent = `${i + 1}. `;
        });
    }

    function validateIngredients() {
        if (!ingContainer) return true;

        clearSectionWarning();

        let validIngredientCount = 0;
        let hasErrors = false;
        let firstActiveForm = null;

        const forms = ingContainer.querySelectorAll(".ingredient-form");
        forms.forEach((form, index) => {
            clearRowWarning(form);

            const nameInput = form.querySelector(".ingredient-name");
            const qtyInput = form.querySelector(".ingredient-quantity");
            const unitInput = form.querySelector(".ingredient-unit");

            clearFieldError(nameInput);
            clearFieldError(qtyInput);
            clearFieldError(unitInput);

            if (isDeletedIngredientForm(form)) return;

            if (!firstActiveForm) firstActiveForm = form;

            const nameValue = nameInput ? nameInput.value.trim() : "";
            const qtyValue = qtyInput ? qtyInput.value.trim() : "";
            const unitValue = unitInput ? unitInput.value.trim() : "";
            const hasAnyValue = nameValue || qtyValue || unitValue;

            if (!hasAnyValue) return;

            const missingFields = [];
            if (!nameValue) {
                missingFields.push("name");
                markFieldError(nameInput);
            }
            if (!qtyValue) {
                missingFields.push("quantity");
                markFieldError(qtyInput);
            }
            if (!unitValue) {
                missingFields.push("unit");
                markFieldError(unitInput);
            }

            if (missingFields.length > 0) {
                hasErrors = true;
                const ingredientNumber = getIngredientNumber(form, index);
                showRowWarning(form, `Ingredient ${ingredientNumber}: ${missingFields.join(", ")} required.`);
                return;
            }

            validIngredientCount += 1;
        });

        if (validIngredientCount === 0) {
            hasErrors = true;
            showSectionWarning("Ingredients: add at least one ingredient with name, quantity, and unit.");

            if (firstActiveForm) {
                const ingredientNumber = getIngredientNumber(firstActiveForm, 0);
                showRowWarning(firstActiveForm, `Ingredient ${ingredientNumber}: name, quantity, and unit required.`);
                markFieldError(firstActiveForm.querySelector(".ingredient-name"));
                markFieldError(firstActiveForm.querySelector(".ingredient-quantity"));
                markFieldError(firstActiveForm.querySelector(".ingredient-unit"));
            }
        }

        return !hasErrors;
    }

    function validateMainFields() {
        clearMainWarning();
        clearFieldError(titleInput);
        clearFieldError(servingsInput);

        const titleMissing = !titleInput || !titleInput.value.trim();
        const servingsRaw = servingsInput ? servingsInput.value.trim() : "";
        const servingsValue = parseInt(servingsRaw, 10);
        const servingsMissing = !servingsRaw || !Number.isFinite(servingsValue) || servingsValue <= 0;

        if (!titleMissing && !servingsMissing) {
            return true;
        }

        if (titleMissing) {
            markFieldError(titleInput);
        }
        if (servingsMissing) {
            markFieldError(servingsInput);
        }

        if (titleMissing && servingsMissing) {
            showMainWarning("Write the Recipe title and enter the number of person.");
        } else if (titleMissing) {
            showMainWarning("Write the Recipe title.");
        } else {
            showMainWarning("Enter the number of person.");
        }

        return false;
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

        newForm.classList.remove("deleted-ingredient");
        newForm.style.display = "";
        clearRowWarning(newForm);
        newForm.querySelectorAll(".input-error").forEach(clearFieldError);

        ingContainer.appendChild(newForm);
        ingTotal.value = count + 1;
        updateIngredientNumbers();
    });

    ingContainer.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-ingredient")) {

            const form = e.target.closest(".ingredient-form");
            const deleteInput = form.querySelector('input[type="checkbox"][name$="-DELETE"]');

            if (deleteInput) {
                // For editing existing ingredients (checking the Django DELETE checkbox)
                deleteInput.checked = true;
                form.style.display = "none";
                form.classList.add("deleted-ingredient");
                clearRowWarning(form);
            } else {
                // For newly added ingredients (just remove from DOM)
                const warningEl = form.nextElementSibling;
                if (warningEl && warningEl.classList.contains("ingredient-row-warning")) {
                    warningEl.remove();
                }
                form.remove();
            }

            // DO NOT DECREMENT TOTAL_FORMS! Django needs it to track the highest index submitted.
            updateIngredientNumbers();
        }
    });


    updateIngredientNumbers();
    clearMainWarning();
    clearSectionWarning();

    if (titleInput) {
        titleInput.addEventListener("input", function () {
            clearMainWarning();
            clearFieldError(titleInput);
        });
    }
    if (servingsInput) {
        servingsInput.addEventListener("input", function () {
            clearMainWarning();
            clearFieldError(servingsInput);
        });
    }

    if (recipeForm) {
        recipeForm.addEventListener("submit", function (e) {
            const isMainValid = validateMainFields();
            const areIngredientsValid = validateIngredients();

            if (!isMainValid || !areIngredientsValid) {
                e.preventDefault();
                if (!isMainValid) {
                    const mainSection = mainWarning ? mainWarning.closest(".recipe-left") : null;
                    if (mainSection) {
                        mainSection.scrollIntoView({ behavior: "smooth", block: "start" });
                    }
                } else {
                    const section = ingredientWarning ? ingredientWarning.closest(".section-card") : null;
                    if (section) {
                        section.scrollIntoView({ behavior: "smooth", block: "center" });
                    }
                }
            }
        });
    }

    // =========================
    // SERVING SCALING
    // =========================
    if (servingsInput) {
        let previousServings = parseFloat(servingsInput.value) || 1;

        // Update previousServings when user focuses to type
        servingsInput.addEventListener("focus", function () {
            previousServings = parseFloat(this.value) || 1;
        });

        servingsInput.addEventListener("change", function () {
            const currentServings = parseFloat(this.value);

            if (!currentServings || currentServings <= 0 || previousServings <= 0 || previousServings === currentServings) {
                previousServings = currentServings || 1;
                return;
            }

            // Ask user if they want to scale the ingredients
            const doScale = confirm(`You changed servings from ${previousServings} to ${currentServings}. Scale ingredient quantities?`);

            if (doScale) {
                const scale = currentServings / previousServings;

                const qtyInputs = document.querySelectorAll(".ingredient-quantity");
                qtyInputs.forEach(input => {
                    if (input.value) {
                        const currentQty = parseFloat(input.value);
                        if (!isNaN(currentQty)) {
                            let newQty = (currentQty * scale).toFixed(2);
                            if (newQty.endsWith('.00')) {
                                newQty = parseInt(newQty);
                            }
                            input.value = newQty;
                        }
                    }
                });
            }

            previousServings = currentServings;
        });
    }


    // =========================
    // STEPS (FORMSET SAFE)
    // =========================

    const stepContainer = document.getElementById("step-container");
    const addStepBtn = document.getElementById("add-step");
    const totalForms = document.getElementById("id_steps-TOTAL_FORMS");
    const emptyFormTemplate = document.getElementById("empty-step-form").innerHTML;

    function autoGrowStepTextarea(textarea) {
        if (!textarea) return;
        textarea.style.height = "auto";
        textarea.style.height = `${textarea.scrollHeight}px`;
    }

    function autoGrowAllStepTextareas() {
        if (!stepContainer) return;
        stepContainer.querySelectorAll("textarea.step-instruction").forEach(autoGrowStepTextarea);
    }

    if (stepContainer) {
        stepContainer.addEventListener("input", function (e) {
            const target = e.target;
            if (target && target.matches && target.matches("textarea.step-instruction")) {
                autoGrowStepTextarea(target);
            }
        });
    }

    function updateStepNumbers() {
        const forms = stepContainer.querySelectorAll(".step-form:not([style*='display: none'])");
        forms.forEach((form, index) => {
            const number = form.querySelector(".step-number");
            if (number) number.textContent = (index + 1) + ".";
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
        autoGrowStepTextarea(newForm.querySelector("textarea.step-instruction"));
    });

    stepContainer.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-step")) {

            const form = e.target.closest(".step-form");
            const deleteInput = form.querySelector('input[type="checkbox"][name$="-DELETE"]');

            if (deleteInput) {
                // For editing existing steps (checking the Django DELETE checkbox)
                deleteInput.checked = true;
                form.style.display = "none";
                form.classList.add("deleted-step");
            } else {
                // For newly added steps (just remove from DOM)
                form.remove();
            }

            // Recalculate TOTAL_FORMS properly for the step container
            const updatedForms = stepContainer.querySelectorAll(".step-form:not(.deleted-step)");
            // If we actually removed it from DOM, we might need to update totalForms, 
            // but Django formsets usually expect TOTAL_FORMS to include deleted forms. 
            // The safest thing for steps is to let Django handle the extra deleted inputs.

            updateStepNumbers();
        }
    });


    updateStepNumbers();
    autoGrowAllStepTextareas();
});


// =========================
// RECIPE IMAGE
// =========================

document.addEventListener("DOMContentLoaded", function () {

    const input = document.querySelector(".image-input");
    const preview = document.getElementById("image-preview");
    const uploadBox = document.querySelector(".upload-box");

    if (input) {
        input.addEventListener("change", function () {
            const file = this.files[0];

            if (file) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    preview.src = e.target.result;
                    uploadBox.classList.add("has-image");
                };

                reader.readAsDataURL(file);
            } else {
                uploadBox.classList.remove("has-image");
            }
        });
    }

});


// =========================
// STEP IMAGE
// =========================

document.addEventListener("change", function (e) {

    if (e.target.type === "file") {

        const label = e.target.closest(".step-upload-label");
        const preview = label.querySelector(".step-preview");
        const placeholder = label.querySelector(".upload-placeholder");

        const file = e.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (event) {
                preview.src = event.target.result;
                preview.style.display = "block";
                if (placeholder) {
                    placeholder.style.display = "none";
                }
            };

            reader.readAsDataURL(file);
        }
    }

});

// =========================
// SELECT2 TAG
// =========================


$(document).ready(function () {
    $('.tag-select').select2({
        placeholder: "Select or add tags",
        tags: true,              // allows new tags
        tokenSeparators: [','],  // press comma to create tag
        allowClear: true
    });
});
