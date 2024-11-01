
document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', (event) => {
        if (event.target.id === 'closeModalBtn') {
            const element = event.target;
            const modal = element.closest('[modal]') || exit('Error: Modal not found!');

            modal.classList.remove('fade-in-down');
            modal.classList.add('fade-out-up');

            setTimeout(() => {
                document.getElementById('modalContainer').remove();
            }, 300)
        }
    });

    document.addEventListener('input', async (event) => {
        const isRad = document.getElementById('is_rad').value == 'y';

        if (event.target.id === 'account' && isRad) {
            const element = event.target;
            url = `/dashboard/get-rads?Account=${element.value}`

            const response = await fetch(url);
            const data = await response.json();

            const optionsSelect = document.getElementById('rad');
            optionsSelect.innerHTML = '';

            if (data && data.length > 0) {
                data.forEach(option => {
                    const newOption = document.createElement('option');
                    newOption.value = option;
                    newOption.label = option;
                    optionsSelect.appendChild(newOption);
                });
                optionsSelect.parentElement.classList.remove('hidden');
            } else {
                optionsSelect.parentElement.classList.add('hidden');
            }

        }
    });


    const rows = document.querySelectorAll('#budget-entries tr');
    let draggedRow = null;

    rows.forEach(row => {
        row.addEventListener('dragstart', () => {
            draggedRow = row;
            row.classList.add('opacity-30');
        });

        row.addEventListener('dragend', () => {
            draggedRow = null;
            row.classList.remove('opacity-30');
        });

        row.addEventListener('dragover', (event) => {
            event.preventDefault(); // Allow the drop
        });

        row.addEventListener('drop', () => {
            if (draggedRow !== row) {
                const parent = row.parentNode;
                parent.insertBefore(draggedRow, row.nextSibling || row);
                updateDisplayOrder();
            }
        });
    });

    function updateDisplayOrder() {
        const newOrder = Array.from(document.querySelectorAll('#budget-entries tr')).map((row, index) => {
            const displayOrderInput = row.querySelector('td:first-child input'); // Adjust the selector if needed
            if (displayOrderInput) {
                displayOrderInput.value = index + 1;
            }
            return {
                id: row.dataset.id,
                order: index + 1
            };
        });
    }

    function appendModalHtml(data) {
        document.getElementById('modalContainer')?.remove();

        const contentDiv = document.createElement('div');
        const parser = new DOMParser();
        const doc = parser.parseFromString(data, 'text/html');

        // Extract the body content and append it to the container
        const content = document.importNode(doc.body, true);
        contentDiv.appendChild(content);
        contentDiv.id = 'modalContainer';

        document.querySelector('body').append(contentDiv);
    }

    const fetchData = async (url) => {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.text();
            appendModalHtml(data);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    };

    document.querySelectorAll('[delete]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('rowId');
            fetchData(`/dashboard/budget-admin-view/delete?id=${id}`);
        });
    });

    document.querySelector('[create]').addEventListener('click', () => {
        fetchData('/dashboard/budget-admin-view/create');
    });

    document.addEventListener("click", async (event) => {
        if (event.target.id !== 'createFormSubmitBtn') return;

        event.preventDefault(); // Prevent default form submission

        const form = document.getElementById('createForm');
        const formData = new FormData(form);
        const url = form.action;
        const method = form.method;

        try {
            const response = await fetch(url, {
                method: method,
                body: formData,
            });

            if (response.redirected) {
                // If the server responds with a redirect, navigate to the new URL
                window.location.href = response.url;
            } else if (response.ok) {
                // If the response is OK, render the new form with error messages if needed
                const data = await response.text();
                appendModalHtml(data);
            }
        } catch (error) {
            throw new Error("An error occurred while submitting the form. Please try again.");
        }
    });
});