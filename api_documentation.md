# Chemical Inventory API Documentation

This document provides a comprehensive reference for the Chemical Inventory API endpoints, request/response formats, and authentication requirements.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-production-domain.com`

## Authentication

The API uses JWT (JSON Web Token) for authentication. Include the token in the Authorization header for protected endpoints:

```
Authorization: Bearer <access_token>
```

### Authentication Endpoints

#### Register User

```
POST /api/users/register/
```

Creates a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login

```
POST /api/users/token/
```

Authenticates a user and returns access and refresh tokens.

**Request Body:**
```json
{
  "username": "username",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Refresh Token

```
POST /api/users/token/refresh/
```

Obtains a new access token using a refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## User Endpoints

### Get Current User

```
GET /api/users/me/
```

Returns information about the currently authenticated user.

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "username",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_staff": false
}
```

### Update User Profile

```
PATCH /api/users/me/
```

Updates the authenticated user's profile information.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "username",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_staff": false
}
```

## Inventory Endpoints

### List Chemicals

```
GET /api/inventory/chemicals/
```

Returns a paginated list of chemicals in the inventory.

**Query Parameters:**
- `page` (optional): Page number
- `page_size` (optional): Items per page
- `search` (optional): Search term for chemical name or formula
- `category` (optional): Filter by category ID
- `location` (optional): Filter by storage location ID

**Response (200 OK):**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/inventory/chemicals/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Sodium Chloride",
      "chemical_formula": "NaCl",
      "cas_number": "7647-14-5",
      "category": {
        "id": 1,
        "name": "Inorganic Salts"
      },
      "hazard_level": "Low",
      "storage_location": {
        "id": 1,
        "name": "Cabinet A-1"
      },
      "quantity": 500,
      "unit": "g",
      "date_added": "2023-10-15T14:30:00Z",
      "expiry_date": "2025-10-15T00:00:00Z"
    },
    {
      "id": 2,
      "name": "Sulfuric Acid",
      "chemical_formula": "H2SO4",
      "cas_number": "7664-93-9",
      "category": {
        "id": 2,
        "name": "Acids"
      },
      "hazard_level": "High",
      "storage_location": {
        "id": 2,
        "name": "Acid Cabinet B-3"
      },
      "quantity": 250,
      "unit": "ml",
      "date_added": "2023-09-20T10:15:00Z",
      "expiry_date": "2024-09-20T00:00:00Z"
    }
  ]
}
```

### Get Chemical Details

```
GET /api/inventory/chemicals/{id}/
```

Returns detailed information about a specific chemical.

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Sodium Chloride",
  "chemical_formula": "NaCl",
  "cas_number": "7647-14-5",
  "molecular_weight": 58.44,
  "category": {
    "id": 1,
    "name": "Inorganic Salts"
  },
  "hazard_level": "Low",
  "hazard_statements": [
    "May cause mild eye irritation"
  ],
  "precautionary_statements": [
    "Wear eye protection",
    "Wash hands thoroughly after handling"
  ],
  "storage_conditions": "Store in a cool, dry place",
  "storage_location": {
    "id": 1,
    "name": "Cabinet A-1",
    "room": "Chemistry Lab 101"
  },
  "quantity": 500,
  "unit": "g",
  "supplier": "Sigma-Aldrich",
  "catalog_number": "S7653",
  "date_added": "2023-10-15T14:30:00Z",
  "expiry_date": "2025-10-15T00:00:00Z",
  "date_opened": null,
  "added_by": {
    "id": 1,
    "username": "labmanager"
  },
  "safety_data_sheet_url": "http://localhost:8000/media/sds/sodium_chloride.pdf"
}
```

### Create Chemical

```
POST /api/inventory/chemicals/
```

Adds a new chemical to the inventory.

**Request Body:**
```json
{
  "name": "Potassium Hydroxide",
  "chemical_formula": "KOH",
  "cas_number": "1310-58-3",
  "molecular_weight": 56.11,
  "category_id": 3,
  "hazard_level": "High",
  "hazard_statements": [
    "Causes severe skin burns and eye damage",
    "May be corrosive to metals"
  ],
  "precautionary_statements": [
    "Do not breathe dust/fume/gas/mist/vapours/spray",
    "Wear protective gloves/protective clothing/eye protection/face protection",
    "IF SWALLOWED: Rinse mouth. Do NOT induce vomiting"
  ],
  "storage_conditions": "Store in a dry place. Store in a closed container.",
  "storage_location_id": 3,
  "quantity": 100,
  "unit": "g",
  "supplier": "Merck",
  "catalog_number": "105033",
  "expiry_date": "2024-12-31"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "Potassium Hydroxide",
  "chemical_formula": "KOH",
  "cas_number": "1310-58-3",
  "molecular_weight": 56.11,
  "category": {
    "id": 3,
    "name": "Bases"
  },
  "hazard_level": "High",
  "hazard_statements": [
    "Causes severe skin burns and eye damage",
    "May be corrosive to metals"
  ],
  "precautionary_statements": [
    "Do not breathe dust/fume/gas/mist/vapours/spray",
    "Wear protective gloves/protective clothing/eye protection/face protection",
    "IF SWALLOWED: Rinse mouth. Do NOT induce vomiting"
  ],
  "storage_conditions": "Store in a dry place. Store in a closed container.",
  "storage_location": {
    "id": 3,
    "name": "Base Cabinet C-2",
    "room": "Chemistry Lab 101"
  },
  "quantity": 100,
  "unit": "g",
  "supplier": "Merck",
  "catalog_number": "105033",
  "date_added": "2023-11-20T09:45:12Z",
  "expiry_date": "2024-12-31T00:00:00Z",
  "date_opened": null,
  "added_by": {
    "id": 1,
    "username": "labmanager"
  },
  "safety_data_sheet_url": null
}
```

### Update Chemical

```
PATCH /api/inventory/chemicals/{id}/
```

Updates information about a specific chemical.

**Request Body:**
```json
{
  "quantity": 450,
  "date_opened": "2023-11-21T08:30:00Z"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Sodium Chloride",
  "chemical_formula": "NaCl",
  "quantity": 450,
  "unit": "g",
  "date_opened": "2023-11-21T08:30:00Z",
  "date_added": "2023-10-15T14:30:00Z",
  "expiry_date": "2025-10-15T00:00:00Z"
}
```

### Delete Chemical

```
DELETE /api/inventory/chemicals/{id}/
```

Removes a chemical from the inventory.

**Response (204 No Content)**

### List Categories

```
GET /api/inventory/categories/
```

Returns a list of chemical categories.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Inorganic Salts",
    "description": "Ionic compounds that are not of biological origin"
  },
  {
    "id": 2,
    "name": "Acids",
    "description": "Compounds that donate hydrogen ions (protons) in aqueous solutions"
  },
  {
    "id": 3,
    "name": "Bases",
    "description": "Compounds that accept hydrogen ions (protons) in aqueous solutions"
  }
]
```

### List Storage Locations

```
GET /api/inventory/locations/
```

Returns a list of available storage locations.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Cabinet A-1",
    "room": "Chemistry Lab 101",
    "description": "General chemicals storage cabinet",
    "category": null
  },
  {
    "id": 2,
    "name": "Acid Cabinet B-3",
    "room": "Chemistry Lab 101",
    "description": "Acid-resistant cabinet with ventilation",
    "category": {
      "id": 2,
      "name": "Acids"
    }
  },
  {
    "id": 3,
    "name": "Base Cabinet C-2",
    "room": "Chemistry Lab 101",
    "description": "Base-resistant cabinet with ventilation",
    "category": {
      "id": 3,
      "name": "Bases"
    }
  }
]
```

## Reporting Endpoints

### Generate Inventory Report

```
GET /api/reports/inventory/
```

Generates a report of the current inventory.

**Query Parameters:**
- `format` (optional): Output format, either "pdf" or "xlsx" (default: "pdf")
- `category` (optional): Filter by category ID
- `location` (optional): Filter by storage location ID
- `expiring_before` (optional): Filter for chemicals expiring before this date (YYYY-MM-DD)

**Response (200 OK):**

Returns the generated report file with appropriate content type.

### Low Stock Report

```
GET /api/reports/low-stock/
```

Generates a report of chemicals with quantity below the defined threshold.

**Query Parameters:**
- `format` (optional): Output format, either "pdf" or "xlsx" (default: "pdf")
- `threshold` (optional): Custom threshold for defining low stock (overrides default settings)

**Response (200 OK):**

Returns the generated report file with appropriate content type.

## Status Codes

The API uses standard HTTP status codes:

- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `204 No Content`: Request succeeded with no content to return
- `400 Bad Request`: Invalid request format or parameters
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

## Error Responses

Error responses follow a standard format:

```json
{
  "detail": "Error message describing the problem"
}
```

For validation errors:

```json
{
  "field_name": [
    "Error message for this field"
  ],
  "another_field": [
    "Error message for another field"
  ]
}
```

## API Documentation

Interactive API documentation is available at:

- `/api/schema/swagger-ui/` - Swagger UI interface
- `/api/schema/redoc/` - ReDoc interface
- `/api/schema/` - OpenAPI schema (JSON) 