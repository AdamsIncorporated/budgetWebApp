function filterTable() {
    // Get the input value and convert it to lower case
    const filter = document.getElementById("filterInput").value.toLowerCase();
    const table = document.getElementById("businessUnitsTable");
    const rows = table.getElementsByTagName("tr");

    // Loop through all table rows (except the first, which is the header)
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        let rowVisible = false;

        // Loop through the cells in the current row
        for (let j = 0; j < cells.length; j++) {
            // Check if the cell contains the filter text
            if (cells[j].textContent.toLowerCase().includes(filter)) {
                rowVisible = true; // Mark the row as visible if a match is found
                break; // Exit the inner loop if a match is found
            }
        }

        // Show or hide the row based on whether it matched the filter
        rows[i].style.display = rowVisible ? "" : "none";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const containers = {
        delete: document.getElementById('deleteModalContainer'),
        edit: document.getElementById('editModalContainer'),
        create: document.getElementById('createModalContainer'),
    };

    const fetchData = async (url, container) => {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.text();
            container.innerHTML = `<div>${data}</div>`;
            container.style.display = 'block';
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    };

    document.querySelectorAll('button[delete]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('rowId');
            fetchData(`/dashboard/delete?id=${id}`, containers.delete);
        });
    });

    document.getElementById('createButton').addEventListener('click', () => {
        fetchData('/dashboard/create', containers.create);
    });

    document.querySelectorAll('button[edit]').forEach((btn) => {
        btn.addEventListener('click', () => {
            const id = btn.getAttribute('rowId');
            fetchData(`/dashboard/edit?id=${id}`, containers.edit);
        });
    });
});
