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