# K&T Financial Hub - Django Backend

This Django REST API replaces the Supabase backend for the K&T Financial Consultancy website.

## Quick Start

### 1. Setup PostgreSQL

Make sure PostgreSQL is installed and running:

```bash
# macOS (with Homebrew)
brew install postgresql
brew services start postgresql

# Create database
createdb kt_financial

# Or use Docker
docker run -d --name kt-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=kt_financial \
  -p 5432:5432 postgres:15
```

### 2. Setup Django

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environment Variables

Edit `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://postgres:postgres@localhost:5432/kt_financial
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8080,https://www.kt-info.com
```

### Database URL Format

```
postgres://USER:PASSWORD@HOST:PORT/DATABASE
```

**Examples:**
```
# Local development
postgres://postgres:postgres@localhost:5432/kt_financial

# Production
postgres://user:password@db.example.com:5432/kt_financial

# Railway/Render (they provide this URL)
postgres://user:password@host.railway.app:5432/railway
```

## API Endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/api/auth/login/` | POST | User login |
| `/api/auth/logout/` | POST | User logout |
| `/api/auth/change-password/` | POST | Change password |
| `/api/about-content/` | GET, POST, PUT, PATCH, DELETE | About page content |
| `/api/home-content/` | GET, POST, PUT, PATCH, DELETE | Home page content |
| `/api/services-content/` | GET, POST, PUT, PATCH, DELETE | Services content |
| `/api/blog-posts/` | GET, POST, PUT, PATCH, DELETE | Blog posts |
| `/api/blog-categories/` | GET, POST, PUT, PATCH, DELETE | Blog categories |
| `/api/business-contact/` | GET, POST, PUT, PATCH | Contact info |
| `/api/consultation-bookings/` | GET, POST | Consultation bookings |
| `/api/contact-submissions/` | GET, POST | Contact form submissions |
| `/api/admin-profiles/me/` | GET, PUT, PATCH | Current user profile |

## Admin Interface

Access at: `http://localhost:8000/admin/`

## Production Deployment

### 1. Set Production Environment

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-production-database-url
ALLOWED_HOSTS=your-api-domain.com
CORS_ALLOWED_ORIGINS=https://www.kt-info.com
```

### 2. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 3. Deploy to Platform

Recommended platforms:
- **Railway** (easiest)
- **Render**
- **DigitalOcean App Platform**
- **Heroku**

### Railway Deployment (Recommended)

1. Push code to GitHub
2. Connect Railway to your repo
3. Add environment variables in Railway dashboard
4. Deploy automatically

## Migration from Supabase

To migrate existing data:

1. Export data from Supabase as JSON
2. Use the migration script:

```bash
python manage.py shell
```

Then import your data using Django ORM or create a custom management command.

## Testing

```bash
python manage.py test
```

## Models

The backend includes models matching the original Supabase schema:

- **AboutContent** - About page sections
- **HomeContent** - Home page sections
- **ServicesContent** - Services information
- **BlogPost** / **BlogCategory** - Blog system
- **BusinessContact** - Contact information
- **ConsultationBooking** - Booking form submissions
- **ContactSubmission** - Contact form submissions
- **AdminProfile** - Admin user profiles
