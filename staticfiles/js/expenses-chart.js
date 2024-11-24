document.addEventListener('DOMContentLoaded', () => {
    function loadChart(apiUrl) {
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                console.log('Chart Data:', data);

                if (window.propertyExpensesChart) {
                    window.propertyExpensesChart.destroy();
                }

                const ctx = document.getElementById('property-expenses-chart').getContext('2d');
                window.propertyExpensesChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: [
                            'Utilities', 'Notary Taxes', 'Profit Tax', 'Municipal Taxes',
                            'Advertising', 'Administrative Fees', 'Insurance', 'Other Expenses',
                            'Bathroom Repair Expenses', 'Kitchen Repair Expenses', 'Floor Repair Expenses',
                            'Wall Repair Expenses', 'Window/Door Repair Expenses', 'Plumbing Repair Expenses',
                            'Electrical Repair Expenses', 'Roof Repair Expenses', 'Facade Repair Expenses',
                            'Other Repair Expenses'
                        ],
                        datasets: [{
                            label: 'Property Expenses',
                            data: [
                                data.utilities, data.notary_taxes, data.profit_tax, data.municipality_taxes,
                                data.advertising, data.administrative_fees, data.insurance, data.other_expenses,
                                data.bathroom_repair_expenses, data.kitchen_repair_expenses, data.floors_repair_expenses,
                                data.walls_repair_expenses, data.windows_doors_repair_expenses, data.plumbing_repair_expenses,
                                data.electrical_repair_expenses, data.roof_repair_expenses, data.facade_repair_expenses,
                                data.other_repair_expenses
                            ],
                            backgroundColor: [
                                'rgba(54, 162, 235, 0.6)',
                                'rgba(255, 99, 132, 0.6)',
                                'rgba(75, 192, 192, 0.6)',
                                'rgba(153, 102, 255, 0.6)',
                                'rgba(255, 159, 64, 0.6)',
                                'rgba(255, 206, 86, 0.6)',
                                'rgba(54, 162, 235, 0.6)',
                                'rgba(255, 99, 132, 0.6)',
                                'rgba(75, 192, 192, 0.6)',
                                'rgba(153, 102, 255, 0.6)',
                                'rgba(255, 159, 64, 0.6)',
                                'rgba(255, 206, 86, 0.6)',
                                'rgba(54, 162, 235, 0.6)',
                                'rgba(255, 99, 132, 0.6)',
                                'rgba(75, 192, 192, 0.6)',
                                'rgba(153, 102, 255, 0.6)',
                                'rgba(255, 159, 64, 0.6)'
                            ],
                            borderColor: [
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 99, 132, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 99, 132, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)',
                                'rgba(255, 206, 86, 1)',
                                'rgba(54, 162, 235, 1)',
                                'rgba(255, 99, 132, 1)',
                                'rgba(75, 192, 192, 1)',
                                'rgba(153, 102, 255, 1)',
                                'rgba(255, 159, 64, 1)'
                            ],
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
                        }
                    }
                });
            })
            .catch(error => console.error('Error loading chart:', error));
    }

    function applyDateFilter() {
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;

        if (startDate && endDate) {
            const apiUrl = `/properties/api-expenses/?start_date=${startDate}&end_date=${endDate}`;
            loadChart(apiUrl);
        } else {
            loadChart('/properties/api-expenses/');
        }
    }

    const filterButton = document.getElementById('filter-button');
    if (filterButton) {
        filterButton.addEventListener('click', applyDateFilter);
    }

    loadChart('/properties/api-expenses/');
});