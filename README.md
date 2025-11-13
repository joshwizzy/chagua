# CHAGUA E-Commerce Platform

A multi-vendor e-commerce platform designed for Uganda, Rwanda, and Burundi. CHAGUA connects product sellers with buyers across East Africa without holding inventory.

## Features

### Core Features
- **Phone-based Authentication**: User registration and login with phone number + PIN
- **Multi-Factor Authentication (MFA)**: Optional TOTP-based MFA for enhanced security
- **User Roles**: Buyers, Sellers, and Administrators
- **Product Management**: Multi-category product listings with images and variants
- **Order Management**: Comprehensive order tracking with unique tracking numbers
- **Tracking Number Format**: `CHAGUA-YYYYMMDD-XXXX` (sequential daily numbering)
- **Shopping Cart**: Full cart functionality with item management
- **Payment Integration**: Cash on Delivery, Airtel Money, MTN Mobile Money
- **Notifications**: SMS, Email, and in-app notifications
- **Reviews & Ratings**: Product and seller rating system
- **Subscription Plans**: Basic, Pro, and Premium tiers for sellers
- **Multi-language Support**: English, French, and Swahili
- **PWA Support**: Progressive Web App for offline functionality

### Product Categories
- Clothes
- Cosmetics
- Shoes
- Jewelry
- Bags
- Gadgets
- Others

## Technology Stack

### Backend
- **Framework**: Django 4.2.7 + Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT with SimpleJWT
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **Build Tool**: Vite
- **State Management**: Pinia
- **Routing**: Vue Router
- **Internationalization**: Vue I18n
- **PWA**: vite-plugin-pwa

## Project Structure

```
chagua/
├── backend/                 # Django backend
│   ├── chagua_backend/     # Main Django settings
│   ├── users/              # User authentication & profiles
│   ├── products/           # Product management
│   ├── orders/             # Order & cart management
│   ├── payments/           # Payment processing
│   ├── notifications/      # Notification system
│   ├── subscriptions/      # Seller subscriptions
│   ├── reviews/            # Product & seller reviews
│   ├── manage.py
│   └── requirements.txt
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── views/         # Page components
│   │   ├── stores/        # Pinia stores
│   │   ├── router/        # Vue Router config
│   │   ├── services/      # API services
│   │   └── locales/       # i18n translations
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- pip and npm

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create PostgreSQL database**:
   ```sql
   CREATE DATABASE chagua_db;
   CREATE USER chagua_user WITH PASSWORD 'your_password';
   ALTER ROLE chagua_user SET client_encoding TO 'utf8';
   ALTER ROLE chagua_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE chagua_user SET timezone TO 'Africa/Kampala';
   GRANT ALL PRIVILEGES ON DATABASE chagua_db TO chagua_user;
   ```

5. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your configuration:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=chagua_db
   DB_USER=chagua_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

6. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**:
   ```bash
   python manage.py runserver
   ```

   Backend will be available at: `http://localhost:8000`
   API Documentation: `http://localhost:8000/api/docs/`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

4. **Run development server**:
   ```bash
   npm run dev
   ```

   Frontend will be available at: `http://localhost:5173`

5. **Build for production**:
   ```bash
   npm run build
   ```

## API Endpoints

### Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `POST /api/users/logout/` - User logout
- `POST /api/users/token/refresh/` - Refresh access token

### Products
- `GET /api/products/` - List all products
- `GET /api/products/<slug>/` - Get product details
- `GET /api/products/categories/` - List categories
- `POST /api/products/seller/products/` - Create product (sellers only)
- `GET /api/products/featured/` - Get featured products
- `GET /api/products/popular/` - Get popular products

### Orders
- `GET /api/orders/` - List user's orders
- `POST /api/orders/create/` - Create order from cart
- `GET /api/orders/<tracking_number>/` - Get order details
- `POST /api/orders/<id>/status/` - Update order status (sellers)
- `GET /api/orders/track/<tracking_number>/` - Track order

### Cart
- `GET /api/orders/cart/` - Get shopping cart
- `POST /api/orders/cart/add/` - Add item to cart
- `PUT /api/orders/cart/items/<id>/` - Update cart item quantity
- `DELETE /api/orders/cart/items/<id>/remove/` - Remove item from cart
- `POST /api/orders/cart/clear/` - Clear cart

### Payments
- `POST /api/payments/initiate/` - Initiate payment
- `GET /api/payments/<id>/` - Get payment details

### Reviews
- `GET /api/reviews/products/<product_id>/` - List product reviews
- `POST /api/reviews/products/<product_id>/` - Create product review
- `GET /api/reviews/sellers/<seller_id>/` - List seller reviews

## Order Flow

1. **Customer places order** → System generates tracking number (e.g., `CHAGUA-20251113-0001`)
2. **Notification sent to seller** → Via WhatsApp, SMS, or email with order details and tracking number
3. **Seller confirms order** → Status updated to "Confirmed"
4. **Seller ships product** → Can upload courier receipt photo, status updated to "Shipped"
5. **System notifies customer** → With tracking number and shipping confirmation
6. **Order delivered** → Status updated to "Delivered"

## Tracking Number System

The platform automatically generates unique tracking numbers for each order:

- **Format**: `CHAGUA-YYYYMMDD-XXXX`
  - `CHAGUA`: Company/platform code
  - `YYYYMMDD`: Order date (e.g., 20251113)
  - `XXXX`: Sequential number for the day (e.g., 0001, 0002, etc.)

- **Example**: `CHAGUA-20251113-0001` (first order on November 13, 2025)

- **Optional Randomization**: Can be configured to use random alphanumeric suffix (e.g., `CHAGUA-20251113-A7F3`)

## Subscription Plans

### Basic
- **Price**: 50,000 UGX/month
- **Listings**: Up to 10 products
- **Features**: Standard visibility

### Pro
- **Price**: 150,000 UGX/month
- **Listings**: Up to 50 products
- **Features**: Enhanced visibility

### Premium
- **Price**: 300,000 UGX/month
- **Listings**: Unlimited products
- **Features**: Priority placement, featured status

## Multi-Currency Support

The platform supports display-only currency conversion for:
- **UGX** - Ugandan Shilling (default)
- **RWF** - Rwandan Franc
- **BIF** - Burundian Franc

## Development

### Running Tests
```bash
cd backend
python manage.py test
```

### Code Formatting
```bash
# Backend
black .
flake8

# Frontend
npm run lint
```

### Database Migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## Deployment

### Backend Deployment
1. Set `DEBUG=False` in production
2. Configure proper `SECRET_KEY`
3. Set up PostgreSQL database
4. Configure static files serving
5. Set up media files storage (e.g., AWS S3)
6. Configure CORS settings for production domain
7. Set up SSL certificate
8. Use production WSGI server (e.g., Gunicorn, uWSGI)

### Frontend Deployment
1. Update `VITE_API_BASE_URL` in `.env`
2. Build for production: `npm run build`
3. Deploy `dist/` folder to hosting service
4. Configure routing for SPA
5. Set up SSL certificate

## Security Features

- Phone number + PIN authentication
- Optional MFA with TOTP
- JWT token-based authentication
- HTTPS encryption (in production)
- Password hashing with Django's default
- CSRF protection
- Input validation and sanitization
- SQL injection prevention (Django ORM)
- XSS protection

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is proprietary software. All rights reserved.

## Support

For support and questions, please contact the development team.

## Roadmap

- [ ] Mobile app development (React Native/Flutter)
- [ ] Advanced analytics dashboard
- [ ] AI-powered product recommendations
- [ ] Enhanced logistics integration
- [ ] Additional payment gateways
- [ ] Multi-warehouse support
- [ ] Bulk import/export tools
- [ ] Advanced search with filters
- [ ] Real-time chat support
- [ ] Social media integration

---

Built with ❤️ for East Africa
