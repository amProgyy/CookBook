document.addEventListener("DOMContentLoaded", function () {
    const addBtn = document.getElementById("add-step");
    const container = document.getElementById("step-container");
    const totalForms = document.getElementById("id_form-TOTAL_FORMS");

    // Update step numbers in HTML and hidden input
    function updateStepNumbers() {
        const steps = container.querySelectorAll(".step-form");
        steps.forEach((step, index) => {
            // Update visible number
            const numberSpan = step.querySelector(".step-number");
            if (numberSpan) {
                numberSpan.textContent = `${index + 1}: `;
            }

            // Update hidden step_number field
            const hiddenInput = step.querySelector('input[type="hidden"]');
            if (hiddenInput) {
                hiddenInput.value = index + 1;
            }
        });
    }

    // Add new step
    addBtn.addEventListener("click", function () {
        const formCount = parseInt(totalForms.value);
        const lastForm = container.querySelector(".step-form:last-child");
        const newForm = lastForm.cloneNode(true);

        // Clear textarea
        const textarea = newForm.querySelector("textarea");
        if (textarea) textarea.value = "";

        // Update input names and ids
        newForm.querySelectorAll('input, textarea').forEach(input => {
            input.name = input.name.replace(/-\d+-/, `-${formCount}-`);
            input.id = input.id.replace(/-\d+-/, `-${formCount}-`);
        });

        container.appendChild(newForm);

        // Update TOTAL_FORMS
        totalForms.value = formCount + 1;

        // Update step numbers
        updateStepNumbers();
    });

    // Remove step
    container.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-step")) {
            const steps = container.querySelectorAll(".step-form");
            if (steps.length > 1) {
                e.target.closest(".step-form").remove();
                totalForms.value = steps.length - 1;
                updateStepNumbers();
            }
        }
    });

    // Initial numbering
    updateStepNumbers();
});
