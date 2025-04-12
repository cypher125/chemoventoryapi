# Chemical Inventory System

A comprehensive web-based system for managing and tracking chemical inventory in laboratory environments. This system helps ensure safety, compliance, and efficient resource management.

![Chemical Inventory](https://via.placeholder.com/800x400?text=Chemical+Inventory+System)

## Features

- **User Management**: Role-based access control for administrators and regular users
- **Comprehensive Chemical Tracking**: Store detailed information about chemicals including hazard data
- **Location Management**: Track where chemicals are stored and organize by storage conditions
- **Inventory Management**: Monitor quantities, expiration dates, and usage patterns
- **Reporting**: Generate PDF and Excel reports for inventory, low stock, and expiring chemicals
- **Search & Filter**: Quickly find chemicals by name, formula, location, or category
- **Safety Information**: Access safety data and hazard information for each chemical
- **Responsive Design**: Access the system from desktop or mobile devices

## Tech Stack

### Frontend
- React
- Material UI for styling
- React Router for navigation
- Axios for API requests
- JWT authentication

### Backend
- Django & Django REST Framework
- JWT authentication with Simple JWT
- SQLite (development) / PostgreSQL (production)
- ReportLab for PDF generation
- OpenPyXL for Excel report generation

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn
- Git

### Backend Setup

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/chemical-inventory.git
   cd chemical-inventory/backend
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Edit the .env file with your settings
   ```

5. Run migrations
   ```bash
   python manage.py migrate
   ```

6. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

7. Start the development server
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the frontend directory
   ```bash
   cd ../frontend
   ```

2. Install dependencies
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open your browser and navigate to http://localhost:3000

## API Documentation

API documentation is available at `/api/schema/swagger-ui/` when the backend server is running. This provides an interactive interface to explore the API endpoints and their functionality.

For more details, see [API Documentation](backend/api_documentation.md).

## Architecture

The system follows a client-server architecture with a React frontend communicating with a Django REST API backend. For more details about the system architecture, see [Architecture Overview](backend/architecture_overview.md).

## Deployment

### Backend Deployment

1. Set up a production database (PostgreSQL recommended)
2. Configure environment variables for production
3. Collect static files
   ```bash
   python manage.py collectstatic
   ```
4. Use Gunicorn as the WSGI server
   ```bash
   gunicorn chemoventry.wsgi
   ```
5. Set up Nginx as a reverse proxy

### Frontend Deployment

1. Build the frontend
   ```bash
   npm run build
   # or
   yarn build
   ```
2. Serve the built files with Nginx or another web server

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django and React communities for excellent documentation
- All contributors who have helped build and improve this system 