window.onload = function() {
    const ctx2 = document.getElementById('pieChart').getContext('2d');
    new Chart(ctx2, {
        type: 'pie',
        data: {
            labels: ['A', 'B', 'C', 'D'],
            datasets: [{
                label: 'Pie Chart Data',
                backgroundColor: ['green', 'blue', 'red', 'yellow'],
                data: [12, 19, 3, 5]
            }]
        }
    });
};
