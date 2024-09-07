// js/slider.js
/* globals Chart:false, feather:false */

document.addEventListener('DOMContentLoaded', function() {
    const sliders = [
        { id: 'initial-balance', unit: '만원', max: 100000 },
        { id: 'monthly-save', unit: '만원', max: 500 },
        { id: 'annual-interest', unit: '%', max: 20 },
        { id: 'investment-period', unit: '년', max: 50 }
    ];

    function updateChart() {
        const initialBalance = parseInt(document.getElementById('initial-balance').value);
        const monthlySave = parseInt(document.getElementById('monthly-save').value);
        const annualInterest = parseFloat(document.getElementById('annual-interest').value) / 100;
        const investmentPeriod = parseInt(document.getElementById('investment-period').value);

        const labels = Array.from({length: investmentPeriod}, (_, i) => i + 1);
        const data = [];

        let balance = initialBalance;
        for (let year = 0; year <= investmentPeriod; year++) {
            data.push(Math.round(balance));
            balance = balance * (1 + annualInterest) + monthlySave * 12;
        }

        window.myChart.data.labels = labels;
        window.myChart.data.datasets[0].data = data;
        window.myChart.update();
    }

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
            updateChart();
        }

        input.addEventListener('input', updateSliderValue);
        updateSliderValue(); // Initialize the display
    });

    // Initial chart update
    updateChart();
});