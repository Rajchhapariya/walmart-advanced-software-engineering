# API Specification & Endpoint Contracts

**API Standard:** RESTful JSON / OpenAPI 3.1  
**Base URL:** `/api/v1`  
**Authentication:** Bearer JWT in `Authorization` Header

---

## 1. Authentication Endpoints

### `POST /api/v1/auth/login`

- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response `200 OK`:**
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "expires_in": 3600
  }
  ```
- **Error `401 Unauthorized`:**
  ```json
  {
    "error": "INVALID_CREDENTIALS",
    "message": "The email or password provided is incorrect."
  }
  ```

---

## 2. Resource Endpoints

### `GET /api/v1/resources`

- **Query Parameters:**
  - `page`: Integer (default: 1)
  - `limit`: Integer (default: 20, max: 100)
  - `sort`: String (e.g. `-created_at`)
- **Response `200 OK`:**
  ```json
  {
    "data": [],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total_count": 0,
      "total_pages": 0
    }
  }
  ```
