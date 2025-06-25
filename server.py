from flask import Flask, jsonify
from flask_cors import CORS
import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

app = Flask(__name__)
CORS(app)  # <-- разрешает CORS-запросы

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

@app.route("/start", methods=["POST"])
def start_server():
    try:
        options = uc.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=options)
        driver.get("https://aternos.org/go/")

        # Переход на логин
        driver.get("https://aternos.org/login/")
        time.sleep(2)

        # Ввод email и пароля
        driver.find_element(By.NAME, "user").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(4)
        driver.get("https://aternos.org/server/")

        time.sleep(5)

        # Проверка: кнопка запуска
        start_button = driver.find_element(By.ID, "start")

        if start_button.is_enabled():
            start_button.click()
            driver.quit()
            return jsonify({"message": "Сервер запускается через Selenium!"})
        else:
            driver.quit()
            return jsonify({"message": "Сервер уже включён или неактивен."})

    except Exception as e:
        print("Ошибка:", e)
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)), debug=True)
