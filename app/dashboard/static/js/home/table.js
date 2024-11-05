document.addEventListener('DOMContentLoaded', () => {
    const tableContainer = document.getElementById('tableContainer');
    const fiscalYearSelect = document.getElementById('fiscal_year');
    const businessUnitSelect = document.getElementById('business_unit');

    const updateTableData = async (url) => {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const html = await response.text();
            tableContainer.innerHTML = html;
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            tableContainer.innerHTML = errorHtml;
        }
    };

    const updateTable = () => {
        const fiscalYear = fiscalYearSelect.value;
        const businessUnitId = businessUnitSelect.value;
        tableContainer.innerHTML = skeletonLoaderHtml;
        const url = `/dashboard/home/table?fiscalYear=${fiscalYear}&businessUnitId=${businessUnitId}`;
        updateTableData(url);
    };

    fiscalYearSelect.addEventListener('change', updateTable);
    businessUnitSelect.addEventListener('change', updateTable);
});

const errorHtml = `
    <div class="text-center text-3xl bg-gradient-to-r from-rose-300 to-red-600 bg-clip-text text-transparent font-bold">
    <h1>There was an error loading the data!</h1>
    </div>
`

const skeletonLoaderHtml = `
    <div class="animate-pulse">
        <div class="h-4 bg-gray-200 mt-3 mb-6 rounded"></div>
        <div class="h-4 bg-gray-300 mb-6 rounded"></div>
        <div class="h-4 bg-gray-200 mb-6 rounded"></div>
        <div class="h-4 bg-gray-300 mb-6 rounded"></div>
        <div class="h-4 bg-gray-200 mb-6 rounded"></div>
    </div>
`
