// Dummy Data
const dailyData = {
  labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
  values: [42000, 58000, 65000, 48000, 92000, 110000, 85000]
};

const monthlyData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  values: [180000, 220000, 195000, 280000, 320000, 410000, 385000, 420000, 398000, 450000, 520000, 485000]
};

const topProducts = [
  { name: "iPhone 15 Pro", sold: 342, revenue: 485000 },
  { name: "Samsung S24 Ultra", sold: 298, revenue: 398000 },
  { name: "MacBook Air M3", sold: 189, revenue: 285000 },
  { name: "AirPods Pro 2", sold: 412, revenue: 168000 },
  { name: "Sony WH-1000XM5", sold: 267, revenue: 142000 }
];

// Daily Chart
new Chart(document.getElementById('dailyChart'), {
  type: 'line',
  data: {
    labels: dailyData.labels,
    datasets: [{
      label: 'Daily Sales (₨)',
      data: dailyData.values,
      borderColor: '#1e40af',
      backgroundColor: 'rgba(30, 64, 175, 0.1)',
      tension: 0.4,
      fill: true,
      pointBackgroundColor: '#1e40af',
      pointRadius: 5
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } }
  }
});

// Monthly Chart
new Chart(document.getElementById('monthlyChart'), {
  type: 'bar',
  data: {
    labels: monthlyData.labels,
    datasets: [{
      label: 'Monthly Revenue (₨)',
      data: monthlyData.values,
      backgroundColor: '#1e40af',
      borderRadius: 8
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } }
  }
});

// Top Products
const topDiv = document.getElementById('topProducts');
topProducts.forEach((p, i) => {
  const div = document.createElement('div');
  div.className = 'flex items-center justify-between p-3 bg-gray-50 rounded-lg border';
  div.innerHTML = `
    <div class="flex items-center gap-3">
      <span class="text-2xl font-bold text-blue-900">${i+1}</span>
      <div>
        <p class="font-bold text-gray-800">${p.name}</p>
        <p class="text-xs text-gray-600">${p.sold} units sold</p>
      </div>
    </div>
    <p class="font-bold text-blue-900">₨${p.revenue.toLocaleString()}</p>
  `;
  topDiv.appendChild(div);
});