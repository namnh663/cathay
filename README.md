# Selenium Automated Testing for Cathay United Bank

## 📌 Project Overview
This project automates UI testing for **Cathay United Bank** login and password reset pages using **Selenium WebDriver** with Python.

## 🚀 Features
- Automates login validation (missing credentials).
- Handles popups.
- Verifies password reset workflow.
- Ensures correct redirection for credit card users.
- Captures screenshots for UI validation.

## 📂 Project Structure
```
selenium-cathay-test/
│── pages/               # Page Object Model (POM) structure
│   └── login_page.py    # Handles login & UI interactions
│── tests/               # Test cases
│   └── test_login.py    # Main test script
│── utils/               # Helper functions
│   └── webdriver_setup.py
│── README.md            # Project documentation
│── .gitignore           # Files to ignore
│── requirements.txt     # Dependencies
```

## 🛠 Installation
### **1️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2️⃣ Run Tests**
```bash
pytest tests/test_login.py --capture=no
```

## 🎯 Technologies Used
- **Python** 🐍
- **Selenium WebDriver** 🌐
- **Pytest** 🧪

## 📸 Sample Screenshot
![Cathaybk Screenshot](Cathaybk.png)