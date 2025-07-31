 // Sample data
    let portfolioData = {
        performance: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            values: [110000, 112000, 108000, 115000, 118000, 120000, 122000, 119000, 123000, 125000, 124000, 125847]
        },
        allocation: {
            labels: ['Stocks', 'Bonds', 'Cash'],
            values: [85000, 28447, 12450],
            colors: ['#4285f4', '#6fa8f7', '#a3c4f9']
        },
        holdings: [],
        searchResults: [
            { symbol: 'META', name: 'Meta Platforms Inc.', price: 285.50, change: '+2.5%' },
            { symbol: 'NFLX', name: 'Netflix Inc.', price: 485.20, change: '-1.2%' },
            { symbol: 'CRM', name: 'Salesforce Inc.', price: 220.75, change: '+0.8%' },
            { symbol: 'ADBE', name: 'Adobe Inc.', price: 380.90, change: '+1.5%' },
            { symbol: 'PYPL', name: 'PayPal Holdings Inc.', price: 95.30, change: '-0.5%' },
            { symbol: 'NVDA', name: 'NVIDIA Corp.', price: 450.80, change: '+1.5%' },
            { symbol: 'TSLA', name: 'Tesla Inc.', price: 180.45, change: '-0.5%' },
            { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 95.30, change: '-0.5%' },
            { symbol: 'AAPL', name: 'Apple Inc.', price: 175.50, change: '+1.2%' },
            { symbol: 'MSFT', name: 'Microsoft Corp.', price: 320.75, change: '+0.8%' },
            { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 145.20, change: '+0.3%' },
            { symbol: 'INTC', name: 'Intel Corp.', price: 45.80, change: '-1.1%' },
            { symbol: 'AMD', name: 'Advanced Micro Devices', price: 120.45, change: '+2.1%' },
            { symbol: 'ORCL', name: 'Oracle Corp.', price: 85.30, change: '+0.7%' },
            { symbol: 'IBM', name: 'International Business Machines', price: 165.20, change: '-0.4%' }
        ]
    };

    async function fetchPortfolioData() {
    try {
        const response = await fetch("http://127.0.0.1:5000/portfolio");
        if (!response.ok) {
            throw new Error("Failed to fetch portfolio data");
        }

        const data = await response.json();
        console.log(data)
        // // Update the global holdings with live backend data
        portfolioData.holdings = data;
        console.log(portfolioData.holdings)
        filteredHoldings = [...portfolioData.holdings];

        populateHoldingsTable();
    } catch (error) {
        console.error("Error fetching portfolio data:", error);
    }
}


    // Pagination variables for search table
    let currentPage = 1;
    const recordsPerPage = 6;
    let filteredResults = [...portfolioData.searchResults];

    // Pagination variables for holdings table
    let holdingsCurrentPage = 1;
    let filteredHoldings = [...portfolioData.holdings];

    // Initialize charts
    function initializeCharts() {
        // Performance Chart
        const performanceCtx = document.getElementById('performanceChart').getContext('2d');
        new Chart(performanceCtx, {
            type: 'line',
            data: {
                labels: portfolioData.performance.labels,
                datasets: [{
                    label: 'Portfolio Value',
                    data: portfolioData.performance.values,
                    borderColor: '#4285f4',
                    backgroundColor: 'rgba(66, 133, 244, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#999999'
                        }
                    },
                    y: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        ticks: {
                            color: '#999999',
                            callback: function(value) {
                                return '$' + (value / 1000) + 'k';
                            }
                        }
                    }
                }
            }
        });

        // Allocation Chart
        const allocationCtx = document.getElementById('allocationChart').getContext('2d');
        new Chart(allocationCtx, {
            type: 'doughnut',
            data: {
                labels: portfolioData.allocation.labels,
                datasets: [{
                    data: portfolioData.allocation.values,
                    backgroundColor: portfolioData.allocation.colors,
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#cccccc',
                            padding: 20
                        }
                    }
                }
            }
        });
    }

    // Populate holdings table with pagination
    function populateHoldingsTable() {
        const tbody = document.getElementById('holdingsTableBody');
        tbody.innerHTML = '';

        const paginatedHoldings = getPaginatedData(filteredHoldings, holdingsCurrentPage, recordsPerPage - 1);

    paginatedHoldings.forEach(holding => {
    let symbol = holding.ticker;
    let avgPrice = Number(holding.avg_price);
    let quantity = Number(holding.total_quantity);
    let currentValue=Number(holding.current_value);
    console.log(holding.current_value)
    let totalCost = quantity * avgPrice;
    let gainLoss = currentValue - totalCost;
    let gainLossPercent = (gainLoss / totalCost * 100).toFixed(2);
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${symbol}</td>
        <td>${quantity}</td>
        <td>$${avgPrice.toFixed(2)}</td>
        <td>$${currentValue.toFixed(2)}</td>
        <td class="${gainLoss >= 0 ? 'trend-positive' : 'trend-negative'}">
                    ${gainLoss >= 0 ? '+' : ''}$${gainLoss.toFixed(2)} (${gainLossPercent}%)
        </td>
        <td>
            <button class="btn btn-danger btn-sm" onclick="sellStock('${symbol}')">Sell</button>
        </td>
    `;
    tbody.appendChild(row);
});


    updateHoldingsPaginationControls();
}

    // Get paginated data
    function getPaginatedData(data, page, recordsPerPage) {
        const startIndex = (page - 1) * recordsPerPage;
        const endIndex = startIndex + recordsPerPage;
        return data.slice(startIndex, endIndex);
    }

    // Update pagination controls
    function updatePaginationControls() {
        const totalPages = Math.ceil(filteredResults.length / recordsPerPage);
        let paginationContainer = document.getElementById('searchPagination');
        
        if (!paginationContainer) {
            // Create pagination container if it doesn't exist
            const searchTableContainer = document.querySelector('.tables-section .table-container:first-child');
            const paginationDiv = document.createElement('div');
            paginationDiv.id = 'searchPagination';
            paginationDiv.className = 'pagination-controls';
            searchTableContainer.appendChild(paginationDiv);
            paginationContainer = document.getElementById('searchPagination');
        }

        paginationContainer.innerHTML = '';

        if (totalPages <= 1) {
            return; // Don't show pagination if only one page
        }

        // Previous button
        const prevBtn = document.createElement('button');
        prevBtn.className = 'btn btn-secondary pagination-btn';
        prevBtn.innerHTML = '← Previous';
        prevBtn.disabled = currentPage === 1;
        prevBtn.onclick = () => {
            if (currentPage > 1) {
                currentPage--;
                populateSearchTable();
                updatePaginationControls();
            }
        };
        paginationContainer.appendChild(prevBtn);

        // Page info
        const pageInfo = document.createElement('span');
        pageInfo.className = 'pagination-info';
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
        paginationContainer.appendChild(pageInfo);

        // Next button
        const nextBtn = document.createElement('button');
        nextBtn.className = 'btn btn-secondary pagination-btn';
        nextBtn.innerHTML = 'Next →';
        nextBtn.disabled = currentPage === totalPages;
        nextBtn.onclick = () => {
            if (currentPage < totalPages) {
                currentPage++;
                populateSearchTable();
                updatePaginationControls();
            }
        };
        paginationContainer.appendChild(nextBtn);
    }

    // Populate search table with pagination
    function populateSearchTable() {
        const tbody = document.getElementById('searchTableBody');
        tbody.innerHTML = '';

        const paginatedData = getPaginatedData(filteredResults, currentPage, recordsPerPage);

        paginatedData.forEach(stock => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><strong>${stock.symbol}</strong></td>
                <td>${stock.name}</td>
                <td>$${stock.price.toFixed(2)}</td>
                <td class="${stock.change.startsWith('+') ? 'trend-positive' : 'trend-negative'}">
                    ${stock.change}
                </td>
                <td>
                    <button class="btn btn-primary" onclick="addStock('${stock.symbol}')">Add</button>
                </td>
            `;
            tbody.appendChild(row);
        });

        updatePaginationControls();
    }

    // Update holdings pagination controls
    function updateHoldingsPaginationControls() {
        const totalPages = Math.ceil(filteredHoldings.length / recordsPerPage);
        let paginationContainer = document.getElementById('holdingsPagination');
        
        if (!paginationContainer) {
            // Create pagination container if it doesn't exist
            const holdingsTableContainer = document.querySelector('.tables-section .table-container:last-child');
            const paginationDiv = document.createElement('div');
            paginationDiv.id = 'holdingsPagination';
            paginationDiv.className = 'pagination-controls';
            holdingsTableContainer.appendChild(paginationDiv);
            paginationContainer = document.getElementById('holdingsPagination');
        }

        paginationContainer.innerHTML = '';

        if (totalPages <= 1) {
            return; // Don't show pagination if only one page
        }

        // Previous button
        const prevBtn = document.createElement('button');
        prevBtn.className = 'btn btn-secondary pagination-btn';
        prevBtn.innerHTML = '← Previous';
        prevBtn.disabled = holdingsCurrentPage === 1;
        prevBtn.onclick = () => {
            if (holdingsCurrentPage > 1) {
                holdingsCurrentPage--;
                populateHoldingsTable();
                updateHoldingsPaginationControls();
            }
        };
        paginationContainer.appendChild(prevBtn);

        // Page info
        const pageInfo = document.createElement('span');
        pageInfo.className = 'pagination-info';
        pageInfo.textContent = `Page ${holdingsCurrentPage} of ${totalPages}`;
        paginationContainer.appendChild(pageInfo);

        // Next button
        const nextBtn = document.createElement('button');
        nextBtn.className = 'btn btn-secondary pagination-btn';
        nextBtn.innerHTML = 'Next →';
        nextBtn.disabled = holdingsCurrentPage === totalPages;
        nextBtn.onclick = () => {
            if (holdingsCurrentPage < totalPages) {
                holdingsCurrentPage++;
                populateHoldingsTable();
                updateHoldingsPaginationControls();
            }
        };
        paginationContainer.appendChild(nextBtn);
    }

    // Search functionality with pagination
    function setupSearch() {
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            
            // Filter results based on search term
            filteredResults = portfolioData.searchResults.filter(stock => 
                stock.symbol.toLowerCase().includes(searchTerm) || 
                stock.name.toLowerCase().includes(searchTerm)
            );
            
            // Reset to first page when searching
            currentPage = 1;
            
            // Repopulate table with filtered results
            populateSearchTable();
        });
    }

    // Action functions
    function addStock(symbol) {
        const stock = portfolioData.searchResults.find(s => s.symbol === symbol);
        if (!stock) {
            alert("Stock data not found.");
            return;
        }

        document.getElementById('buySymbol').value = stock.symbol;
        document.getElementById('buyPrice').value = stock.price.toFixed(2);
        document.getElementById('buyQuantity').value = '';
        document.getElementById('buyDate').value = new Date().toISOString().split('T')[0];

        const modal = new bootstrap.Modal(document.getElementById('buyStockModal'));
        modal.show();
    }


    function sellStock(symbol) {
        if (confirm(`Are you sure you want to sell ${symbol}?`)) {
            alert(`Sold ${symbol}!`);
            // In a real application, this would make an API call to sell the stock
        }
    }

    // Initialize the dashboard
    document.addEventListener('DOMContentLoaded', function () {
        initializeCharts();
        fetchPortfolioData();
        populateSearchTable();
        setupSearch();

        // Handle the Buy Stock form submission
        document.getElementById('buyStockForm').addEventListener('submit', async function (event) {
            event.preventDefault();

            const symbol = document.getElementById('buySymbol').value;
            const quantity = Number(document.getElementById('buyQuantity').value);
            const price = Number(document.getElementById('buyPrice').value);
            const date = document.getElementById('buyDate').value;

            const purchaseData = {
                ticker: symbol,
                quantity: quantity,
                asset_type: 'equity',
                purchase_price : price,
                purchase_date: date
            };

            try {
                console.log("Sending this to backend:", purchaseData);
                const response = await fetch('http://127.0.0.1:5000/portfolio', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(purchaseData)
                });

                if (!response.ok) throw new Error('Failed to add stock');

                alert('Stock added successfully!');
                fetchPortfolioData(); // Refresh table
            } catch (error) {
                console.error('Error adding stock:', error);
                alert('Error adding stock. Please try again.');
            }

            // Close the modal after submission
            const modalEl = document.getElementById('buyStockModal');
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
        });
});
