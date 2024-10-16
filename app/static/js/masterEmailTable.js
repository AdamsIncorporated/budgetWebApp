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
