# Тестовое задание для Lexicom

## Запуск приложения

Требуется предварительно установленный Python версии 3.10 и выше,
а также Poetry!

1. Создать виртуальное окружение и установить библиотеки командой

```sh
poetry install
```

2. Войти в виртуальное окружение

```sh
poetry shell
```

3. Продублировать файл **example.env**, переименовать в **.env**, при необходимости
   изменить настройки приложения.
4. Запустить через файл **main.py**.

## Скрипт для PostgreSQL

```sql
-- создаём таблицы
CREATE TABLE short_names (
	name VARCHAR(64),
	status BOOLEAN
);

CREATE TABLE full_names (
	name VARCHAR(64),
	status BOOLEAN
);

-- заполняем тестовыми данными таблицы
INSERT INTO short_names (name, status)
SELECT
	md5(random()::text) AS name, random() > 0.5 as status
FROM generate_series(1, 700000);

INSERT INTO full_names (name)
SELECT
	concat(name, '.mp3')
FROM short_names
OFFSET 200000;

-- финальные запросы на заполнение колонки status в таблице full_names

-- 1, самый долгий запрос
UPDATE full_names SET status = name_status.status
FROM (
	SELECT
		fn.name AS name, sn.status AS status
	FROM full_names AS fn
	JOIN short_names as sn ON fn.name LIKE concat(sn.name, '._%')
) AS name_status
WHERE full_names.name = name_status.name;

-- 2, лучше, чем 1, но работает медленно из-за регулярного выражения
UPDATE full_names AS fn SET status = sn.status
FROM short_names AS sn
WHERE fn.name LIKE concat(sn.name, '._%');

-- 3, самый быстрый
UPDATE full_names AS fn SET status = sn.status
FROM (
	SELECT SPLIT_PART(name, '.', 1) AS name, status
	FROM short_names
) AS sn
WHERE fn.name = sn.name;
```