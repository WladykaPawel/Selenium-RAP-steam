from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import random

# Konfiguracja opcji dla Edge
options = webdriver.EdgeOptions()

# Inicjalizacja przeglądarki Edge
driver = webdriver.Edge(options=options)

app_url = "https://admin-test.rapsteam.edu.pl/login/"

try:
    # Otwórz stronę logowania
    driver.get(app_url)
    input("Strona logowania została otwarta. Naciśnij Enter, aby kontynuować...")

    # Wyszukaj pola logowania i wypełnij je
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    input("Pola logowania zostały znalezione. Naciśnij Enter, aby wprowadzić dane...")

    username_field.send_keys("167865@stud.prz.edu.pl")
    password_field.send_keys("wH!UhXoohhrNKD&")
    input("Dane logowania zostały wprowadzone. Naciśnij Enter, aby kliknąć 'ZALOGUJ'...")

    # Kliknij przycisk logowania
    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'ZALOGUJ')]")
    login_button.click()
    input("Kliknięto przycisk logowania. Naciśnij Enter, aby przejść dalej...")

    # Poczekaj na zmianę URL po zalogowaniu
    WebDriverWait(driver, 10).until(EC.url_changes(app_url))


#=============TRENET===============================================================


    trener = driver.find_element("xpath", "//a[contains(text(), 'Trener')]")
    url = trener.get_attribute("href")
    driver.get(url)
    input("Wejście na Trenera. Naciśnij Enter, aby kontynuować...")

    # Kliknij w obrazek materiałów
    material_image = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@src='/static/images/Tile1.png']"))
    )
    material_image.click()
    input("Kliknięto w obrazek materiału. Naciśnij Enter, aby zakończyć...")

    # Znajdź wszystkie przyciski "Pobierz"
    download_buttons = driver.find_elements(By.CSS_SELECTOR, "a.btn.rap-btn")

    for button in download_buttons:
        # Kliknij przycisk "Pobierz"
        button.click()

        input("Kliknięto w pobierz. Naciśnij Enter, aby zakończyć...")

        # Przełącz z powrotem na główną kartę
        driver.switch_to.window(driver.window_handles[0])

        input("zamknięcie PDF. Naciśnij Enter, aby zakończyć...")


    dyrektor = driver.find_element("xpath", "//a[contains(text(), 'Trener')]")
    url = dyrektor.get_attribute("href")
    driver.get(url)
    input("Wejście na Trenera. Naciśnij Enter, aby kontynuować...")


except Exception as e:
    print("Wystąpił błąd:", e)

finally:
    driver.quit()
    input("Przeglądarka została zamknięta. Naciśnij Enter, aby zakończyć program.")
