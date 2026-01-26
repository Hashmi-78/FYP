// Load products from Django-injected json_script element (products-data)
const productsDataEl = document.getElementById('products-data');
let allProducts = [];
try {
  allProducts = productsDataEl ? JSON.parse(productsDataEl.textContent || '[]') : [];
} catch (e) {
  allProducts = [];
}

// Render Products
function renderProducts(products) {
  const grid = document.getElementById('products-grid');
  if (!grid) return; // Exit if element doesn't exist

  grid.innerHTML = products.map(p => `
    <div class="group bg-white rounded-2xl shadow-md overflow-hidden border hover:shadow-2xl transition-all duration-300">
      <div class="overflow-hidden">
        <img src="${p.image}" alt="${p.name}" class="w-full h-72 object-cover group-hover:scale-110 transition duration-500">
      </div>
      <div class="p-5">
        <h3 class="font-semibold text-gray-900 text-lg">${p.name}</h3>
        <div class="flex items-center gap-1 mt-2">
          ${'★'.repeat(Math.floor(p.rating))}<span class="text-gray-400 text-sm"> (${p.rating})</span>
        </div>
        <p class="text-2xl font-bold text-primary mt-3">PKR ${p.price.toLocaleString()}</p>
        <button class="mt-4 w-full bg-accent text-white py-3 rounded-xl hover:bg-red-700 transition font-medium">
          Add to Cart
        </button>
      </div>
    </div>
  `).join('');

  const resultCount = document.getElementById('result-count');
  if (resultCount) {
    resultCount.textContent = `${products.length} Products Found`;
  }
}

// Active Filters UI
function updateActiveFilters() {
  const checked = document.querySelectorAll('.filter-item:checked');
  const container = document.getElementById('active-filters');
  if (!container) return; // Exit if element doesn't exist

  container.innerHTML = '';

  checked.forEach(cb => {
    const label = cb.parentElement.cloneNode(true);
    label.querySelector('input').remove();
    const tag = document.createElement('span');
    tag.className = "px-4 py-2 bg-accent text-white rounded-full text-sm flex items-center gap-2";
    tag.innerHTML = label.innerHTML + `<i class="fas fa-times ml-2 cursor-pointer" onclick="this.parentElement.remove(); document.querySelector('[data-value=\\'${cb.dataset.value || ''}\\''][data-min=\\'${cb.dataset.min || ''}\\''][data-max=\\'${cb.dataset.max || ''}\\''])?.click()"></i>`;
    container.appendChild(tag);
  });
}

// Apply Filters
function applyFilters() {
  let filtered = allProducts;

  document.querySelectorAll('.filter-item:checked').forEach(cb => {
    if (cb.dataset.type === 'price') {
      const min = cb.dataset.min ? Number(cb.dataset.min) : 0;
      const max = cb.dataset.max ? Number(cb.dataset.max) : Infinity;
      filtered = filtered.filter(p => p.price >= min && p.price <= max);
    }
    if (cb.dataset.type === 'color') {
      filtered = filtered.filter(p => p.color === cb.dataset.value);
    }
    if (cb.dataset.type === 'rating') {
      filtered = filtered.filter(p => p.rating >= Number(cb.dataset.value));
    }
  });

  updateActiveFilters();
  renderProducts(filtered);
}

// Event Listeners
document.addEventListener('change', (e) => {
  if (e.target.classList.contains('filter-item')) applyFilters();
});

// Only attach event listeners if elements exist
const sortOptions = document.getElementById('sort-options');
if (sortOptions) {
  sortOptions.addEventListener('change', (e) => {
    let sorted = [...allProducts];
    switch (e.target.value) {
      case 'Price: Low to High': sorted.sort((a, b) => a.price - b.price); break;
      case 'Price: High to Low': sorted.sort((a, b) => b.price - a.price); break;
      case 'Latest': sorted.reverse(); break;
    }
    renderProducts(sorted);
  });
}

const clearAllBtn = document.getElementById('clear-all');
if (clearAllBtn) {
  clearAllBtn.addEventListener('click', () => {
    document.querySelectorAll('.filter-item').forEach(cb => cb.checked = false);
    applyFilters();
  });
}

// Initial Load - only if products grid exists
const productsGrid = document.getElementById('products-grid');
if (productsGrid) {
  renderProducts(allProducts);
}