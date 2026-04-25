# Cloud-Based eCommerce Analytics Tool

#Overview
This is a cloud-based web application designed to analyze product data and identify profitable items for resale.

The application allows users to search for products, estimate profit margins, and view ranked results based on profitability.

---

# Features
- Search products using keyword input
- Calculate estimated profit margins
- Rank items based on profitability
- Simple frontend interface for user interaction
- REST API backend returning structured JSON data

---

# Tech Stack
- **Cloud:** AWS EC2
- **Backend:** Python, Flask
- **Web Server:** NGINX
- **Application Server:** Gunicorn
- **Containerization:** Docker
- **Frontend:** HTML, CSS, JavaScript
- **Version Control:** Git, GitHub

---

# Architecture
User → NGINX → Gunicorn → Flask → API → Response (JSON)

---

# How It Works
1. User enters a product keyword and buy price
2. Flask backend processes the request
3. External API provides product data
4. Application calculates estimated profit
5. Results are returned and displayed on the frontend

---

# Setup Instructions

 Clone the repository
```bash
git clone https://github.com/IsaiahSeeram-Dev/ebay-analytics-tool.git
cd ebay-analytics-tool
