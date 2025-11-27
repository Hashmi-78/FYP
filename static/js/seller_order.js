let orders = [
  {
    id: "ORD-1001",
    customer: { name: "Ahmad Khan", phone: "03001234567", email: "ahmad@gmail.com", address: "House 123, Street 5, Gulberg III, Lahore" },
    items: [
      { title: "iPhone 15 Pro", qty: 1, price: 399999 },
      { title: "AirPods Pro", qty: 2, price: 64999 }
    ],
    total: 529997,
    status: "pending",
    date: "2025-11-19"
  },
  {
    id: "ORD-1002",
    customer: { name: "Sara Ali", phone: "03331234567", email: "sara@yahoo.com", address: "Flat A-12, DHA Phase 6, Karachi" },
    items: [{ title: "MacBook Air M2", qty: 1, price: 389999 }],
    total: 389999,
    status: "processing",
    date: "2025-11-18"
  },
  {
    id: "ORD-1003",
    customer: { name: "Usman Butt", phone: "03219876543", email: "usman@outlook.com", address: "Plot 45, Bahria Town, Islamabad" },
    items: [{ title: "Sony WH-1000XM5", qty: 1, price: 89999 }],
    total: 89999,
    status: "shipped",
    date: "2025-11-17"
  }
];

let currentOrder = null;

function renderOrders() {
  const container = document.getElementById('ordersContainer');
  container.innerHTML = '';

  const counts = { pending: 0, processing: 0, shipped: 0, completed: 0 };

  orders.forEach(order => {
    counts[order.status]++;

    const statusColor = {
      pending: 'bg-orange-100 text-orange-700',
      processing: 'bg-blue-100 text-blue-700',
      shipped: 'bg-purple-100 text-purple-700',
      completed: 'bg-green-100 text-green-700'
    }[order.status];

    const card = document.createElement('div');
    card.className = 'bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition cursor-pointer';
    card.onclick = () => openOrderModal(order);

    card.innerHTML = `
      <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h3 class="text-xl font-bold text-blue-900">#${order.id}</h3>
          <p class="text-gray-600">${order.customer.name} • ${order.date}</p>
          <p class="text-sm text-gray-500 mt-1">${order.items.length} item(s)</p>
        </div>
        <div class="text-right">
          <p class="text-2xl font-bold text-blue-900">₨${order.total.toLocaleString()}</p>
          <span class="inline-block mt-2 px-5 py-2 rounded-full font-bold text-sm ${statusColor}">
            ${order.status.toUpperCase()}
          </span>
        </div>
      </div>
    `;
    container.appendChild(card);
  });

  // Update counters
  document.getElementById('pendingCount').textContent = counts.pending;
  document.getElementById('processingCount').textContent = counts.processing;
  document.getElementById('shippedCount').textContent = counts.shipped;
  document.getElementById('completedCount').textContent = counts.completed;
}

function openOrderModal(order) {
  currentOrder = order;
  document.getElementById('cName').textContent = order.customer.name;
  document.getElementById('cPhone').textContent = order.customer.phone;
  document.getElementById('cEmail').textContent = order.customer.email;
  document.getElementById('cAddress').textContent = order.customer.address;
  document.getElementById('totalAmount').textContent = '₨' + order.total.toLocaleString();
  document.getElementById('statusSelect').value = order.status;

  const itemsDiv = document.getElementById('orderItems');
  itemsDiv.innerHTML = '';
  order.items.forEach(item => {
    const div = document.createElement('div');
    div.className = 'flex justify-between py-2 border-b';
    div.innerHTML = `<span>${item.title} × ${item.qty}</span><span>₨${(item.price * item.qty).toLocaleString()}</span>`;
    itemsDiv.appendChild(div);
  });

  document.getElementById('orderModal').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('orderModal').classList.add('hidden');
}

function updateStatus() {
  if (!currentOrder) return;
  const newStatus = document.getElementById('statusSelect').value;
  currentOrder.status = newStatus;
  closeModal();
  renderOrders();
  alert("Order status updated!");
}

function openChat() {
  document.getElementById('chatName').textContent = currentOrder.customer.name;
  document.getElementById('chatMessages').innerHTML = '<p class="text-gray-500 text-center">Start chatting...</p>';
  document.getElementById('chatBox').classList.remove('hidden');
  closeModal();
}

function closeChat() {
  document.getElementById('chatBox').classList.add('hidden');
}

function sendMessage() {
  const input = document.getElementById('msgInput');
  if (!input.value.trim()) return;

  const msg = document.createElement('div');
  msg.className = 'bg-blue-900 text-white p-3 rounded-lg max-w-xs ml-auto mb-3';
  msg.textContent = input.value;
  document.getElementById('chatMessages').appendChild(msg);
  document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
  input.value = '';
}

// Start
renderOrders();