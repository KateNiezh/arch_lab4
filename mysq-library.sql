-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Июн 12 2017 г., 19:20
-- Версия сервера: 5.7.18-0ubuntu0.16.04.1
-- Версия PHP: 7.1.5-1+deb.sury.org~xenial+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `library`
--
CREATE DATABASE IF NOT EXISTS `library` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `library`;

-- --------------------------------------------------------

--
-- Структура таблицы `author`
--

CREATE TABLE `author` (
  `id` int(10) NOT NULL,
  `author` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `author`
--

INSERT INTO `author` (`id`, `author`) VALUES
(3, 'author111'),
(2, 'author2');

-- --------------------------------------------------------

--
-- Структура таблицы `book`
--

CREATE TABLE `book` (
  `id` int(10) NOT NULL,
  `title` varchar(100) NOT NULL,
  `genre` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `path` varchar(100) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `publication` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `book`
--

INSERT INTO `book` (`id`, `title`, `genre`, `year`, `path`, `description`, `publication`) VALUES
(9, 'book11', 'genre', 1234, 'path', 'desc', 'publ'),
(10, 'book123', 'genre', 1000, 'path', 'desc', 'publication');

-- --------------------------------------------------------

--
-- Структура таблицы `lib`
--

CREATE TABLE `lib` (
  `id` int(10) NOT NULL,
  `book` int(10) NOT NULL,
  `author` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `lib`
--

INSERT INTO `lib` (`id`, `book`, `author`) VALUES
(3, 9, 3),
(4, 10, 2);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `author`
--
ALTER TABLE `author`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `authors_author_uindex` (`author`);

--
-- Индексы таблицы `book`
--
ALTER TABLE `book`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `books_book_uindex` (`title`);

--
-- Индексы таблицы `lib`
--
ALTER TABLE `lib`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book` (`book`,`author`),
  ADD KEY `author_fk0` (`author`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `author`
--
ALTER TABLE `author`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT для таблицы `book`
--
ALTER TABLE `book`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT для таблицы `lib`
--
ALTER TABLE `lib`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `lib`
--
ALTER TABLE `lib`
  ADD CONSTRAINT `author_fk0` FOREIGN KEY (`author`) REFERENCES `author` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `book_fk0` FOREIGN KEY (`book`) REFERENCES `book` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
