document.addEventListener('DOMContentLoaded', () => {
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

    async function deleteRow(element) {
        const id = parseInt(element.getAttribute('data-id'), 10);
        const url = `/budget-admin-view-delete/${id}`;

        try {
            const response = await fetch(url, { method: 'DELETE' });

            if (!response.ok) {
                throw new Error(`Failed to delete row with ID ${id}: ${response.statusText}`);
            }

            // Optional: remove the row from the DOM if delete was successful
            element.closest('tr').remove();
            console.log(`Row with ID ${id} deleted successfully.`);
        } catch (error) {
            console.error('Error:', error);
        }
    }
});