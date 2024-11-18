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
    updateTable()
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

const getTableText = (divider) => {
    // Get the headers from the table
    const headers = Array.from(document.querySelectorAll('thead th'))
        .map(header => header.textContent.trim())
        .join(divider);
    
    // Get the data rows from the table
    const rows = Array.from(document.querySelectorAll('tbody tr'));
    const td = rows
        .map(row => Array.from(row.querySelectorAll('td'))
            .map(cell => cell.textContent.trim())
            .join(divider))
        .join('\n');

    // Return the full table text
    return `${headers}\n${td}`;
};


const handleCopy = (evt) => {
    if (!navigator.clipboard) {
        return;
    }
    const text = getTableText(divider="\t");
    navigator.clipboard.writeText(text).then(() => {
        console.log("Copied to clipboard");
        const copyToolTip = document.getElementById('copyToolTip');
        copyToolTip.classList.remove('hidden');
        setTimeout(() => copyToolTip.classList.add('hidden'), 1000);
    });
};


function getCSVFile() {
    const fiscalYearSelect = document.getElementById('fiscal_year');
    const businessUnitSelect = document.getElementById('business_unit');
    const fiscalYear = fiscalYearSelect.value;
    const businessUnitId = businessUnitSelect.value;
    const url = `/dashboard/home/download-csv-table?fiscalYear=${fiscalYear}&businessUnitId=${businessUnitId}`;
    fetch(url, {
        method: "GET",
    })
        .then(response => response.blob())  // Expecting a file (blob)
        .then(blob => {
            // Create a link element, use it to download the file
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'output.xlsx';  // The file name
            link.click();
        })
        .catch(error => console.error('Error downloading the file:', error));
}
