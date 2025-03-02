---
title: Use NeonDB for a Django project deployed to Railway
summary: Set a Django project using NeonDB, and deployed it to Railway
date: 2025-03-02
badge: code
image:
---

Here's a guide on **how to use NeonDB for a Django project deployed on Railway**.

---

## **Step 1: Create a NeonDB Database**
1. Go to [NeonDB](https://neon.tech/) and sign up.
2. Create a new PostgreSQL database.
3. Copy the **connection string** (it looks like `postgres://username:password@host:port/dbname`).

---

## **Step 2: Set Up Django with NeonDB**
In your **Django project**, install PostgreSQL dependencies:
```sh
pip install psycopg
```

Also install **`dj-database-url`**. **`dj_database_url`** is a **Django utility** that allows you to configure your **database connection** using a **single environment variable** (`DATABASE_URL`). It simplifies database settings, especially when deploying to cloud platforms like **NeonDB and Railway**.

Using **`dj_database_url`** is usefuk for several reasons :

✅ **Cleaner Code** → No need for long database settings.  
✅ **Easy to Switch Databases** → Just change the `DATABASE_URL`.  
✅ **Perfect for Cloud Deployments** → Platforms like **Heroku, Railway, and Render** provide `DATABASE_URL` by default.  
✅ **Works with PostgreSQL, MySQL, SQLite, etc.**  

Then, update your **`settings.py`**:

```python
import os
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}
```

### Why did I choose the `psycopg` package ?

The **`psycopg`** ecosystem has multiple packages, each designed for different use cases. Here’s a breakdown of the key differences:

---

#### **1. `psycopg2` (Legacy)**
- The most widely used PostgreSQL adapter for Python.
- **Synchronous/blocking** operations.
- Stable and mature, but **no longer actively developed** (only bug fixes).
- Compatible with Django, Flask, and most Python ORMs.

**Use when:**  
✅ You want stability and traditional synchronous queries.  
❌ You **don't** need async support.

---

#### **2. `psycopg2-binary` (Precompiled)**
- Same as `psycopg2`, but comes with **precompiled C extensions**.
- Easier to install (no need to compile from source).
- **Not recommended for production** (can cause compatibility issues).

**Use when:**  
✅ You need an **easy installation** (e.g., local development).  
❌ **Not recommended for production** (use `psycopg2` instead).

---

#### **3. `psycopg` (New, Async)**
- **Newer version** with modern features.
- Supports **both synchronous and asynchronous** execution.
- Uses **Pythonic APIs** and **typed query parameters**.
- Actively maintained and future-proof.

**Use when:**  
✅ You need **async support** (e.g., FastAPI, async Django).  
✅ You want **future-proofing** (recommended over `psycopg2`).  
❌ **Might require code changes** if migrating from `psycopg2`.

---

#### **4. `psycopg-c` (C Extension)**
- Faster performance using **C optimizations**.
- Requires compilation, so **installation may be tricky**.
- Compatible with the new `psycopg` package.


**Use when:**  
✅ You need **high performance** PostgreSQL connections.

---

#### **Which One Should You Use?**
| Package              | Sync/Async | Recommended for Production? | Performance |
|----------------------|-----------|----------------------------|-------------|
| `psycopg2`          | Sync      | ✅ Yes, but legacy         | ⭐⭐⭐       |
| `psycopg2-binary`   | Sync      | ❌ No (only for dev)       | ⭐⭐⭐       |
| `psycopg`           | Sync/Async| ✅ Yes (modern choice)     | ⭐⭐⭐⭐      |
| `psycopg-c`         | Sync/Async| ✅ Yes (high performance)  | ⭐⭐⭐⭐⭐     |

#### **Recommendation**
- For **new projects** → **Use `psycopg`** (modern, async support, future-proof).
- For **Django, Flask, or existing projects** → **Use `psycopg2`**.
- For **local development** → **Use `psycopg2-binary`**.
- For **high performance apps** → **Use `psycopg-c`**.


### **Add the NeonDB URL to Environment Variables**
Set **`DATABASE_URL`** in your `.env` file or Railway's environment variables:
```
DATABASE_URL=postgres://username:password@host:port/dbname
```

## **Step 3: Migrate & Run Django**
Run migrations:
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

You're running the server locally, but the `migrate` command created the tables in the remote DB on Neon
