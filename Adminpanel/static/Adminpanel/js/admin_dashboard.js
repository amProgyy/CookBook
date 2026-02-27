function toggleRejectForm(recipeId) {
    const formDiv = document.getElementById('reject-form-' + recipeId);
    if (formDiv.style.display === 'none' || formDiv.style.display === '') {
        formDiv.style.display = 'block';
    } else {
        formDiv.style.display = 'none';
    }
}
