const ctx2 = document.getElementById('barChart').getContext('2d');
new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['A', 'B', 'C', 'D'],
        datasets: [{
            label: 'Bar Chart Data',
            backgroundColor: 'green',
            data: [12, 19, 3, 5]
        }]
    }
});
