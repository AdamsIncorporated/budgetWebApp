document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('fiscal_year').addEventListener('change', () => {
        document.getElementById('fiscalYearForm').submit();
    });

    document.getElementById('downloadBtn').addEventListener('click', () => { 
        const fiscalYear = document.getElementById('fiscal_year').value;

        fetch(`/dashboard/download-template/${fiscalYear}`, {
            method: "GET",
        })
        .then(response => response.blob())  // Expecting a file (blob)
        .then(blob => {
            // Create a link element, use it to download the file
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'template.xlsx';  // The file name
            link.click();
        })
        .catch(error => console.error('Error downloading the file:', error));
    });
})
