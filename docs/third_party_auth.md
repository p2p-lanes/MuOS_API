## Third‑Party Authentication Integration Guide

This guide explains how an external application can authenticate a user via the Citizen Portal and obtain a Bearer token to call protected endpoints.

### Overview
- **Goal**: Verify a user by email using a short‑lived code and receive a JWT Bearer token.
- **Flow**:
  1. Your app calls `POST /citizens/authenticate-third-party` with the user's email and your app name.
  2. The portal sends a 6‑digit code to the user's email (valid for 5 minutes).
  3. Your app collects the code from the user and calls `POST /citizens/login` with `email` and `code` as query parameters.
  4. You receive a JWT Bearer token to access protected endpoints.

Use `https://<BASE_URL>` for your deployment host.

### Endpoints

#### 1) Request email code
- **Method/Path**: `POST /citizens/authenticate-third-party`
- **Body (JSON)**:
```json
{
  "email": "user@example.com",
  "app_name": "YourAppName"
}
```
- **Success (200)**:
```json
{ "message": "Mail sent successfully" }
```
- **Errors**:
  - 404 if the citizen does not exist.

Example cURL:
```bash
curl -X POST \
  "https://<BASE_URL>/citizens/authenticate-third-party" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "app_name": "YourAppName"
  }'
```

#### 2) Exchange code for token
- **Method/Path**: `POST /citizens/login`
- **Query parameters**: `email` (string), `code` (integer)
- **Success (200)**:
```json
{
  "access_token": "<jwt>",
  "token_type": "Bearer"
}
```
- **Errors**:
  - 400 if `email` and `code` are not both provided
  - 401 if the code is invalid or expired
  - 404 if the citizen is not found

Example cURL:
```bash
curl -X POST \
  "https://<BASE_URL>/citizens/login?email=user%40example.com&code=123456"
```

Token details:
- **Format**: JWT (HS256).
- **Claims**: includes `citizen_id`, `email`, and may include `third_party_app` when this flow is used.
- **Usage**: send in the `Authorization` header as `Bearer <token>`.

### Using the token
Example: Get the authenticated citizen's profile
```bash
curl -X GET \
  "https://<BASE_URL>/citizens/profile" \
  -H "Authorization: Bearer <token>"
```

### Practical considerations
- **Security**: Always use HTTPS and never log or expose the code or token.
- **Code lifetime**: 5 minutes; prompt the user to request a new code on failure.
- **Token lifetime**: The API validates the JWT signature server‑side. If you receive 401 responses, repeat the code exchange flow.
- **Branding**: Provide a recognizable `app_name`; it will be embedded in the token for traceability.
