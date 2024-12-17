from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pesel_generator import generate_random_pesel
import random
import time

# Ścieżka do pliku AdBlock .crx
adblock_path = "bloker_reklam.crx"

# Konfiguracja opcji dla Edge
options = webdriver.EdgeOptions()
options.add_extension(adblock_path)  # Dodaj rozszerzenie AdBlock

# Inicjalizacja przeglądarki Edge
driver = webdriver.Edge(options=options)


app_url = "https://admin-test.rapsteam.edu.pl/login/"
temp_mail_url = "https://10minutemail.net/"

try:
    # 1. Logowanie na konto
    driver.get(app_url)
    input("Strona logowania została otwarta. Naciśnij Enter, aby kontynuować...")
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.send_keys("167865@stud.prz.edu.pl")
    password_field.send_keys("wH!UhXoohhrNKD&")
    input("Dane logowania wprowadzone. Naciśnij Enter, aby kliknąć 'ZALOGUJ'...")

    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'ZALOGUJ')]")
    login_button.click()

    # Poczekaj na zalogowanie
    WebDriverWait(driver, 10).until(EC.url_changes(app_url))
    input("Zalogowano pomyślnie. Naciśnij Enter, aby otworzyć 10-minutową pocztę...")

    # 2. Otwórz 10-minutową pocztę w nowej karcie
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(temp_mail_url)
    try:
        # Poczekaj na pojawienie się przycisku "Consent"
        consent_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, 'fc-button-label') and text()='Consent']"))
        )
        consent_button.click()

    except Exception as e:
        print(f"Wystąpił błąd podczas klikania w przycisk 'Consent': {e}")

    input("10-minutowa poczta została otwarta. Naciśnij Enter, aby skopiować adres e-mail...")



    # Skopiuj wygenerowany adres e-mail
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fe_text"))
    )
    generated_email = email_field.get_attribute("value")
    print(f"Skopiowany e-mail: {generated_email}")
    input("E-mail został skopiowany. Naciśnij Enter, aby wrócić do aplikacji...")

    # 3. Wróć do aplikacji
    driver.switch_to.window(driver.window_handles[0])
    dyrektor = driver.find_element(By.XPATH, "//a[contains(text(), 'Dyrektor')]")
    driver.get(dyrektor.get_attribute("href"))
    input("Przejście do sekcji 'Dyrektor' zakończone. Naciśnij Enter, aby kontynuować...")

    teacher_image = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@src='/static/images/Tile-teachers.png']"))
    )
    teacher_image.click()
    input("Przejście do sekcji nauczycieli zakończone. Naciśnij Enter, aby dodać użytkownika...")

    # Wypełnij formularz dodawania użytkownika
    first_names = ["Jan", "Marek", "Anna", "Piotr", "Katarzyna"]
    last_names = ["Kowalski", "Nowak", "Wiśniewski", "Kamiński", "Lewandowski"]
    random_pesel = generate_random_pesel(start_year=1990, end_year=2000)
    print(f"Losowy PESEL: {random_pesel}")

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    pesel_or_other_id = random_pesel

    first_name_field = driver.find_element(By.NAME, "first_name")
    first_name_field.send_keys(first_name)

    last_name_field = driver.find_element(By.NAME, "last_name")
    last_name_field.send_keys(last_name)

    email_field = driver.find_element(By.NAME, "email")
    email_field.send_keys(generated_email)

    pesel_or_other_id_field = driver.find_element(By.NAME, "pesel_or_other_id")
    pesel_or_other_id_field.send_keys(pesel_or_other_id)

    teaches_informatics_select = driver.find_element(By.NAME, "teaches_informatics")
    select = Select(teaches_informatics_select)
    select.select_by_value("yes")  # Wybór "yes"

    input("Dane użytkownika wprowadzone. Naciśnij Enter, aby wysłać zaproszenie...")

    send_invitation_button = driver.find_element(By.XPATH, "//button[contains(@class, 'rap-btn') and contains(text(), 'Wyślij zaproszenie')]")
    send_invitation_button.click()
    print("Dodano użytkownika.")
    input("Naciśnij Enter, aby sprawdzić e-mail na 10-minutowej poczcie...")

    # 4. Przełącz się na kartę z 10-minutową pocztą
    driver.switch_to.window(driver.window_handles[1])
    email_subject = "RAP STEAM – Robotyka i programowanie"
    timeout = 120  # Maksymalny czas oczekiwania na maila


    def countdown(seconds):
        """Funkcja pomocnicza do odliczania czasu w konsoli."""
        for i in range(seconds, 0, -1):
            print(f"Odliczanie: {i} sekund...", end='\r')
            time.sleep(1)


    try:
        start_time = time.time()
        mail_found = False

        while not mail_found and (time.time() - start_time) < timeout:
            # Sprawdź, czy mail już jest dostępny
            try:
                email_link = driver.find_element(By.XPATH, f"//a[contains(text(), '{email_subject}')]")
                mail_found = True
            except:
                mail_found = False

            if mail_found:
                print("Mail znaleziony!")
                email_href = email_link.get_attribute("href")
                print(f"Otrzymano link do maila: {email_href}")
                input("Naciśnij Enter, aby kliknąć w nowego maila...")
                email_link.click()
                input("Naciśnij Enter, aby kliknąć w zaproszenie...")
            else:
                print("Mail nie został jeszcze znaleziony, odświeżam stronę... NIE NACISKAJ ENTERA! ")
                countdown(10)  # Odliczanie co sekundę przez 10 sekund
                refresh_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Odśwież tę stronę')]")
                refresh_button.click()
                print("Kliknięto w przycisk odświeżenia.")

        if not mail_found:
            print("Mail nie pojawił się w ciągu 60 sekund.")



        # Poczekaj na załadowanie treści maila i kliknij w przycisk 'Zaakceptuj zaproszenie'
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'accept-button')]"))
        )
        accept_button.click()
        print("Kliknięto w 'Zaakceptuj zaproszenie'.")
        driver.switch_to.window(driver.window_handles[2])
        input("Naciśnij Enter, aby przejść dalej")

        # Wypełnij pola hasła
        new_password1_field = driver.find_element(By.NAME, "new_password1")
        new_password1_field.send_keys("TwojeNoweHaslo123!")  # Wpisz nowe hasło

        new_password2_field = driver.find_element(By.NAME, "new_password2")
        new_password2_field.send_keys("TwojeNoweHaslo123!")  # Wpisz to samo hasło w pole potwierdzenia

        input("Naciśnij Enter, aby przejść dalej")

        # Kliknij przycisk "Zapisz hasło"
        save_password_button = driver.find_element(By.XPATH, "//button[contains(text(),'ZAPISZ HASŁO')]")
        save_password_button.click()
        print("Hasło zostało zapisane.")
        input("Naciśnij Enter, aby przejść dalej")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")

finally:
    driver.quit()
    print("Przeglądarka została zamknięta.")
