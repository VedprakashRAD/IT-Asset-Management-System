/**
 * IT Asset Management System - Table Enhancements
 * Modern table functionality with sorting, filtering and responsive behavior
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all sortable tables
    initSortableTables();
    
    // Initialize all filterable tables
    initFilterableTables();
    
    // Add responsive behavior to tables
    makeTablesResponsive();
    
    // Apply dark mode specific styles to tables
    applyTableThemeStyles();
    
    // Listen for theme changes
    listenForThemeChanges();
});

/**
 * Initialize sortable tables
 */
function initSortableTables() {
    const sortableTables = document.querySelectorAll('table.sortable');
    
    sortableTables.forEach(table => {
        const headerCells = table.querySelectorAll('thead th[data-sort]');
        
        headerCells.forEach(th => {
            // Add sort indicator and click handler
            th.classList.add('sortable-header');
            th.innerHTML += '<span class="sort-icon ms-1"><i class="bi bi-arrow-down-up"></i></span>';
            
            th.addEventListener('click', function() {
                const sortDirection = this.getAttribute('data-sort-direction') === 'asc' ? 'desc' : 'asc';
                const columnIndex = Array.from(th.parentNode.children).indexOf(th);
                const sortType = this.getAttribute('data-sort');
                
                // Reset all headers
                headerCells.forEach(cell => {
                    cell.setAttribute('data-sort-direction', '');
                    cell.querySelector('.sort-icon').innerHTML = '<i class="bi bi-arrow-down-up"></i>';
                });
                
                // Set current header
                this.setAttribute('data-sort-direction', sortDirection);
                this.querySelector('.sort-icon').innerHTML = sortDirection === 'asc' 
                    ? '<i class="bi bi-arrow-up"></i>' 
                    : '<i class="bi bi-arrow-down"></i>';
                
                // Sort the table
                sortTable(table, columnIndex, sortDirection, sortType);
            });
        });
    });
}

/**
 * Sort table by column
 */
function sortTable(table, columnIndex, direction, sortType) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Sort rows
    rows.sort((a, b) => {
        const aValue = getCellValue(a, columnIndex, sortType);
        const bValue = getCellValue(b, columnIndex, sortType);
        
        if (direction === 'asc') {
            return aValue > bValue ? 1 : -1;
        } else {
            return aValue < bValue ? 1 : -1;
        }
    });
    
    // Re-append rows in sorted order
    rows.forEach(row => tbody.appendChild(row));
}

/**
 * Get cell value for sorting
 */
function getCellValue(row, columnIndex, sortType) {
    const cell = row.cells[columnIndex];
    let value = cell.textContent.trim();
    
    // Convert value based on sort type
    switch (sortType) {
        case 'number':
            return parseFloat(value) || 0;
        case 'date':
            return new Date(value).getTime() || 0;
        default:
            return value.toLowerCase();
    }
}

/**
 * Initialize filterable tables
 */
function initFilterableTables() {
    const filterableTables = document.querySelectorAll('.table-filterable');
    
    filterableTables.forEach(tableContainer => {
        const table = tableContainer.querySelector('table');
        const filterInput = document.createElement('input');
        
        // Create filter input
        filterInput.type = 'text';
        filterInput.className = 'form-control form-control-sm mb-2';
        filterInput.placeholder = 'Search...';
        tableContainer.insertBefore(filterInput, table);
        
        // Add filter functionality
        filterInput.addEventListener('input', function() {
            const filterValue = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filterValue) ? '' : 'none';
            });
        });
    });
}

/**
 * Make tables responsive
 */
function makeTablesResponsive() {
    const tables = document.querySelectorAll('table:not(.table-responsive)');
    
    tables.forEach(table => {
        // Check if table is not already in a responsive wrapper
        if (!table.parentElement.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
}

/**
 * Apply theme-specific styles to tables
 */
function applyTableThemeStyles() {
    const isDarkMode = document.body.classList.contains('dark-theme');
    const tables = document.querySelectorAll('table');
    
    tables.forEach(table => {
        if (isDarkMode) {
            table.classList.add('table-dark');
        } else {
            table.classList.remove('table-dark');
        }
    });
}

/**
 * Listen for theme changes to update table styles
 */
function listenForThemeChanges() {
    // Create a mutation observer to watch for class changes on the body element
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.attributeName === 'class') {
                applyTableThemeStyles();
            }
        });
    });
    
    // Start observing
    observer.observe(document.body, { attributes: true });
    
    // Also listen for theme toggle button clicks
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            // Small delay to ensure the class has been toggled
            setTimeout(applyTableThemeStyles, 50);
        });
    }
}

/**
 * Add row highlighting on hover
 */
document.addEventListener('mouseover', function(e) {
    if (e.target.tagName === 'TD') {
        e.target.parentElement.classList.add('row-highlight');
    }
}, true);

document.addEventListener('mouseout', function(e) {
    if (e.target.tagName === 'TD') {
        e.target.parentElement.classList.remove('row-highlight');
    }
}, true);

/**
 * Add CSS for table enhancements
 */
(function addTableStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .sortable-header {
            cursor: pointer;
            user-select: none;
        }
        
        .sortable-header:hover {
            background-color: var(--hover-bg);
        }
        
        .sort-icon {
            opacity: 0.6;
        }
        
        .row-highlight {
            background-color: var(--hover-bg) !important;
        }
        
        /* Dark mode specific styles */
        body.dark-theme .table {
            color: var(--text);
            background-color: var(--bg-secondary);
            border-color: var(--table-border);
        }
        
        body.dark-theme .table th {
            background-color: var(--table-header);
            color: var(--text);
            border-color: var(--table-border);
        }
        
        body.dark-theme .table td {
            color: var(--text);
            border-color: var(--table-border);
        }
        
        body.dark-theme .table tbody tr:nth-child(even) {
            background-color: var(--table-stripe);
        }
        
        body.dark-theme .table tbody tr:nth-child(odd) {
            background-color: var(--bg-secondary);
        }
        
        body.dark-theme .table-responsive {
            background-color: var(--bg-secondary);
        }
        
        @media (max-width: 768px) {
            .table-responsive {
                border-radius: 0.5rem;
                border: 1px solid var(--border);
            }
            
            .table-responsive table {
                border: none;
            }
        }
    `;
    document.head.appendChild(style);
})(); 