// Resources JavaScript
document.addEventListener('DOMContentLoaded', function() {
    initializeInventoryTable();
});

function initializeInventoryTable() {
    // Add search/filter functionality
    const table = document.querySelector('.table');
    if (table) {
        console.log('Inventory table initialized');
    }
}

// Quantity update function with animation
function updateQuantityWithAnimation(id) {
    const row = document.querySelector(`button[onclick*="${id}"]`).closest('tr');
    if (row) {
        row.style.backgroundColor = '#fff3cd';
        setTimeout(function() {
            row.style.backgroundColor = '';
        }, 1000);
    }
}

// Export functions for use in templates
window.updateQuantity = function(id) {
    const newQuantity = prompt('Въведете ново количество:');
    if (newQuantity !== null && !isNaN(newQuantity) && parseInt(newQuantity) >= 0) {
        fetch('/resources/' + id + '/update-quantity', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({ quantity: parseInt(newQuantity) })
        }).then(function(response) {
            if (response.ok) {
                updateQuantityWithAnimation(id);
                location.reload();
            }
        });
    }
};

window.deleteResource = function(id) {
    if (confirm('Сигурни ли сте, че искате да изтриете този ресурс?')) {
        fetch('/resources/' + id + '/delete', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(function(response) {
            if (response.redirected) {
                window.location.href = response.url;
            }
        });
    }
};