// css/dashboard.css
/* globals Chart:false, feather:false */
(() => {
    'use strict';

    feather.replace({'aria-hidden': 'true'});

    // Graphs
    const ctx = document.getElementById('myChart');
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],  // This will be set dynamically based on the investment period
            datasets: [
                {
                    label: '초기 투자 금액',
                    data: [],
                    backgroundColor: 'rgba(0, 123, 255, 0.5)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 2,
                    stack: 'stacked',  // Same stack group
                },
                {
                    label: '추가 투자금',
                    data: [],
                    backgroundColor: 'rgba(255, 193, 7, 0.5)',
                    borderColor: 'rgba(255, 193, 7, 1)',
                    borderWidth: 2,
                    stack: 'stacked',  // Same stack group
                },
                {
                    label: '누적 수익',
                    data: [],
                    backgroundColor: 'rgba(40, 167, 69, 0.5)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 2,
                    stack: 'stacked',  // Same stack group
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    mode: 'index',  // Show tooltips for all datasets at the same time
                    intersect: false,  // Ensure hovering over any point shows all tooltips
                    callbacks: {
                        // Reverse the order of the tooltips so that the bottom-most stack shows first
                        label: function(tooltipItem) {
                            let value = tooltipItem.raw;  // Access raw data value
                            return tooltipItem.dataset.label + ': ' + value.toLocaleString() + ' 만원';
                        },
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    stacked: true,  // Enable stacked bars for y-axis
                    title: {
                        display: true,
                        text: '금액 (만원)'
                    }
                },
                x: {
                    stacked: true,  // Enable stacked bars for x-axis
                    title: {
                        display: true,
                        text: '년도'
                    }
                }
            }
        }
    });

    // Export the chart instance
    window.myChart = myChart;

})();