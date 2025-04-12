# Завдання 1 - Обробка даних сенсорів
Цей файл містить скрипт для обробки даних з сенсорів аналізуючи "BIG" повідомлення, виводить деталі помилок на основі отриманих результатів
- [Обробка даних сенсорів](#завдання-1---обробка-даних-сенсорів])
  - [Опис](#опис)
  - [Використання](#використання)
  - [Результати](#результати)
- [Тести для CheckQr](#завдання-2-)
  - [Опис тестів](#опис-тестів)
  - [Використання](#використання-)
## Опис
Програма призначена для обробки журналів з повідомленнями, що містять інформацію про стан датчиків. Вона виконує наступні основні операції:
- Відфільтровує важливу для нас інформацію
  - HANDLER 
  - ID 
  - Стан
  - Першу частину флагів стану
  - Другу частину флагів стану
- Аналізує помилку датчику на основі флагів стану
- Виводить кількість повідомлень, та інформацію про помилки
## Використання
1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/DimaFedor/ajax_task
   ```
2. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```
3. Перейдіть до директорії першого завдання:
   ```bash
   cd first_task
   ```
4. Помістіть файл з логами в дерикторію з скриптом
5. За потреби змініть назву файлу на 134 стрічці коду
    ```bash
   134. processor.process_file('Шлях до файлу з логами')
   # За замовчуванням так:
   134. processor.process_file('app_2.log')
   ```
6. Запустити скрипт
    ```bash
   python3 do_it_yourself.py
   ```
## Результати
- `ALL big messages` - Кількість повідомлень з хендлером "BIG"
- `BIG messages (distinct sensors)` - Кількість унікальних датчиків, які згенерували "BIG" повідомлення
- `Successful big messages` - Кількість успішних датчиків, які протягом усього циклу не мали помилок
- `Failed big messages` - Кількість датчиків, які мають помилки(неуспішні)
- Деталі помилок сенсорів:
  - `ID: ERROR(Battery device error, Temperature device error, Threshold central error)` - ідентифікатор датчика: тип помилки відповідно
- `Success messages count` - Кількість успішних повідомлень для кожного датчика 


# Завдання 2 - Тести для CheckQr
Тести перевіряють різні сценарії обробки, включаючи перевірку кольору на основі довжини QR-коду, перевірку наявності QR-коду в базі даних та коректну обробку помилок.
## Опис тестів
- `test_color_success`
  - Перевіряє чи програма призначає правильний колір залежно від довжини QR коду
  - Перевіряє чи метод `can_add_device` правильно призначає повідомлення`('hallelujah len(qr)')`
- `test_check_len_color_fail`
  - Перевіряє поведінку програми, коли вказана довжина, яка не відповідає жодному кольору
  - Перевіряє чи метод `send_error` правильно призначає повідомлення`('Wrong QR length len(qr)')`
- `test_qr_not_in_db`
  - Перевіряє поведінку програми, коли QR має правильну довжину, але не знайдений в БД 
  - Перевіряє чи метод `send_error` правильно призначає повідомлення(`'Not in DB'`)
- `test_successful_scan` 
  - Перевіряє повністю успішний сценарій
    - QR правильної довжини
    - QR є в БД 
    - `can_add_device` правильно призначає повідомлення`('hallelujah len(qr)')`
## Використання 
1. Так як для перевірки першого завдання вам потрібно було клонувати репозиторій, у вас вже повинна папка під назвою `second_task`
2. Перейдіть у цю директорію
    ```bash
   cd ..  !(Якщо ви були в дерикторії first_task)!
   cd second_task
   ```
3. Запуск тестів:
     ```bash
        pytest test_name.py -v 
    ```
4. В результаті усі тести повинні бути з поміткою PASSED
    ```
   Приклад: test_name.py::test_color_success[123-Red] PASSED

   ```
