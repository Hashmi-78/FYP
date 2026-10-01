# 🛍️ Ahyera Store: Multi-Vendor E-Commerce with AI Features

> Final Year Project (BS Computer Science, COMSATS University Islamabad): a full-stack multi-vendor marketplace where sellers run their own storefronts and customers can **negotiate prices with an LLM** and **search by photo**.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-4.2-092E20)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-CSS-38BDF8)
![Groq](https://img.shields.io/badge/LLM-Llama%20via%20Groq-orange)

Built as a team of three.

---

## ✨ AI Features

### 🤝 LLM Price Negotiation
Customers can make an offer on a product, and a **Llama 3.3 70B** model (served through the Groq API) acts as the seller's negotiation assistant.

- The model is given the listed price, the seller's **minimum allowed price** and the customer's offer. It must reply in a strict format: `ACCEPT`, `REJECT` or `COUNTER: <price>`.
- The output is **validated in code, not trusted blindly**. Counter-offers are clamped between the minimum and listed price, and malformed responses fall back to a safe midpoint counter-offer.
- If the API key or endpoint is missing, the feature degrades gracefully instead of crashing.

Code: [`services/llama_service.py`](services/llama_service.py)

### 📷 Visual Product Search
Customers upload a photo of an item and get matching products from the catalogue.

1. The image is sent to the **Llama 4 Scout** vision model, which returns a short search query (item type, colour, style, material).
2. The query is cleaned into keywords and matched against product names, descriptions, brands and categories.

Code: [`services/visual_search_service.py`](services/visual_search_service.py)

### 🎯 Personalised Recommendations
Recommends products from the categories in a user's **order history** (weighted higher) and **wishlist**. It excludes items they have already bought, and falls back to top-rated products for new users.

Code: [`services/recommendation_service.py`](services/recommendation_service.py)

---

## 🏪 Marketplace Features

| Customers | Sellers |
|---|---|
| Browse, search and filter products | Seller onboarding with an approval step |
| Cart, wishlist and checkout | Add, edit and bulk-delete products |
| Saved shipping addresses | Order management and status updates |
| Order tracking and history | Delivery management |
| Chat with the seller about an order | Sales graphs and payment overview |
| Product reviews | Messaging with customers |

Plus: authentication with password reset by email, notifications, and role-based dashboards.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 4.2 |
| Frontend | Django templates, Tailwind CSS, JavaScript |
| Database | SQLite (development) |
| AI | Groq API: Llama 3.3 70B (negotiation), Llama 4 Scout (vision) |
| Other | python-decouple (config), WhiteNoise (static files), Pillow |

---

## 🗂️ Project Structure

```
FYP/
├── ahyera_store/      # Project settings and URLs
├── authentication/    # Login, registration, password reset
├── core/              # Landing and home pages
├── customers/         # Cart, checkout, orders, wishlist, chat, AI search
├── sellers/           # Seller dashboard, products, orders, delivery, sales
├── products/          # Product, category, review and negotiation models
├── services/          # AI services: negotiation, visual search, recommendations
├── templates/         # Shared templates
└── static/            # CSS, JS and images
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/Hashmi-78/FYP.git
cd FYP
python -m venv venv
venv\Scripts\activate        # Windows  (source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
LLAMA_ENDPOINT=https://api.groq.com/openai/v1/chat/completions
LLAMA_API_KEY=your-groq-api-key
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-app-password
```

Then:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000.

> The AI features need a free [Groq API key](https://console.groq.com/). Without one, the rest of the store still works.

---

## 👤 Author

**Muhammad Umar Usman Hashmi**: [GitHub](https://github.com/Hashmi-78) · [LinkedIn](https://www.linkedin.com/in/muhammad-umar-usman-hashmi-4a34002b8)
