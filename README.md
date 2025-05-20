# NumEduLab

A simple frontend app using Alpine.js + Tailwind CSS for interacting with a numerical methods API.

## 🧠 Features

- Bisection Method
- Newton-Raphson Method
- Secant Method
- False Position Method
- Fixed Point Iteration

## 🖥 Frontend Setup

No build step needed. It's a plain HTML + Alpine.js + Tailwind app.

### ✅ Run Locally

1. Clone the repository:

```bash
git clone https://github.com/your-username/numedulab.git
cd numedulab
```

2. Open `index.html` directly in your browser:
- OR use a static server:

```bash
# Using Python (optional)
python3 -m http.server 8001
# Then visit: http://localhost:8001
```

---

## ⚙️ Backend Setup

Assumes your backend is a FastAPI service (running `main.py` or similar).

### Create virtual environment & install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> If you don’t have a `requirements.txt`, use:

```bash
pip install fastapi uvicorn sympy
```

### Run the API server:

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Make sure the API endpoints are accessible at:
```
http://127.0.0.1:8000/api/<method>
```

---

## 🔁 Frontend–Backend Sync

Ensure the API in `index.html` points to the correct backend address:

```js
fetch(`http://127.0.0.1:8000/api/${methodId}`, {
  method: "POST",
  ...
})
```

If you're deploying or using a different port, update that line.

---

## 📸 Screenshot

> _Add a screenshot of the app here if desired._

---

## 📄 License

MIT
