-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 29, 2024 at 08:06 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `atm_laundering`
--

-- --------------------------------------------------------

--
-- Table structure for table `predictions`
--

CREATE TABLE `predictions` (
  `id` int(11) NOT NULL,
  `type` varchar(30) NOT NULL,
  `amount` float NOT NULL,
  `oldbalanceOrg` float NOT NULL,
  `newbalanceOrig` float NOT NULL,
  `oldbalanceDest` float NOT NULL,
  `newbalanceDest` float NOT NULL,
  `isFraud` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `predictions`
--

INSERT INTO `predictions` (`id`, `type`, `amount`, `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`, `isFraud`, `userId`, `date`) VALUES
(1, 'Transfer', 100, 0, 0, 0, 0, 1, 1, '2024-06-22 21:23:21'),
(2, 'Payment', 100, 0, 0, 0, 0, 0, 1, '2024-06-21 20:41:11'),
(3, 'Debit', 90, 963, 81, 92, 0, 0, 3, '2024-06-21 21:55:49'),
(4, 'Cash In', 50, 0, 0, 100, 100, 0, 2, '2024-06-21 23:06:42'),
(5, 'Payment', 34567, 56789, 6789, 56789, 56789, 0, 1, '2024-06-21 14:32:15'),
(6, 'Transfer', 100, 187, 9, 10, 10, 1, 2, '2024-06-21 21:55:05'),
(7, 'Transfer', 100, 500, 10927, 0, 0, 1, 2, '2024-06-21 21:57:45'),
(11, 'Debit', 2024, 0, 0, 0, 0, 0, 6, '2024-06-22 18:09:23'),
(12, 'Transfer', 2000, 100, 100, 100, 100, 1, 7, '2024-06-29 05:37:07');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fullName` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `userRole` varchar(10) DEFAULT 'User',
  `joinDate` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `fullName`, `email`, `password`, `dob`, `gender`, `location`, `userRole`, `joinDate`) VALUES
(1, 'Abdullahi Khalif ', 'test@gmail.com', 'admin', '2000-05-21', 'Male', 'Howlwadaag', 'User', '2024-06-20 22:06:31'),
(2, 'Mohamed Adan', 'mohaadan@gmail.com', 'admin', '2004-12-12', 'Male', 'Ceelash Biyaha', 'User', '2024-06-20 22:13:26'),
(4, 'Ayaan Abdullahi', 'ayanah@gmail.com', 'ayaan', '2002-02-01', 'Male', 'Suuqa Xoolaha', 'Admin', '2024-06-21 19:07:44'),
(6, 'Mascuud Abirahman', 'maska1@gmail.com', 'admin', '2004-02-09', 'Male', 'Hodan', 'Admin', '2024-06-22 18:06:02'),
(7, 'Abdinasir Just', 'nasri12@gmail.com', '1299', '2001-02-03', 'Male', 'Hodan', 'Admin', '2024-06-29 05:30:47'),
(8, 'Abdinor', 'abdi@gmail.com', 'admin', '1997-01-02', 'Male', 'Ceelash Biyaha', 'User', '2024-06-29 05:38:43');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `predictions`
--
ALTER TABLE `predictions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userId` (`userId`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `predictions`
--
ALTER TABLE `predictions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
