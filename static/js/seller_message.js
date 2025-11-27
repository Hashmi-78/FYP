let conversations = [
  {
    customer: { id: 1, name: "Ahmad Khan", avatar: "A", lastMsg: "Bhai kab tak deliver hoga?", time: "2 min ago", unread: 3 },
    messages: [
      { text: "Salam bhai, order confirm kar diya hai", sender: "seller", time: "10:30 AM" },
      { text: "Walaikum salam! Kab tak deliver hoga?", sender: "customer", time: "10:32 AM" },
      { text: "Kal tak InshaAllah pahunch jayega", sender: "seller", time: "10:33 AM" },
      { text: "Shukriya bhai", sender: "customer", time: "10:35 AM" }
    ]
  },
  {
    customer: { id: 2, name: "Sara Ali", avatar: "S", lastMsg: "Size available hai?", time: "1 hour ago", unread: 1 },
    messages: [
      { text: "Yes ma'am, Medium aur Large dono available hain", sender: "seller", time: "09:15 AM" },
      { text: "Thanks! Large bhej den", sender: "customer", time: "09:20 AM" }
    ]
  },
  {
    customer: { id: 3, name: "Usman Butt", avatar: "U", lastMsg: "You: Payment received, shipping today", time: "Yesterday", unread: 0 },
    messages: [
      { text: "Payment received, shipping today", sender: "seller", time: "Yesterday" }
    ]
  }
];

let currentCustomer = null;

function renderConversations() {
  const list = document.getElementById('conversationsList');
  list.innerHTML = '';

  let totalUnread = 0;

  conversations.forEach(conv => {
    totalUnread += conv.customer.unread;

    const item = document.createElement('div');
    item.className = `p-4 border-b hover:bg-gray-50 cursor-pointer transition ${conv.customer.unread > 0 ? 'bg-blue-50' : ''}`;
    item.onclick = () => openChat(conv);

    item.innerHTML = `
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-blue-900 text-white rounded-full flex items-center justify-center font-bold text-lg">
            ${conv.customer.avatar}
          </div>
          <div>
            <h4 class="font-bold text-gray-800">${conv.customer.name}</h4>
            <p class="text-sm text-gray-600 truncate w-40">${conv.customer.lastMsg}</p>
          </div>
        </div>
        <div class="text-right">
          <p class="text-xs text-gray-500">${conv.customer.time}</p>
          ${conv.customer.unread > 0 ? `<span class="bg-red-600 text-white text-xs rounded-full px-2 py-1 mt-1 inline-block">${conv.customer.unread}</span>` : ''}
        </div>
      </div>
    `;
    list.appendChild(item);
  });

  const badge = document.getElementById('totalBadge');
  if (totalUnread > 0) {
    badge.textContent = totalUnread;
    badge.classList.remove('hidden');
  } else {
    badge.classList.add('hidden');
  }
}

function openChat(conv) {
  currentCustomer = conv;

  // Desktop
  document.getElementById('chatWith').textContent = conv.customer.name;
  renderMessages(conv.messages);
  document.getElementById('chatArea').classList.remove('hidden');

  // Mobile
  document.getElementById('mobileChatName').textContent = conv.customer.name;
  document.getElementById('mobileMessages').innerHTML = document.getElementById('messagesContainer').innerHTML;
  document.getElementById('mobileChat').classList.remove('hidden');

  // Mark as read
  conv.customer.unread = 0;
  renderConversations();
}

function backToList() {
  document.getElementById('mobileChat').classList.add('hidden');
}

function renderMessages(messages) {
  const container = document.getElementById('messagesContainer');
  const mobileContainer = document.getElementById('mobileMessages');
  const html = messages.map(msg => `
    <div class="mb-4 flex ${msg.sender === 'seller' ? 'justify-end' : 'justify-start'}">
      <div class="${msg.sender === 'seller' ? 'bg-blue-900 text-white' : 'bg-gray-200 text-gray-800'} px-5 py-3 rounded-2xl max-w-xs">
        <p>${msg.text}</p>
        <p class="text-xs opacity-70 mt-1">${msg.time}</p>
      </div>
    </div>
  `).join('');

  container.innerHTML = html || '<p class="text-center text-gray-500">Start the conversation...</p>';
  if (mobileContainer) mobileContainer.innerHTML = container.innerHTML;
  container.scrollTop = container.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById('messageInput');
  const mobileInput = document.getElementById('mobileInput');
  const text = input.value.trim() || mobileInput.value.trim();
  if (!text || !currentCustomer) return;

  const newMsg = {
    text: text,
    sender: "seller",
    time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
  };

  currentCustomer.messages.push(newMsg);
  currentCustomer.customer.lastMsg = "You: " + text;
  currentCustomer.customer.time = "Just now";

  renderMessages(currentCustomer.messages);
  renderConversations();

  input.value = '';
  if (mobileInput) mobileInput.value = '';
}

// Enter key to send
document.getElementById('messageInput').addEventListener('keypress', e => { if(e.key === 'Enter') sendMessage(); });
document.getElementById('mobileInput')?.addEventListener('keypress', e => { if(e.key === 'Enter') sendMessage(); });

// Start
renderConversations();