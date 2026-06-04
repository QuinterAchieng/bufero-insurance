# Bufero Insurance Dashboard

## Project Overview

This is a full-stack insurance management application built with:

- Django REST Framework (Backend)
- React.js (Frontend)
- SQLite Database

The system allows customers to:

- View customer details
- View insurance policies
- View policy status
- Renew policies
- Submit insurance claims
- Prevent duplicate policy renewals through frontend button protection

---

## Features Implemented

### Backend

- Customer API
- Policy API
- Claim API
- Policy Renewal Endpoint
- Customer-Policy Relationship
- Policy Status Support:
  - ACTIVE
  - PENDING
  - LAPSED
  - UNDER_REVIEW

### Frontend

- Customer Dashboard
- Policy Cards
- Status Badges with Colors
- Claim Submission Modal
- Policy Renewal Button
- Double Click Protection

---

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- SQLite

### Frontend

- React
- Axios

---

## Setup Instructions

### Clone Repository

```bash
git clone https://github.com/QuinterAchieng/bufero-insurance.git
cd bufero-insurance
```

---

## Backend Setup

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install django
pip install djangorestframework
pip install django-cors-headers
```

Run migrations:

```bash
python manage.py migrate
```

Start backend server:

```bash
python manage.py runserver
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

## Frontend Setup

Navigate to frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start React app:

```bash
npm start
```

Frontend runs on:

```text
http://localhost:3000
```

---


## Folder Structure
bufero-insurance/

backend/
│
├── insurance/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── services.py
│   ├── tests.py
│
├── config/
│
└── manage.py

frontend/
│
├── src/
│   ├── pages/
│   ├── components/
│   ├── api/
│
└── package.json


## Architecture Reflection

The first bottleneck would likely be database contention from thousands of simultaneous policy and claim operations. Initially I would introduce Redis caching, optimize database indexing, and move long-running workflows such as claims processing to asynchronous background workers using Celery. As traffic grows further, I would separate read and write workloads using database replicas and deploy the application behind a load balancer.


## API Endpoints

### Create Customer

```http
POST /api/customers/
```

### Get Customer

```http
GET /api/customers/<id>/
```

### Renew Policy

```http
POST /api/renew-policy/
```

### Create Claim

```http
POST /api/claims/
```

---

## Policy Status Colors

| Status | Color |
| ACTIVE | Green |
| PENDING | Yellow |
| LAPSED | Red |
| UNDER_REVIEW | Orange |

---

## Double Click Protection

The Renew button is disabled while a renewal request is being processed.

Example:

```javascript
disabled={loading}
```

This prevents multiple submissions and duplicate renewals.

---

## Assumptions

- SQLite is used for development.
- A customer can have multiple policies.
- Claims can only be submitted for active policies.
- Policy renewal updates the policy status.

---

## Author

Quinter Odawo

GitHub:
https://github.com/QuinterAchieng
