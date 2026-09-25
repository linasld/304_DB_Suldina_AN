#!/usr/bin/env python3

import csv
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(SCRIPT_DIR, '..', 'dataset')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'db_init.sql')

BATCH_SIZE = 500


def escape(value):
    if value is None or value == '':
        return 'NULL'
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def extract_year(title):
    m = re.search(r'\((\d{4})\)\s*$', title)
    if m:
        return title[:m.start()].strip(), int(m.group(1))
    return title.strip(), None


def write_schema(f):
    f.write("PRAGMA foreign_keys = OFF;\n")
    f.write("PRAGMA synchronous = OFF;\n")
    f.write("PRAGMA journal_mode = MEMORY;\n")
    f.write("PRAGMA cache_size = 100000;\n\n")
    f.write("DROP TABLE IF EXISTS ratings;\n")
    f.write("DROP TABLE IF EXISTS tags;\n")
    f.write("DROP TABLE IF EXISTS movies;\n")
    f.write("DROP TABLE IF EXISTS users;\n\n")

    f.write("""CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER,
    genres TEXT
);

""")
    f.write("""CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL,
    timestamp INTEGER NOT NULL
);

""")
    f.write("""CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    tag TEXT,
    timestamp INTEGER NOT NULL
);

""")
    f.write("""CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    gender TEXT,
    register_date TEXT,
    occupation TEXT
);

""")


def batch_insert(f, table, columns, rows):
    prefix = f"INSERT INTO {table} ({', '.join(columns)}) VALUES "
    for i in range(0, len(rows), BATCH_SIZE):
        chunk = rows[i:i + BATCH_SIZE]
        values = ",\n".join(
            "(" + ", ".join(escape(v) for v in row) + ")" for row in chunk
        )
        f.write(prefix + values + ";\n")


def load_movies(f):
    rows = []
    with open(os.path.join(DATASET_DIR, 'movies.csv'), 'r', encoding='utf-8') as src:
        for row in csv.DictReader(src):
            title, year = extract_year(row['title'])
            rows.append((int(row['movieId']), title, year, row['genres']))
    batch_insert(f, 'movies', ['id', 'title', 'year', 'genres'], rows)


def load_ratings(f):
    rows = []
    with open(os.path.join(DATASET_DIR, 'ratings.csv'), 'r', encoding='utf-8') as src:
        for row in csv.DictReader(src):
            rows.append((int(row['userId']), int(row['movieId']),
                         float(row['rating']), int(row['timestamp'])))
    batch_insert(f, 'ratings', ['user_id', 'movie_id', 'rating', 'timestamp'], rows)


def load_tags(f):
    rows = []
    with open(os.path.join(DATASET_DIR, 'tags.csv'), 'r', encoding='utf-8') as src:
        for row in csv.DictReader(src):
            rows.append((int(row['userId']), int(row['movieId']),
                         row['tag'], int(row['timestamp'])))
    batch_insert(f, 'tags', ['user_id', 'movie_id', 'tag', 'timestamp'], rows)


def load_users(f):
    rows = []
    with open(os.path.join(DATASET_DIR, 'users.txt'), 'r', encoding='utf-8') as src:
        for line in src:
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split('|')
            if len(parts) < 6:
                continue
            rows.append((int(parts[0]), parts[1], parts[2],
                         parts[3], parts[4], parts[5]))
    batch_insert(f, 'users',
                 ['id', 'name', 'email', 'gender', 'register_date', 'occupation'],
                 rows)


def main():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        write_schema(f)
        f.write("BEGIN TRANSACTION;\n")
        load_movies(f)
        load_ratings(f)
        load_tags(f)
        load_users(f)
        f.write("COMMIT;\n")
    print(f"Generated: {OUTPUT_FILE}")


if __name__ == '__main__':
    main()

