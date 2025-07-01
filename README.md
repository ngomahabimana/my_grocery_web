# My Grocery Web

A Flask web app to track grocery purchases with quantity, unit price, discount, and tax calculation.  
Includes item adding, editing, deleting, tax setting, and CSV export functionality.  
Styled with custom CSS and ready for deployment on Render.

---

## 🚀 Features
✅ Add grocery items (name, quantity, unit price, discount)  
✅ Edit or delete existing items  
✅ Set tax rate and see real-time tax and total calculation  
✅ Download grocery list as CSV  
✅ Simple, clean styling with CSS  

---

## 💻 Requirements
- Python 3.x
- Flask

---

## 🛠 Setup

1️⃣ Install dependencies:
```
pip install -r requirements.txt
```

2️⃣ Run the app locally:
```
python my_grocery_web.py
```
or
```
python3 my_grocery_web.py
```

Visit in your browser:
```
http://127.0.0.1:5000/
```

---

## 🌐 Deployment

You can deploy this app easily on [Render](https://render.com/):

- Connect your GitHub repo on Render  
- Use `pip install -r requirements.txt` as build command  
- Use `python my_grocery_web.py` as start command (or `gunicorn` for production)

---

## 📂 Project Structure

```
my_grocery_web.py
requirements.txt
README.md
/templates/index.html
/static/styles.css
```

---

## ✉ Author

**Your Name / GitHub Username**

---

## ⚠ Note
This app uses Flask's development server. For production, consider using `gunicorn` or similar WSGI servers.