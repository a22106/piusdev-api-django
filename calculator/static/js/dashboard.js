/* globals Chart:false, feather:false */

(() => {
    'use strict'

    feather.replace({'aria-hidden': 'true'})

    // Graphs
    const ctx = document.getElementById('myChart')
    // eslint-disable-next-line no-unused-vars
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [
                'Sunday',
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday'
            ],
            datasets: [{
                data: [
                    15339,
                    21345,
                    18483,
                    24003,
                    23489,
                    24092,
                    12034
                ],
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#007bff',
                borderWidth: 4,
                pointBackgroundColor: '#007bff'
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
            },
            legend: {
                display: false
            }
        }
    })
})()

document.addEventListener('DOMContentLoaded', function() {
    const sliders = [
        { id: 'initial-balance', unit: '만원', max: 100000 },
        { id: 'monthly-save', unit: '만원', max: 500 },
        { id: 'annual-interest', unit: '%', max: 20 },
        { id: 'investment-period', unit: '년', max: 50 }
    ];

    sliders.forEach(slider => {
        const input = document.getElementById(slider.id);
        const valueDisplay = document.getElementById(`${slider.id}-value`);

        function updateSliderValue() {
            let value = input.value;
            let displayText = `${value}${slider.unit}`;

            if (slider.id === 'annual-interest') {
                value = parseFloat(value).toFixed(1);
                displayText = `${value}${slider.unit}`;
            }

            valueDisplay.textContent = displayText;
        }

        input.addEventListener('input', updateSliderValue);
        updateSliderValue(); // Initialize the display
    });
});