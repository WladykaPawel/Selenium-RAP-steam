from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pesel_generator import generate_random_pesel
from selenium.webdriver.common.action_chains import ActionChains
import random
import pyperclip

# Konfiguracja opcji dla Edge
options = webdriver.EdgeOptions()
driver = webdriver.Edge(options=options)


app_url = "https://admin-test.rapsteam.edu.pl/login/"
temp_mail_url = "https://adrestymczasowy.pl"

try:
    # 1. Logowanie na konto
    driver.get(app_url)
    #input("Strona logowania została otwarta. Naciśnij Enter, aby kontynuować...")
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    username_field.send_keys("167865@stud.prz.edu.pl")
    password_field.send_keys("wH!UhXoohhrNKD&")
    input("Dane logowania wprowadzone. Naciśnij Enter, aby kliknąć 'ZALOGUJ'...")

    login_button = driver.find_element(By.XPATH, "//button[contains(text(),'ZALOGUJ')]")
    login_button.click()

    # Poczekaj na zalogowanie
    WebDriverWait(driver, 10).until(EC.url_changes(app_url))
    #input("Zalogowano pomyślnie. Naciśnij Enter, aby otworzyć 10-minutową pocztę...")

    # 2. Otwórz 10-minutową pocztę w nowej karcie
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(temp_mail_url)

    try:
        # Poczekaj na pojawienie się pola z adresem e-mail
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "TempEmail"))
        )

        # Pobierz wartość atrybutu "value" z pola input
        generated_email = email_input.get_attribute("value")
        print(f"Adres e-mail został pobrany: {generated_email}")

    except Exception as e:
        print(f"Wystąpił błąd podczas pobierania adresu e-mail: {e}")

    input("10-minutowa poczta została otwarta. Naciśnij Enter, aby kontynuować...")


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
    driver.switch_to.window(driver.window_handles[1])

    # Poczekaj na pojawienie się listy e-maili i kliknij pierwszy dostępny e-mail
    email_item = WebDriverWait(driver, 120).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".list-group-item.list-group-item-action.email-list-item.mb-3"))
    )
    email_item.click()
    input("Kliknięto w pierwszy e-mail. Naciśnij Enter")

####### ZAAKCEPTOWANIE##################################

    # # Poczekaj na pojawienie się linku i kliknij w niego
    # invitation_link = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "a.url-link"))
    # )
    # invitation_link.click()
    # input("Kliknięto w link zaproszenia.")

    def accept():
        driver.switch_to.window(driver.window_handles[2])
        # Wypełnij pola hasła
        new_password1_field = driver.find_element(By.NAME, "new_password1")
        new_password1_field.send_keys("TwojeNoweHaslo123!")  # Wpisz nowe hasło

        new_password2_field = driver.find_element(By.NAME, "new_password2")
        new_password2_field.send_keys("TwojeNoweHaslo123!")  # Wpisz to samo hasło w pole potwierdzenia

        input("Naciśnij Enter, aby przejść dalej")

        # Poczekaj na przycisk "ZAPISZ HASŁO" i kliknij go
        save_password_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.btn.rap-btn.rounded-pill.rap-bg-secondary.d-flex.mx-auto.btn-lg.mt-4"))
        )
        save_password_button.click()
        input("Kliknięto przycisk 'ZAPISZ HASŁO'.")

        # Poczekaj na link "zaloguj się" i kliknij go
        login_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "zaloguj się."))
        )
        login_link.click()
        print("Kliknięto link 'zaloguj się'.")

        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(generated_email)
        password_field.send_keys("TwojeNoweHaslo123!")
        input("Dane logowania wprowadzone. Naciśnij Enter, aby kliknąć 'ZALOGUJ'...")

        login_button = driver.find_element(By.XPATH, "//button[contains(text(),'ZALOGUJ')]")
        login_button.click()

        # Poczekaj na zalogowanie
        WebDriverWait(driver, 10).until(EC.url_changes(app_url))

        # Wypełnij numer telefonu
        phone_input = driver.find_element(By.ID, "id_contact_phone")
        phone_input.send_keys("123-456-789")

        actions = ActionChains(driver)

        voivodeship_select = Select(driver.find_element(By.ID, "id_voivodeship"))
        voivodeship_select.select_by_index(0)
        voivodeship_select1 = driver.find_element(By.ID, "id_voivodeship")
        actions.click(voivodeship_select1).perform()


        # Wybierz pierwszą opcję z listy powiatów
        district_select = Select(driver.find_element(By.ID, "id_district"))
        district_select.select_by_index(0)
        district_select1 = driver.find_element(By.ID, "id_district")
        actions.click(district_select1).perform()


        # Wybierz pierwszą opcję z listy gmin
        commune_select = Select(driver.find_element(By.ID, "id_commune"))
        commune_select.select_by_index(0)
        commune_select1 = driver.find_element(By.ID, "id_commune")
        actions.click(commune_select1).perform()


        # Wybierz pierwszą opcję z listy miast
        city_select = Select(driver.find_element(By.ID, "id_city"))
        city_select.select_by_index(0)
        city_select1 = driver.find_element(By.ID, "id_city")
        actions.click(city_select1).perform()


        # Wpisz losowy kod pocztowy
        postal_code_input = driver.find_element(By.ID, "id_postalcode")
        postal_code_input.send_keys("37-100")

        # Wpisz losową ulicę i numer domu
        street_input = driver.find_element(By.ID, "id_street_with_number")
        street_input.send_keys("Kwiatowa 15")

        # Zaznacz checkbox
        agreement_checkbox = driver.find_element(By.ID, "id_agreement")
        if not agreement_checkbox.is_selected():
            agreement_checkbox.click()

        # Kliknięcie przycisku "DALEJ"
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.rap-btn.d-flex.m-auto.rap-bg-secondary"))
        )
        next_button.click()
        print("Kliknięto przycisk DALEJ.")

        # Wybór opcji na podstawie inputu użytkownika
        choice = int(
            input("Wybierz opcję:\n1 - Średniozaawansowany\n2 - Początkujący\n3 - Pomóż mi wybrać\nTwój wybór: "))

        if choice == 1:
            option_label = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='id_choice_field_1']"))
            )
            option_label.click()
            print("Kliknięto opcję: Średniozaawansowany")
        elif choice == 2:
            option_label = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='id_choice_field_0']"))
            )
            option_label.click()
            print("Kliknięto opcję: Początkujący")
        elif choice == 3:
            option_label = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='id_choice_field_2']"))
            )
            option_label.click()
            print("Kliknięto opcję: Pomóż mi wybrać")
        else:
            print("Nieprawidłowy wybór!")

        # Kliknięcie przycisku "POTWIERDŹ"
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Potwierdź')]"))
        )
        confirm_button.click()
        print("Kliknięto przycisk POTWIERDŹ.")


        # Znajdź wszystkie przyciski "DOŁĄCZ"
        join_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                 "button.btn.rap-btn.rounded-pill.rap-bg-secondary.d-flex.btn-lg.text-uppercase.m-auto"))
        )

        # Sprawdź, czy szósty przycisk ma poprawny atrybut 'name'
        if len(join_buttons) >= 6:
            sixth_button = join_buttons[5]  # Szósty przycisk (indeks 5)
            button_name = sixth_button.get_attribute("name")

            if button_name == "567456745":
                sixth_button.click()
                print("Kliknięto szósty przycisk 'DOŁĄCZ' z poprawnym name='567456745'.")
            else:
                print(f"Szósty przycisk ma nieprawidłowe name: {button_name}")
        else:
            print("Nie znaleziono sześciu przycisków 'DOŁĄCZ'!")

        # Potwierdź wybór przyciskiem "Potwierdź"
        confirm_button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].btn.rap-btn.rounded-pill.rap-bg-secondary.d-flex.m-auto.btn-lg.text-uppercase.m-2"))
        )
        confirm_button2.click()
        print("Kliknięto przycisk 'Potwierdź'.")


        input("KONIEEEECCCCCCCCCCCCCCCC...")


    def deny():
        driver.switch_to.window(driver.window_handles[2])

        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys(generated_email)
        password_field.send_keys("TwojeNoweHaslo123!")
        input("Dane logowania wprowadzone. Naciśnij Enter, aby kliknąć 'ZALOGUJ'...")

        login_button = driver.find_element(By.XPATH, "//button[contains(text(),'ZALOGUJ')]")
        login_button.click()

        # Poczekaj na zalogowanie
        WebDriverWait(driver, 10).until(EC.url_changes(app_url))

        # Wypełnij numer telefonu
        phone_input = driver.find_element(By.ID, "id_contact_phone")
        phone_input.send_keys("123-456-789")

        # Wybierz "PODKARPACKIE" z listy rozwijanej
        voivodeship_select = Select(driver.find_element(By.ID, "id_voivodeship"))
        voivodeship_select.select_by_index(0)

        # Wybierz pierwszą opcję z listy powiatów
        district_select = Select(driver.find_element(By.ID, "id_district"))
        district_select.select_by_index(0)

        # Wybierz pierwszą opcję z listy gmin
        commune_select = Select(driver.find_element(By.ID, "id_commune"))
        commune_select.select_by_index(0)

        # Wybierz pierwszą opcję z listy miast
        city_select = Select(driver.find_element(By.ID, "id_city"))
        city_select.select_by_index(0)

        # Wpisz losowy kod pocztowy
        postal_code_input = driver.find_element(By.ID, "id_postalcode")
        postal_code_input.send_keys("37-100")

        # Wpisz losową ulicę i numer domu
        street_input = driver.find_element(By.ID, "id_street_with_number")
        street_input.send_keys("Kwiatowa 15")

        # Zaznacz checkbox
        agreement_checkbox = driver.find_element(By.ID, "id_agreement")
        if not agreement_checkbox.is_selected():
            agreement_checkbox.click()

        input("KONIEEEECCCCCCCCCCCCCCCC...")



    def click_invitation_link(driver, choice):
        # Poczekaj na pojawienie się wszystkich linków z klasą 'url-link'
        invitation_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.url-link"))
        )

        # Sprawdź, czy znaleziono odpowiednią liczbę linków
        if len(invitation_links) >= 2:
            if choice == 1:
                print("Klikanie w pierwszy link (Zaakceptuj).")
                invitation_links[0].click()
                accept()
            elif choice == 2:
                print("Klikanie w drugi link (Odrzuć).")
                invitation_links[1].click()
                deny()
            else:
                print("Nieprawidłowy wybór. Wybierz 1 dla akceptacji lub 2 dla odrzucenia.")
        else:
            print("Nie znaleziono odpowiedniej liczby linków!")




    choice = int(input("Wybierz 1, aby zaakceptować zaproszenie, lub 2, aby odrzucić: "))
    click_invitation_link(driver, choice)




finally:
    driver.quit()
    print("Przeglądarka została zamknięta.")
