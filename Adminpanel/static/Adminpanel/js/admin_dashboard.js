function toggleRejectForm(recipeId) {
    const formDiv = document.getElementById('reject-form-' + recipeId);
    if (formDiv.style.display === 'none' || formDiv.style.display === '') {
        formDiv.style.display = 'block';
    } else {
        formDiv.style.display = 'none';
    }
}

async function confirmApprove(event, form) {
    event.preventDefault();
    const confirmed = await savoryConfirm("Are you sure you want to approve this recipe? It will be visible to the public.", {
        title: "Approve Recipe",
        confirmText: "Yes, Approve",
        cancelText: "Cancel"
    });
    if (confirmed) {
        form.submit();
    }
}

async function confirmReject(event, form) {
    event.preventDefault();
    const confirmed = await savoryConfirm("Are you sure you want to reject this recipe? The author will be notified.", {
        title: "Reject Recipe",
        confirmText: "Yes, Reject",
        cancelText: "Cancel"
    });
    if (confirmed) {
        form.submit();
    }
}
