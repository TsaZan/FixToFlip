document.addEventListener('DOMContentLoaded', () => {
    const allCategories = [
        'Utilities', 'Notary Taxes', 'Profit Tax', 'Municipality Taxes',
        'Advertising', 'Administrative Fees', 'Insurance', 'Credit Interest', 'Other Expenses',
        'Bathroom Repair Expenses', 'Kitchen Repair Expenses', 'Floors Repair Expenses',
        'Walls Repair Expenses', 'Windows and Doors Repair Expenses', 'Plumbing Repair Expenses',
        'Electrical Repair Expenses', 'Roof Repair Expenses', 'Facade Repair Expenses',
        'Other Repair Expenses'
    ];

    function loadChart(apiUrl) {
        fetch(apiUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // console.log('API Response:', data);

                const expenseData = allCategories.map(category => {
                    if (data[category] === undefined) {
                        // console.warn(`Missing data for ${category}, assigning 0.`);
                        return 0;
                    }
                    return data[category];
                });

                // console.log('Mapped Expense Data:', expenseData);

                if (window.propertyExpensesChart) {
                    window.propertyExpensesChart.destroy();
                }

                const ctx = document.getElementById('property-expenses-chart').getContext('2d');
                window.propertyExpensesChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: allCategories,
                        datasets: [{
                            label: 'Property Expenses',
                            data: expenseData,
                            backgroundColor: 'rgba(54, 162, 235, 0.6)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Expense Amount'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Expense Categories'
                                }
                            }
                        },
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top'
                            }
                        }
                    }
                });
            })
            .catch(error => {
                // console.error('Error loading chart:', error);
            });
    }

    function applyDateFilter() {
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;

        let apiUrl = '/properties/api-expenses/';
        if (startDate || endDate) {
            apiUrl += `?${startDate ? `start_date=${startDate}` : ''}${startDate && endDate ? '&' : ''}${endDate ? `end_date=${endDate}` : ''}`;
        }

        loadChart(apiUrl);
    }

    function resetDates() {
        document.getElementById('start-date').value = '';
        document.getElementById('end-date').value = '';

        loadChart('/properties/api-expenses/');
    }


    const resetButton = document.getElementById('reset-button');
    if (resetButton) {
        resetButton.addEventListener('click', resetDates);
    }

    const filterButton = document.getElementById('filter-button');
    if (filterButton) {
        filterButton.addEventListener('click', applyDateFilter);
    }

    loadChart('/properties/api-expenses/');
});
