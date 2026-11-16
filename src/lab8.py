import os
import sqlite3

# Працюємо у тій самій папці, де лежить скрипт lab8.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))

DB_NAME = "university.db"


def print_teachers(cursor, title):
    """Допоміжна функція для красивого виведення вмісту таблиці."""
    print(f"\n--- {title} ---")
    cursor.execute("SELECT * FROM teachers")
    rows = cursor.fetchall()
    if not rows:
        print("Таблиця порожня.")
        return
    for row in rows:
        print(
            f"ID: {row[0]} | Ім'я: {row[1]} {row[2]} | "
            f"Кафедра: {row[3]} | Посада: {row[4]} | Дата найму: {row[5]}"
        )


def main():
    conn = None
    cur = None
    try:
        # 1-2. Підключення до бази даних «Університет» (створюється автоматично)
        conn = sqlite3.connect(DB_NAME)
        print(f"Успішно підключено до бази даних '{DB_NAME}'")
        cur = conn.cursor()

        # Очищаємо таблицю перед запуском, щоб скрипт можна було запускати багато разів без помилок
        cur.execute("DROP TABLE IF EXISTS teachers")

        # 3. Створення таблиці «Викладачі» (teachers) з різними типами даних (INTEGER, VARCHAR, DATE)
        create_table_query = """
        CREATE TABLE teachers (
            id INTEGER PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            department VARCHAR(150) NOT NULL,
            position VARCHAR(100) NOT NULL,
            hire_date DATE NOT NULL
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print("Таблицю 'teachers' успішно створено.")

        # 4. Вставка принаймні 5 рядків даних
        insert_query = """
        INSERT INTO teachers (id, first_name, last_name, department, position, hire_date)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        teachers_data = [
            (1, "Олександр", "Коваленко", "Інформаційних технологій", "Професор", "2015-09-01"),
            (2, "Ірина", "Шевченко", "Кібербезпеки та комп'ютерної інженерії", "Доцент", "2018-02-15"),
            (3, "Максим", "Бондаренко", "Інформаційних технологій", "Старший викладач", "2020-09-01"),
            (4, "Наталія", "Ткаченко", "Вищої математики", "Асистент", "2023-09-01"),
            (5, "Андрій", "Мельник", "Інформаційних технологій", "Доцент", "2019-11-10"),
        ]
        cur.executemany(insert_query, teachers_data)
        conn.commit()
        print("Дані про 5 викладачів успішно додано.")
        print_teachers(cur, "Початковий список викладачів")

        # 5. Оновлення даних за певною умовою (підвищення посади для Максима Бондаренка)
        update_query = """
        UPDATE teachers
        SET position = 'Доцент'
        WHERE first_name = 'Максим' AND last_name = 'Бондаренко';
        """
        cur.execute(update_query)
        conn.commit()
        print("\nДані оновлено: Максим Бондаренко отримав посаду 'Доцент'.")

        # 6. Видалення даних за певною умовою (видалення викладача з посадою 'Асистент')
        delete_query = """
        DELETE FROM teachers
        WHERE position = 'Асистент';
        """
        cur.execute(delete_query)
        conn.commit()
        print("Дані видалено: викладача з посадою 'Асистент' видалено з бази.")
        print_teachers(cur, "Список викладачів після оновлення та видалення")

        # 7. Вибірка даних з умовою та сортуванням
        # Вибираємо викладачів кафедри 'Інформаційних технологій' і сортуємо за прізвищем за алфавітом
        select_query = """
        SELECT id, first_name, last_name, department, position, hire_date
        FROM teachers
        WHERE department = 'Інформаційних технологій'
        ORDER BY last_name ASC;
        """
        cur.execute(select_query)
        selected_teachers = cur.fetchall()

        print("\n--- Вибірка: викладачі кафедри 'Інформаційних технологій' (відсортовані за прізвищем) ---")
        for t in selected_teachers:
            print(
                f"ID: {t[0]} | {t[2]} {t[1]} | "
                f"Кафедра: {t[3]} | Посада: {t[4]} | Дата найму: {t[5]}"
            )

    except sqlite3.Error as error:
        print("Помилка під час роботи з базою даних SQLite:", error)
    except Exception as error:
        print("Непередбачена помилка:", error)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            print("\nЗ'єднання з базою даних закрито.")

    input("\nНатисніть Enter, щоб вийти...")


if __name__ == "__main__":
    main()