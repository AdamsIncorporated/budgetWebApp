document.addEventListener('DOMContentLoaded', function () {
    const customPalette = [
        '#06B6D4', // Cyan 500
        '#0EA5E9', // Cyan 600
        '#14B8A6', // Teal 500
        '#0D9488', // Teal 600
        '#0F766E', // Teal 700
    ];

    // Initial setup
    const canvases = document.querySelectorAll('#canvasSlider > div');
    let currentIndex = 0;

    function updateCanvasVisibility() {
        const offset = -currentIndex * 100; // Calculate offset
        document.getElementById('canvasSlider').style.transform = `translateX(${offset}%)`;
    }

    fetch('/dashboard/budget-pie-chart')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const labels = data.records.map(item => item.BusinessUnit);
            const budgetAmounts = data.records.map(item => item.TotalBudgetByDepartment);

            const ctx = document.getElementById('budgetPieChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Total Budget Amount',
                        data: budgetAmounts,
                        backgroundColor: customPalette.slice(0, labels.length),
                        borderColor: customPalette.slice(0, labels.length),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            font: {
                                size: 34,
                                weight: 'bold',
                            },
                            display: true,
                            text: 'Budget Allocation by Business Unit'
                        },
                        legend: {
                            display: false
                        },
                        tooltip: {
                            callbacks: {
                                label: function (tooltipItem) {
                                    // Format the raw value with commas and fixed to two decimal places
                                    const formattedValue = tooltipItem.raw.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
                                    return `${tooltipItem.label}: $${formattedValue}`;
                                }
                            }
                        }
                    }
                }
            });

            // Setup another chart if needed
            // For example: setupAnotherChart();

        })
        .catch(error => console.error('Error loading chart data:', error));

    document.getElementById('nextBtn').addEventListener('click', function () {
        currentIndex = (currentIndex + 1) % canvases.length; // Cycle through canvases
        updateCanvasVisibility();
    });

    document.getElementById('prevBtn').addEventListener('click', function () {
        currentIndex = (currentIndex - 1 + canvases.length) % canvases.length; // Cycle through canvases
        updateCanvasVisibility();
    });
});
