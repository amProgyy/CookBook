document.addEventListener('DOMContentLoaded', () => {
    const searchInputs = document.querySelectorAll('.header-search-form input[name="q"]');

    searchInputs.forEach(input => {
        // Wrap input in autocomplete-wrapper if not already
        if (!input.parentNode.classList.contains('autocomplete-wrapper')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'autocomplete-wrapper';
            wrapper.style.flex = '1';
            wrapper.style.display = 'flex';
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);

            const dropdown = document.createElement('div');
            dropdown.className = 'autocomplete-dropdown';
            wrapper.appendChild(dropdown);

            let debounceTimer;

            // Turn off default browser autocomplete
            input.setAttribute('autocomplete', 'off');

            input.addEventListener('input', (e) => {
                clearTimeout(debounceTimer);
                const val = e.target.value.trim();

                if (val.length < 2) {
                    dropdown.innerHTML = '';
                    return;
                }

                debounceTimer = setTimeout(() => {
                    fetch(`/search-recommendations/?q=${encodeURIComponent(val)}`, {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    })
                        .then(res => res.json())
                        .then(data => {
                            dropdown.innerHTML = '';
                            if (data.results && data.results.length > 0) {
                                data.results.forEach(item => {
                                    const div = document.createElement('div');
                                    div.className = 'autocomplete-item';
                                    div.textContent = item;

                                    div.addEventListener('click', () => {
                                        input.value = item;
                                        dropdown.innerHTML = '';
                                        input.closest('form').submit();
                                    });

                                    dropdown.appendChild(div);
                                });
                            }
                        })
                        .catch(err => console.error("Error fetching search recommendations:", err));
                }, 300);
            });

            // Close dropdown if clicking outside
            document.addEventListener('click', (e) => {
                if (!wrapper.contains(e.target)) {
                    dropdown.innerHTML = '';
                }
            });
        }
    });
});
