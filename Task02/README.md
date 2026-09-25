# Лабораторная работа 2. Подготовка скриптов для создания таблиц и добавления данных

## Описание работы

Утилита выполняет **ETL-процесс**: читает исходные данные из каталога `dataset`, генерирует SQL-скрипт `db_init.sql` и загружает его в базу данных SQLite `movies_rating.db`.

---

## Файлы в каталоге Task02

### Скрипты

- **`make_db_init.py`** — скрипт на Python. Читает данные из `dataset` и создаёт файл `db_init.sql` с командами `CREATE TABLE` и `INSERT INTO`.
- **`db_init.bat`** — shell-скрипт. Содержит две команды:
  1. `python make_db_init.py`
  2. `sqlite3 movies_rating.db < db_init.sql`

### Результаты

- **`db_init.sql`** — сгенерированный SQL-скрипт.
- **`movies_rating.db`** — база данных SQLite.

### Исходные данные

- **`genres.txt`** — список жанров фильмов, по одному на строку.
- **`movies.csv`** — информация о фильмах. Колонки: `movieId`, `title`, `genres`.
- **`occupation.txt`** — список профессий пользователей, по одной на строку.
- **`ratings.csv`** — оценки пользователей. Колонки: `userId`, `movieId`, `rating`, `timestamp`.
- **`tags.csv`** — теги пользователей. Колонки: `userId`, `movieId`, `tag`, `timestamp`.
- **`users.txt`** — данные пользователей, разделитель `|`. Поля: `userId`, `name`, `email`, `gender`, `register_date`, `occupation`.

---

## Структура базы данных movies_rating.db

- **movies** — id, title, year, genres
- **ratings** — id, user_id, movie_id, rating, timestamp
- **tags** — id, user_id, movie_id, tag, timestamp
- **users** — id, name, email, gender, register_date, occupation

---

## Требования к окружению

Для работы `db_init.bat` должны быть установлены:

- **Python 3** — проверка: `python --version`
- **SQLite**, утилита `sqlite3` — проверка: `sqlite3 --version`.  
  Утилита `sqlite3` должна быть доступна в `PATH`.

---

## Как запустить

Из каталога `Task02` выполнить:

```bash
./db_init.bat
```

После выполнения появится заполненная база данных `movies_rating.db`.
