# Booking API Assignment

- JWT Token based authorisation
- JWT Access and Refresh tokens
- Pydantic-based model validation
- All 6 required API endpoints and an additional POST /refresh 
- Unit and Integration test with pytest
- OpenAPI/Swagger documentation including business exceptions
- Database seed script
- Sphinx-based documentation


## Setup
1. Clone repo
```
git clone --depth 1 https://github.com/ksaze/booking-api.git
cd booking-api/
```

2. Set up virtual env and build dependencies
```
python -m venv .venv
source .venv/bin/activate
pip install .
```

3. Create a .env using .example_env 
```
mv .example_env .env
```

4. Add a security key and change any other variables if required
```
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
or
```
openssl rand -hex 32
```

## Running
1. (Optional) Use database seed script
```
python -m scripts.seed
```

2. Start the development server:
```
uvicorn app.main:app --reload
```

3. The API will be available at:
```
http://127.0.0.1:8000
```

Interactive Swagger documentation:
```
http://127.0.0.1:8000/docs
```

OpenAPI specification:
```
http://127.0.0.1:8000/openapi.json
```

# Documentation
- General Documentation (Sphinx)
```
cd docs/
make html
xdg-open build/html/index.html
```

- API documentation (Swagger)
```
uvicorn app.main:app --reload
http://127.0.0.1:8000/docs
```

# API Usage
(Generated from swagger docs)

1. Sign Up (POST /signup)
```
curl -X 'POST' \
  'http://127.0.0.1:8000/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "string",
  "email": "user@example.com",
  "password": "stringst"
}'
```

2. Log In (POST /login)
```
curl -X 'POST' \
  'http://127.0.0.1:8000/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "string",
  "password": "string"
}'
```
example response:
```
{
"access_token": "<jwt>",
"refresh_token": "<jwt>",
"token_type": "bearer" 
}
```

3. Refresh Token (POST /refresh)
```
curl -X POST \
  http://127.0.0.1:8000/refresh \
  -H "Authorization: Bearer <refresh_token>"
  -d ''
```

4. List upcoming classes (GET /classes)
```
curl -X 'GET' \
  'http://127.0.0.1:8000/classes' \
  -H 'accept: application/json'
```

5. Create a new class (POST /classes)
```
curl -X POST http://127.0.0.1:8000/classes \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name":"Yoga Flow",
  "dateTime":"2026-07-15T10:00:00Z",
  "instructor":"John Doe",
  "availableSlots":20 
}'
```

6. Book a class (POST /book)
```
curl -X 'POST' \
  'http://127.0.0.1:8000/book' \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "class_id": 0,
  "client_name": "string",
  "client_email": "user@example.com"
}'
```

7. List upcoming booked classes (GET /bookings)
```
curl http://127.0.0.1:8000/bookings \
-H "Authorization: Bearer <access_token>"
```
