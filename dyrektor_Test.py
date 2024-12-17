from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import random

# Konfiguracja opcji dla Edge
options = webdriver.EdgeOptions()
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


#=============DYREKTOR===============================================================


    dyrektor = driver.find_element("xpath", "//a[contains(text(), 'Dyrektor')]")
    url = dyrektor.get_attribute("href")
    driver.get(url)
    input("Wejście na Dyrektora. Naciśnij Enter, aby kontynuować...")

    # Kliknij w obrazek nauczycieli
    instruction_image = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@src='/static/images/Tile-instr.png']"))
    )
    instruction_image.click()
    input("Kliknięto w obrazek instruktaża. Naciśnij Enter, aby zakończyć...")

    # Kliknij przycisk logowania
    Delegate_button = driver.find_element(By.XPATH, "//button[contains(text(),'Deleguj osobę')]")
    Delegate_button.click()
    input("Kliknięto przycisk Delegowanie osób. Naciśnij Enter, aby przejść dalej...")

    # Cofnij stronę
    driver.back()
    input("Strona cofnęła się. Naciśnij Enter, aby kontynuować...")

    dyrektor = driver.find_element("xpath", "//a[contains(text(), 'Dyrektor')]")
    url = dyrektor.get_attribute("href")
    driver.get(url)
    input("Wejście na Dyrektora. Naciśnij Enter, aby kontynuować...")

    # Kliknij w obrazek nauczycieli
    teacher_image = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//img[@src='/static/images/Tile-teachers.png']"))
    )
    teacher_image.click()
    input("Kliknięto w obrazek nauczycieli. Naciśnij Enter, aby zakończyć...")

    # Lista losowych danych
    first_names = ["Jan", "Marek", "Anna", "Piotr", "Katarzyna"]
    last_names = ["Kowalski", "Nowak", "Wiśniewski", "Kamiński", "Lewandowski"]
    emails = ["example1@example.com", "example2@example.com", "example3@example.com", "example4@example.com",
              "example5@example.com"]
    pesel_ids = ["92103136267", "98022754531", "63092158927", "68081321982", "89031522352"]

    # Możliwości dla 'Naucza informatyki'
    teaches_informatics_options = ["yes", "no"]

    for _ in range(1):
        # Losowanie danych
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = random.choice(emails)
        pesel_or_other_id = random.choice(pesel_ids)
        teaches_informatics = random.choice(teaches_informatics_options)

        # Wyszukaj pola i wypełnij je
        first_name_field = driver.find_element(By.NAME, "first_name")
        first_name_field.send_keys(first_name)

        last_name_field = driver.find_element(By.NAME, "last_name")
        last_name_field.send_keys(last_name)

        email_field = driver.find_element(By.NAME, "email")
        email_field.send_keys(email)

        pesel_or_other_id_field = driver.find_element(By.NAME, "pesel_or_other_id")
        pesel_or_other_id_field.send_keys(pesel_or_other_id)

        # Wybór opcji "Naucza informatyki"
        teaches_informatics_select = driver.find_element(By.NAME, "teaches_informatics")
        select = Select(teaches_informatics_select)
        select.select_by_value(teaches_informatics)  # Losowo wybiera "yes" lub "no"

        input("Naciśnij Enter, aby przejść dalej...")

        # Kliknięcie w przycisk "Wyślij zaproszenie"
        send_invitation_button = driver.find_element(By.XPATH, "//button[contains(@class, 'rap-btn') and contains(text(), 'Wyślij zaproszenie')]")
        send_invitation_button.click()
        input("Kliknięto przycisk 'Wyślij zaproszenie'. Naciśnij Enter, aby przejść do następnej iteracji...")

        # Kliknięcie w drugi przycisk "Ponów"
        repeat_button_2 = driver.find_element(By.XPATH, "(//button[contains(@class, 'btn rap-btn') and contains(text(), 'Ponów')])[1]")
        repeat_button_2.click()
        input("Kliknięto drugi przycisk 'Ponów'. Naciśnij Enter, aby kontynuować...")



        # Kliknięcie w pierwszy link zawierający ikonę edycji
        edit_link = driver.find_element(By.XPATH, "(//a[contains(@href, '/accounts/invitation_update/') and .//i[contains(@class, 'bi-pencil')]])[1]")
        edit_link.click()
        input("Kliknięto przycisk edycji. Naciśnij Enter, aby kontynuować...")


        # Zedytuj pole 'Imię' (first_name)
        first_name_field = driver.find_element(By.ID, "id_first_name")
        first_name_field.clear()  # Wyczyść istniejącą wartość
        first_name_field.send_keys("NoweImie")  # Wprowadź nową wartość
        input("Imię zaktualizowane. Naciśnij Enter, aby przejść do kolejnego pola...")

        # Zedytuj pole 'Nazwisko' (last_name)
        last_name_field = driver.find_element(By.ID, "id_last_name")
        last_name_field.clear()  # Wyczyść istniejącą wartość
        last_name_field.send_keys("NoweNazwisko")  # Wprowadź nową wartość
        input("Nazwisko zaktualizowane. Naciśnij Enter, aby przejść do kolejnego pola...")

        # Zedytuj pole 'PESEL' (pesel_or_other_id)
        pesel_field = driver.find_element(By.ID, "id_pesel_or_other_id")
        pesel_field.clear()  # Wyczyść istniejącą wartość
        pesel_field.send_keys("57100422577")  # Wprowadź nową wartość PESEL
        input("PESEL zaktualizowane. Naciśnij Enter, aby przejść do kolejnego pola...")

        # Zedytuj pole 'Czy naucza informatyki?' (teaches_informatics)
        teaches_informatics_select = Select(driver.find_element(By.ID, "id_teaches_informatics"))
        choice = random.choice(["yes", "no"])  # Losuj 'yes' lub 'no'
        teaches_informatics_select.select_by_value(choice)  # Wybierz losową opcję
        input(f"Pole 'Czy naucza informatyki?' zaktualizowane na '{choice}'. Naciśnij Enter, aby przejść do kolejnego kroku...")

        # Kliknięcie przycisku 'Zapisz' lub 'Wyślij' (jeśli istnieje)
        submit_button = driver.find_element(By.XPATH,"//button[contains(text(), 'Zapisz')]")  # Zmienny tekst na "Wyślij"
        submit_button.click()
        input("Formularz wysłany. Naciśnij Enter, aby kontynuować...")

        # Kliknięcie przycisku 'Zapisz' lub 'Wyślij' (jeśli istnieje)
        raport_button = driver.find_element(By.XPATH,"//button[contains(text(), 'Raport PDF')]")  # Zmienny tekst na "Wyślij"
        raport_button.click()
        input("raport otrzymany . Naciśnij Enter, aby kontynuować...")



except Exception as e:
    print("Wystąpił błąd:", e)

finally:
    driver.quit()
    input("Przeglądarka została zamknięta. Naciśnij Enter, aby zakończyć program.")
