
# 📈 Indeed Job Scraper Frontend

Welcome to the **Indeed Job Scraper Frontend**, a user-friendly Streamlit-based interface for customizing job searches on **Indeed**. This project allows you to easily configure job searches through a sleek UI and generate a downloadable Python script with all your search parameters to run the scraper locally on your machine.

---

## 📝 Features

- **Beautiful UI** powered by **Streamlit** to gather job search parameters.
- **Country selection** with pre-defined Indeed URLs.
- **Customizable job search options**, including:
  - Job title
  - Job location
  - Days since posting
  - Maximum number of jobs to scrape (up to 100)
- **Downloadable Python script** to run the scraper locally on your machine.
- Easy-to-use **CSV export option** from the frontend.
- **Lightweight and easy setup** with no scraping done on the frontend.

---

## 📦 Installation

To run the **frontend** locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/damonDevelops/Streamlit-Indeed-Scraper.git
   cd Streamlit-Indeed-Scraper
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For MacOS/Linux
   .\venv\Scripts\activate   # For Windows
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app:**

   ```bash
   streamlit run app.py
   ```

---

## 🚀 Usage

1. Open the Streamlit app in your browser (`http://localhost:8500`).
2. Select your **country**, **job title**, **location**, and **days since posting**.
3. Set the **maximum number of jobs to scrape** (default is 50, max 100).
4. Click **Generate Script** to download a Python script with your search parameters.

---

## 🛠 Technologies Used

- **Streamlit**: Frontend UI
- **Python**: Core programming language
- **Selenium**: Web scraping tool (for local script)
- **BeautifulSoup**: HTML parsing (for local script)
- **Pandas**: Data manipulation

---

## 🐛 Troubleshooting

- If the scraper fails to run, ensure that **ChromeDriver** is installed correctly. 
- Make sure all dependencies listed in `requirements.txt` are installed.

---

## 💡 Contributing

Contributions are welcome! If you find any issues or want to improve the project, feel free to submit a pull request.

---

## 🙌 Acknowledgments

Special thanks to **[@Eben001](https://github.com/Eben001/IndeedJobScraper)** for the inspiration behind this project.

---

## ☕ Support

If you found this project helpful, consider **[buying me a coffee](https://buymeacoffee.com/damonDevelops)** to show your support!
