# 🚀 Command Gateway – Hackathon Project  
A rule‑based command processing system with API‑key authentication, admin dashboard, dynamic rule engine, audit logging, and credit‑based execution.

This project was built for the **Unbound Hackathon 2025**.

---

## 🏗️ Project Structure

backend/
main.py
models.py
schemas.py
logger.py
database.py
routers/
users.py
rules.py
commands.py
logs.py

frontend/
src/
App.jsx
App.css
index.html
vite.config.js
package.json


---

# 🌐 Features Overview

## 👤 1. Users & API Authentication
- Each user has an API key
- API key sent via `x-api-key` header
- Roles: `admin` / `member`
- Admins can create new users and reset credits

## 💳 2. Credit System
- Every command costs **1 credit**
- Reject command if credits = 0
- Credits only deducted on successful execution

## 📏 3. Rules Engine
- Admins define **regex-based rules**
- Each rule has an action:
  - `AUTO_ACCEPT`
  - `AUTO_REJECT`
- First matching rule determines the output

## ⚙️ 4. Command Execution
- Mock execution (no real shell commands)
- Logged with status and stored in DB

## 📝 5. Audit Logging
Every important event is logged:
- Rule created
- User created
- User viewed
- Command executed
- Command rejected

Admins can view:
- System logs
- Logs by user
- Their own logs  
Members can view:
- Only their own logs

## 🖥️ 6. React Admin Panel (Frontend)
Built using **React + Vite**:
- Sidebar navigation  
- Execute commands  
- Manage rules  
- Create users  
- View logs (system, my logs, logs by user)

---

# ⚙️ Backend Setup (FastAPI)

## 1️⃣ Create virtual env
```bash
python -m venv .venv
Activate:

.venv\Scripts\activate   # Windows
2️⃣ Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic
3️⃣ Run backend
uvicorn main:app --reload
Backend runs at:

http://127.0.0.1:8000
💻 Frontend Setup (React + Vite)
1️⃣ Install dependencies
npm install
2️⃣ Start frontend
npm run dev
Frontend runs at:

http://localhost:5173
🔌 API Endpoints (Summary)
Users
POST /users/
GET  /users/me
GET  /users/
Rules
POST /rules/
GET  /rules/
Commands
POST /commands/
GET  /commands/
Logs
GET /logs/me
GET /logs/system
GET /logs/user/{id}

🎯 Bonus Features Implemented
Complete audit logging layer

Admin can view logs by user

Rule validation (regex-safe)

Complete frontend dashboard layout

Role-based UI rendering

Credit deduction logic

👩‍💻 Author
Namritha R
