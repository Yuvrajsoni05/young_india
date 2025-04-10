const ctx1 = document.getElementById('lineBarChart').getContext('2d');
new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
        datasets: [
            {
                type: 'line',
                label: 'Line Data',
                borderColor: 'blue',
                borderWidth: 2,
                fill: false,
                data: [10, 20, 30, 40, 50]
            },
            {
                type: 'bar',
                label: 'Bar Data',
                backgroundColor: 'red',
                data: [15, 25, 35, 45, 55]
            }
        ]
    }
});
