
 LinkedIn Auto-Apply Bot 🚀

An automated LinkedIn job application assistant built with **Python**, **Playwright**, and **SQLite**. This script searches for targeted job roles across specified locations, handles pagination, and automates both "Easy Apply" and external application forms while maintaining a safe daily application limit to protect your account.

--- ✨ Features

* **Anti-Detection Measures:** Configured with specific User-Agents and browser flags to bypass automation restrictions.
* **Smart Form Filling:** Automatically fills out standard forms (Phone, Email, City, Name) and radio buttons.
* **Cover Letter Generator:** Auto-populates standard textareas with an optimized, professional introduction.
* **Persistent Tracking:** Uses an SQLite database to remember jobs you have already applied to, preventing duplicate submissions.
* **Daily Application Cap:** Enforces a configurable safe daily limit to comply with platform guidelines.

---

## 🛠️ Prerequisites

Before running the bot, ensure you have the following installed on your system:
* **Python 3.8+**
* **Playwright** browser binaries

---

## 📦 Installation & Setup

1. **Clone the Repository** (or download the source files):
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
   cd YOUR_REPOSITORY_NAME

```
 2. **Install Required Libraries:**
   ```bash
   pip install playwright python-dotenv
   
   ```
 3. **Install Chromium Browser:**
   ```bash
   python -m playwright install chromium
   
   ```
 4. **Prepare Directory Structure:**
   Create a folder named AutoApply directly inside your C: drive and place your CV file there:
   * **Path:** C:\AutoApply\
   * **CV Name:** abdalla.pdf
## 📝 Configuration (.env)
Create a file named .env in the root directory of your project and populate it with your personal information:
```env
PHONE="+974 3084 7561"
CITY="Doha"
LINKEDIN_EMAIL="your_email@gmail.com"
SAFE_DAILY_LIMIT=40

```
## 🚀 How to Run
 1. Open your terminal or Command Prompt, and navigate to the project directory:
   ```bash
   cd C:\AutoApply
   
   ```
 2. Execute the script:
   ```bash
   python app.py
   
   ```
 3. **Manual Authentication:**
   * A non-headless Chrome window will open up.
   * Log in to your LinkedIn account manually and complete any required CAPTCHA verification.
   * Once you are on the LinkedIn homepage feed, return to your terminal and press **Enter**.
   * The bot will take over and start running automatically.
 📊 Database Logging
All successful, failed, or skipped job entries are securely logged into a local database file located at C:\AutoApply\jobs.db. A live log and final summary report will be displayed right inside your terminal interface.
 ⚠️ Disclaimer
This project is for educational and personal productivity use only. Automated interaction with LinkedIn may violate their User Agreement. Use this software responsibly and at your own risk.
```

```
