-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 24, 2023 at 05:14 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `lms`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(1, 'dhanushkiren99@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `desc` longtext DEFAULT NULL,
  `author` varchar(255) NOT NULL,
  `availability` tinyint(1) NOT NULL,
  `edition` varchar(255) NOT NULL,
  `count` int(11) DEFAULT NULL,
  `bookphoto` blob DEFAULT NULL,
  `subject` varchar(50) NOT NULL DEFAULT '''''',
  `publication` varchar(50) NOT NULL DEFAULT '',
  `remark` varchar(59) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `name`, `desc`, `author`, `availability`, `edition`, `count`, `bookphoto`, `subject`, `publication`, `remark`) VALUES
(1, '101 Ways To Be A Software Engineer', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut repudiandae assumenda distinctio quas tempore, voluptatibus accusamus dolores temporibus, recusandae eligendi similique. Optio, eius? Sint vel nemo, quisquam architecto fugit odio!', 'Mr. Johnny Test', 1, '1', 0, '', '\'\'', '', ''),
(2, 'JAVA For Absolute Beginners', 'Step into the basics of java programmming along with globally famed programmer', '', 1, '1', 2, '', '\'\'', '', ''),
(3, '\"Engineering Mechanics: Statics\" ', '\"Engineering Mechanics: Statics\" ', 'by J. L. Meriam and L. G. Kraige', 1, '1', 3, '', '\'\'', '', ''),
(4, '\"Engineering Mechanics: Dynamics\" ', '\"Engineering Mechanics: Dynamics\" ', 'by J. L. Meriam and L. G. Kraige', 1, '2', 12, '', '\'\'', '', ''),
(5, '\"Mechanics of Materials\" ', '\"Mechanics of Materials\" ', 'by Ferdinand P. Beer, E. Russell Johnston Jr., and John T. DeWolf', 1, '1', 4, '', '\'\'', '', ''),
(6, '\"Thermodynamics: An Engineering Approach\" ', '\"Thermodynamics: An Engineering Approach\" ', 'by Yunus A. Cengel and Michael A. Boles', 1, '1', 4, '', '\'\'', '', ''),
(7, '\"Introduction to Fluid Mechanics\" ', '\"Introduction to Fluid Mechanics\" ', 'by Robert W. Fox, Alan T. McDonald, and Philip J. Pritchard', 1, '1', 4, '', '\'\'', '', ''),
(8, '\"Heat and Mass Transfer: Fundamentals and Applications\" ', '\"Heat and Mass Transfer: Fundamentals and Applications\" ', 'by Yunus A. Cengel and Afshin J. Ghajar', 1, '1', 4, '', '\'\'', '', ''),
(9, '\"Electric Circuits\" ', '\"Electric Circuits\" ', 'by James W. Nilsson and Susan A. Riedel', 1, '1', 4, '', '\'\'', '', ''),
(10, '\"Control Systems Engineering\" ', '\"Control Systems Engineering\" ', 'by Norman S. Nise', 1, '1', 4, '', '\'\'', '', ''),
(11, '\"Mechanical Vibrations\"', '\"Mechanical Vibrations\"', 'by Singiresu S. Rao', 1, '1', 4, '', '\'\'', '', ''),
(12, '\"Introduction to Engineering\" ', '\"Introduction to Engineering\" ', 'by Paul Wright', 1, '1', 4, '', '\'\'', '', ''),
(13, 'this is to test', NULL, 'afdssfs', 0, '3939393 ', NULL, NULL, 'GN', 'asdf', 'descd'),
(14, 'this is to test', NULL, 'afdssfs', 0, '39393', NULL, NULL, 'GN', 'asdf', 'afdafdsa');

-- --------------------------------------------------------

--
-- Table structure for table `reserve`
--

CREATE TABLE `reserve` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `returned` int(11) NOT NULL DEFAULT 0,
  `issued_date` date DEFAULT NULL,
  `returned_date` date DEFAULT NULL,
  `fine_amt` int(11) DEFAULT 0,
  `delay_days` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `reserve`
--

INSERT INTO `reserve` (`id`, `user_id`, `book_id`, `returned`, `issued_date`, `returned_date`, `fine_amt`, `delay_days`) VALUES
(1, 1, 1, 1, NULL, NULL, 0, 0),
(2, 6, 1, 1, NULL, NULL, 0, 0),
(3, 7, 1, 0, NULL, NULL, 0, 0),
(4, 7, 2, 0, NULL, NULL, 0, 0),
(5, 7, 2, 0, NULL, NULL, 0, 0),
(6, 7, 1, 0, NULL, NULL, 0, 0),
(7, 7, 1, 0, NULL, NULL, 0, 0),
(8, 7, 1, 0, NULL, NULL, 0, 0),
(9, 7, 1, 0, NULL, NULL, 0, 0),
(10, 9, 2, 2, NULL, '2022-05-01', 0, 0),
(11, 9, 3, 2, '2022-03-01', '2022-05-01', 0, 0),
(12, 9, 4, 2, '2022-03-01', '2022-05-01', 0, 0),
(13, 9, 3, 2, '2022-05-01', '2022-07-31', 30, 0),
(14, 9, 11, 2, '2022-05-01', '2022-07-31', 30, 0),
(15, 9, 4, 2, '2022-05-01', '2022-07-31', 30, 0),
(16, 9, 3, 2, '2022-07-31', NULL, 0, 0),
(17, 9, 5, 2, '2022-07-31', NULL, 0, 0),
(18, 11, 6, 2, '2022-07-31', NULL, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(1000) NOT NULL,
  `bio` longtext NOT NULL,
  `mob` varchar(255) NOT NULL,
  `lock` tinyint(1) NOT NULL DEFAULT 1,
  `created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `dept` varchar(4) NOT NULL,
  `usergroup` varchar(5) NOT NULL,
  `regid` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `bio`, `mob`, `lock`, `created_at`, `dept`, `usergroup`, `regid`) VALUES
(1, 'Hamza', 'hamza@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', 'They watch you from the shelf while you sleep 👀. Are you dreaming of them, they wonder, in that wistful mood books are prone to at night when they’re bored and there’s nothing else to do but tease the cat.?', '5873985982', 1, '2021-11-09 00:00:00', '', '', ''),
(6, 'Naveed Ali', 'naveed@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', 'Hi :)! Long time no see ❤️', '5783096830', 1, '2021-11-18 23:07:53', '', '', ''),
(7, 'jaishankar', 'jaishankar.t@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', '', '3457983476', 1, '2023-02-23 09:41:02', '', '', ''),
(9, 'OM', 'dhanushkiren99@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', 'test', '5765788909', 1, '2023-02-23 13:37:44', 'None', 'None', 'None'),
(10, 'om', 'om22121999@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', '', '8709554754', 0, '2023-02-23 14:14:40', 'CS', 'S', 'cs282828'),
(11, 'gova', 'govarthinijaishankar@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', '', '', 0, '2023-04-21 19:06:45', 'CS', 'S', 'CS20221020203'),
(12, 'kumar', 'kumar@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', '', '', 1, '2023-04-22 19:52:05', 'CS', 'S', '202020');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reserve`
--
ALTER TABLE `reserve`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `reserve`
--
ALTER TABLE `reserve`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
