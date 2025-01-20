import json
import datetime
import os
import re

#имя файла справочника
FILE_NAME = "phonebook.json"

#загрузка справочника из файла
def load_phonebook():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
        return {
            tuple(key.split(" ")): value for key, value in data.items()
        }
    return {}

#сохранение справочника в файл
def save_phonebook(phonebook):
    formatted_phonebook = {
        f"{name} {surname}": data for (name, surname), data in phonebook.items()
    }
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(formatted_phonebook, file, ensure_ascii=False, indent=4)

#проверка имени и фамилии
def checking_name(name):
    pattern = re.compile(r'^[A-Za-z0-9\s]+$')
    return bool(pattern.match(name))

#проверка номера телефона
def checking_phone(phone):
    if phone.startswith("+7"):
        phone = "8" + phone[2:]
    if phone.isdigit() and phone.startswith("8") and len(phone) == 11:
        return phone
    return False

#проверка даты рождения
def checking_date(date):
    try:
        datetime.datetime.strptime(date, "%d.%m.%Y")
        return True
    except ValueError:
        return False

#вывод всех записей
def all_records(phonebook):
    if not phonebook:
        print("Справочник пуст.")
        return
    print("\nСПРАВОЧНИК")
    print("-" * 30)
    for (name, surname), data in phonebook.items():
        print(f"Имя: {name}")
        print(f"Фамилия: {surname}")
        print(f"Телефон: {data['phone']}")
        print(f"Дата рождения: {data['dob'] if data['dob'] else 'Не указана'}")
        print("-" * 30)

#поиск записей
def search_records(phonebook):
    print("Укажите критерии поиска. Вы можете оставить поле пустым, чтобы не учитывать его.")

    while True:
        request_name = input("Введите имя: ").strip().capitalize()
        if request_name and not checking_name(request_name):
            print("Имя может содержать только латинские буквы, цифры и пробелы.")
        else:
            break

    while True:
        request_surname = input("Введите фамилию: ").strip().capitalize()
        if request_surname and not checking_name(request_surname):
            print("Фамилия может содержать только латинские буквы, цифры и пробелы.")
        else:
            break

    while True:
        request_phone = input("Введите номер телефона (11 цифр): ").strip()
        if not request_phone:
            break
        formatted_phone = checking_phone(request_phone)
        if not formatted_phone:
            print("Номер телефона должен состоять из 11 цифр. Начало номера: '+7' или '8'")
        else:
            break

    while True:
        request_dob = input("Введите дату рождения (дд.мм.гггг): ").strip()
        if request_dob and not checking_date(request_dob):
            print("Дата рождения должна существовать и быть в формате (дд.мм.гггг).")
        else:
            break

    results = []
    for (name, surname), data in phonebook.items():
        if (
                (not request_name or name.lower() == request_name.lower()) and
                (not request_surname or surname.lower() == request_surname.lower()) and
                (not request_phone or data["phone"] == request_phone) and
                (not request_dob or data["dob"] == request_dob)
        ):
            results.append((name, surname, data))

    if results:
        print("\nНАЙДЕННЫЕ ЗАПИСИ")
        print("-" * 30)
        for name, surname, data in results:
            print(f"Имя: {name}")
            print(f"Фамилия: {surname}")
            print(f"Телефон: {data['phone']}")
            print(f"Дата рождения: {data['dob'] if data['dob'] else 'Не указана'}")
            print("-" * 30)
    else:
        print("Записи не найдены.")

#добавление новой записи
def add_record(phonebook):
    while True:
        name = input("Введите имя: ").strip().capitalize()
        if checking_name(name):
            break
        print("Имя может содержать только латинские буквы, цифры и пробелы.")

    while True:
        surname = input("Введите фамилию: ").strip().capitalize()
        if checking_name(surname):
            break
        print("Фамилия может содержать только латинские буквы, цифры и пробелы.")

    while True:
        if (name, surname) in phonebook:
            print("Запись с таким именем и фамилией уже существует.")
            print("Выберите действие")
            print("1 - Изменить существующую запись")
            print("2 - Ввести другую комбинацию имени и фамилии")
            print("3 - Вернуться к выбору команды")

            choice = input("Введите цифру: ").strip()
            if choice == "1":
                change_record(phonebook)
                save_phonebook(phonebook)
                return
            elif choice == "2":
                add_record(phonebook)
                save_phonebook(phonebook)
                return
            elif choice == "3":
                return
            else:
                print("Некорректный ввод. Попробуйте снова.")
                continue
        break

    while True:
        phone = input("Введите номер телефона (11 цифр): ").strip()
        formatted_phone = checking_phone(phone)
        if not formatted_phone:
            print("Номер телефона должен состоять из 11 цифр. Начало номера: '+7' или '8'")
        else:
            break

    while True:
        dob = input("Введите дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
        if dob and not checking_date(dob):
            print("Дата рождения должна существовать и быть в формате (дд.мм.гггг).")
        else:
            break

    phonebook[(name, surname)] = {"phone": formatted_phone, "dob": dob}
    print("Запись успешно добавлена!")

#удаление записи
def delete_record(phonebook):
    name = input("Введите имя: ").strip().capitalize()
    surname = input("Введите фамилию: ").strip().capitalize()
    if (name, surname) in phonebook:
        del phonebook[(name, surname)]
        print("Запись успешно удалена!")
    else:
        print("Запись не найдена.")

#изменение записи
def change_record(phonebook):
    current_name = input("Введите имя: ").strip().capitalize()
    current_surname = input("Введите фамилию: ").strip().capitalize()
    if (current_name, current_surname) not in phonebook:
        print("Запись не найдена.")
        return

    current_data = phonebook[(current_name, current_surname)]
    print("Текущие данные:")
    print(f"Имя: {current_name}")
    print(f"Фамилия: {current_surname}")
    print(f"Телефон: {current_data['phone']}")
    print(f"Дата рождения: {current_data['dob'] if current_data['dob'] else 'Не указана'}")

    while True:
        new_name = input("Введите новое имя или оставьте пустым: ").strip().capitalize()
        if new_name and not checking_name(new_name):
            print("Имя может содержать только латинские буквы, цифры и пробелы.")
        else:
            break

    while True:
        new_surname = input("Введите новую фамилию или оставьте пустым: ").strip().capitalize()
        if new_surname and not checking_name(new_surname):
            print("Фамилия может содержать только латинские буквы, цифры и пробелы.")
        else:
            break

    while True:
        new_phone = input("Введите новый номер телефона (11 цифр) или оставьте пустым: ").strip()
        if not new_phone:
            break
        formatted_phone = checking_phone(new_phone)
        if not formatted_phone:
            print("Номер телефона должен состоять из 11 цифр. Начало номера: '+7' или '8'")
        else:
            break

    while True:
        new_dob = input("Введите новую дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
        if new_dob and not checking_date(new_dob):
            print("Дата рождения должна существовать и быть в формате (дд.мм.гггг).")
        else:
            break

    final_name = new_name if new_name else current_name
    final_surname = new_surname if new_surname else current_surname
    final_phone = new_phone if new_phone else current_data["phone"]
    final_dob = new_dob if new_dob else current_data["dob"]

    if (current_name, current_surname) != (final_name, final_surname):
        del phonebook[(current_name, current_surname)]
    phonebook[(final_name, final_surname)] = {"phone": final_phone, "dob": final_dob}
    print("Запись успешно обновлена!")

#вывод возраста человека
def find_age(phonebook):
    name = input("Введите имя: ").strip().capitalize()
    surname = input("Введите фамилию: ").strip().capitalize()
    if (name, surname) in phonebook:
        dob = phonebook[(name, surname)]["dob"]
        if not dob:
            print("Дата рождения отсутствует.")
            return

        birth_date = datetime.datetime.strptime(dob, "%d.%m.%Y")
        today = datetime.datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        print(f"Возраст: {age} лет.")
    else:
        print("Запись не найдена.")

def main():
    phonebook = load_phonebook()
    while True:
        print("\nДоступные команды")
        print("1 - Просмотреть все записи")
        print("2 - Найти запись")
        print("3 - Добавить новую запись")
        print("4 - Удалить запись")
        print("5 - Обновить существующую запись")
        print("6 - Узнать сколько лет человеку")
        print("7 - Завершить работу программы")

        choice = input("Введите цифру: ").strip()
        if choice == "1":
            all_records(phonebook)
        elif choice == "2":
            search_records(phonebook)
        elif choice == "3":
            add_record(phonebook)
            save_phonebook(phonebook)
        elif choice == "4":
            delete_record(phonebook)
            save_phonebook(phonebook)
        elif choice == "5":
            change_record(phonebook)
            save_phonebook(phonebook)
        elif choice == "6":
            find_age(phonebook)
        elif choice == "7":
            save_phonebook(phonebook)
            print("Программа успешно завершена!")
            return
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
