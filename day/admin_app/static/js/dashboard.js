document.addEventListener('DOMContentLoaded', function() {
    const table = document.getElementById('eventTable');
    const rows = table.getElementsByTagName('tbody')[0].rows;
    const rowsPerPage = 10;
    const pageCount = Math.ceil(rows.length / rowsPerPage);
    const pagination = document.querySelector('.pagination');

    // Hide all rows initially
    for (let i = 0; i < rows.length; i++) {
        rows[i].style.display = 'none';
    }

    // Show first page by default
    function showPage(page) {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        for (let i = 0; i < rows.length; i++) {
            if (i >= start && i < end) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }

        // Update active page
        const pageLinks = pagination.querySelectorAll('.page-item');
        pageLinks.forEach(link => link.classList.remove('active'));
        pageLinks[page].classList.add('active');
    }

    // Create pagination links dynamically
    function createPaginationLinks() {
        const prevLink = pagination.querySelector('.page-item:first-child');
        const nextLink = pagination.querySelector('.page-item:last-child');

        // Clear existing page links
        const existingLinks = pagination.querySelectorAll('.page-item:not(:first-child):not(:last-child)');
        existingLinks.forEach(link => link.remove());

        // Add page number links
        for (let i = 1; i <= pageCount; i++) {
            const li = document.createElement('li');
            li.classList.add('page-item');
            const a = document.createElement('a');
            a.classList.add('page-link');
            a.href = '#';
            a.textContent = i;
            a.addEventListener('click', function(e) {
                e.preventDefault();
                showPage(i);
            });
            li.appendChild(a);
            nextLink.before(li);
        }

        // Manage previous and next links
        prevLink.classList.toggle('disabled', pageCount <= 1);
        nextLink.classList.toggle('disabled', pageCount <= 1);

        // Previous page handler
        prevLink.querySelector('.page-link').addEventListener('click', function(e) {
            e.preventDefault();
            const currentPage = pagination.querySelector('.page-item.active').textContent;
            if (currentPage > 1) {
                showPage(parseInt(currentPage) - 1);
            }
        });

        // Next page handler
        nextLink.querySelector('.page-link').addEventListener('click', function(e) {
            e.preventDefault();
            const currentPage = pagination.querySelector('.page-item.active').textContent;
            if (currentPage < pageCount) {
                showPage(parseInt(currentPage) + 1);
            }
        });
    }

    // Initialize
    if (rows.length > 0) {
        createPaginationLinks();
        showPage(1);
    }
});


// Function to show table
function table() {
    document.getElementById('table').style.display = 'block';
    document.getElementById('chart').style.display = 'none';
}

// Function to show chart
function chart() {
    document.getElementById('table').style.display = 'none';
    document.getElementById('chart').style.display = 'block';
}

// Ensure table is shown by default when page loads
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('chart').style.display = 'none';
});



function data() {
    document.getElementById('data').style.display = 'block';
    document.getElementById('data1').style.display = 'none';

}