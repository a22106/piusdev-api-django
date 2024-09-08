// js/slider.js
/* globals Chart:false, feather:false */

document.addEventListener('DOMContentLoaded', function () {
    const sliders = [
        {id: 'initial-balance', unit: '만원', max: 100000},
        {id: 'monthly-save', unit: '만원', max: 500},
        {id: 'annual-interest', unit: '%', max: 20},
        {id: 'investment-period', unit: '년', max: 50}
    ];

    /**
     * @param initialBalance 초기 투자금
     * @param monthlySave 월 별 추가 투자금
     * @param annualInterest 연간 이자율
     * @param year 투자 기간
     * @returns {*}
     */
    function yearlyBalance(initialBalance, monthlySave, annualInterest, years) {
        let monthlyInterestRate = annualInterest / 12; // 월 수익률
        let totalBalance = initialBalance; // 초기 잔액으로 시작
        let totalDeposits = initialBalance;
        let yearlyBreakdown = [{
            year: 0,
            deposits: initialBalance,
            interest: 0,
            totalDeposits: initialBalance,
            accruedInterest: 0,
            balance: initialBalance,
            initialBalance: initialBalance
        }];
        let totalInterest = 0;

        for (let month = 1; month <= years * 12; month++) {
            // Calculate interest for the current month
            let interest = totalBalance * monthlyInterestRate;
            totalBalance += interest + monthlySave;
            totalDeposits += monthlySave;
            totalInterest += interest;

            // Push yearly results (only at the end of each year)
            if (month % 12 === 0) {
                let year = month / 12;
                yearlyBreakdown.push({
                    year: year,
                    deposits: monthlySave * 12,
                    interest: totalInterest.toFixed(2),
                    totalDeposits: totalDeposits,
                    accruedInterest: totalInterest.toFixed(2),
                    balance: totalBalance.toFixed(2),
                    initialBalance: initialBalance
                });
                totalInterest = 0; // Reset yearly interest accumulator
            }
        }

        return yearlyBreakdown;
    }

    function updateTable(yearlyBreakdown) {
        const tableBody = document.querySelector('tbody');
        tableBody.innerHTML = ''; // Clear previous data

        yearlyBreakdown.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
            <td>${row.year}</td>
            <td>${row.deposits} 만원</td>
            <td>${row.interest} 만원</td>
            <td>${row.totalDeposits} 만원</td>
            <td>${row.accruedInterest} 만원</td>
            <td>${row.balance} 만원</td>
        `;
            tableBody.appendChild(tr);
        });
    }

    function updateChart() {
        const initialBalance = parseInt(document.getElementById('initial-balance').value);
        const monthlySave = parseInt(document.getElementById('monthly-save').value);
        const annualInterest = parseFloat(document.getElementById('annual-interest').value) / 100;
        const investmentPeriod = parseInt(document.getElementById('investment-period').value);

        const labels = Array.from({ length: investmentPeriod+1 }, (_, i) => i);

        const yearlyBalances = yearlyBalance(initialBalance, monthlySave, annualInterest, investmentPeriod);

        // Update chart
        window.myChart.data.labels = labels;
        window.myChart.data.datasets[0].data = yearlyBalances.map(entry => entry.initialBalance);
        window.myChart.data.datasets[1].data = yearlyBalances.map(entry => entry.totalDeposits - entry.initialBalance);
        window.myChart.data.datasets[2].data = yearlyBalances.map(entry => entry.interest);
        window.myChart.update();

        // Update table with breakdown
        updateTable(yearlyBalances);
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