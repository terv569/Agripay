# 🌾 Agripay - Farm to Table Marketplace

A modern Django-based e-commerce platform connecting farmers directly with customers. Buy fresh produce at fair prices while supporting local agriculture.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### For Customers
- 🛒 Browse fresh products from local farmers
- 🔍 Real-time product search
- 🛍️ Shopping cart with order summary
- 💳 M-Pesa payment integration (Daraja API)
- 📱 Fully responsive design

### For Farmers
- 👨‍🌾 Create farmer profiles with images
- 📦 List and manage products
- ✏️ Edit product details and pricing
- 📊 Track inventory

### UI/UX
- 🎨 Modern gradient design with agricultural theme
- ✨ Smooth animations and hover effects
- 🎯 Intuitive navigation with sticky navbar
- 📱 Mobile-first responsive layout
- 🔔 Alert notifications for user feedback

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/agripay.git
cd agripay_option_a
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Homepage: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
agripay_option_a/
├── accounts/          # User authentication
├── farmers/           # Farmer profiles & products
├── marketplace/       # Product browsing & cart
├── payments/          # M-Pesa integration
├── static/           
│   └── css/
│       └── theme.css  # Custom styling
├── templates/         # HTML templates
├── media/            # User uploads
└── agripay/          # Main project settings
```

## 🎨 Tech Stack

- **Backend:** Django 4.x
- **Frontend:** Bootstrap 5, Bootstrap Icons
- **Database:** SQLite (development)
- **Payment:** Safaricom Daraja API (M-Pesa)
- **Styling:** Custom CSS with gradients & animations

## 💳 M-Pesa Configuration

Update `settings.py` with your Daraja API credentials:

```python
DARAJA_CONSUMER_KEY = 'your_consumer_key'
DARAJA_CONSUMER_SECRET = 'your_consumer_secret'
DARAJA_SHORTCODE = 'your_shortcode'
DARAJA_PASSKEY = 'your_passkey'
DARAJA_ENVIRONMENT = 'sandbox'  # or 'production'
```

**Sandbox Test Number:** 254708374149

## 🔑 Key Features Explained

### Product Management
- Farmers can create, edit, and delete products
- Image upload support for products and profiles
- Real-time inventory tracking

### Shopping Experience
- Live search filtering
- Product cards with hover animations
- Order summary with itemized breakdown
- Secure checkout flow

### Payment Integration
- M-Pesa STK Push integration
- Phone number validation
- Transaction status tracking

## 🎯 Usage

### As a Customer
1. Browse the marketplace
2. Add products to cart
3. Login or signup
4. Enter M-Pesa phone number
5. Complete payment via STK push

### As a Farmer
1. Sign up for an account
2. Create farmer profile
3. Add products with images and pricing
4. Manage inventory
5. Edit or delete products as needed

## 🛠️ Development

### Seeding Data
```bash
python manage.py seed_data
```

### Running Tests
```bash
python manage.py test
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## 🌈 UI Highlights

- **Color Scheme:** Green gradients (agricultural theme)
- **Animations:** Smooth hover effects, card lifts, image zoom
- **Typography:** Modern sans-serif with proper hierarchy
- **Components:** Stat cards, product badges, price tags
- **Footer:** Professional with contact info and social links

## 📱 Responsive Design

- Mobile-first approach
- Breakpoints for tablets and desktops
- Touch-friendly buttons and forms
- Optimized images

## 🔒 Security Notes

- CSRF protection enabled
- Password validation
- Secure payment handling
- Environment variables for sensitive data (recommended for production)

## 🚧 Future Enhancements

- [ ] Order history and tracking
- [ ] Farmer dashboard with analytics
- [ ] Product reviews and ratings
- [ ] Advanced search filters
- [ ] Email notifications
- [ ] Multi-vendor support
- [ ] Delivery tracking

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

Tervil Moywaywa 

## 🙏 Acknowledgments

- Bootstrap for UI components
- Safaricom Daraja API for payment integration
- Unsplash for placeholder images
- Bootstrap Icons for iconography

## 📞 Support

For support, email support@agripay.com or open an issue in the repository.

---

