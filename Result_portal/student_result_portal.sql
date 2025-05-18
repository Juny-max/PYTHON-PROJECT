-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 17, 2025 at 05:51 PM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `student_result_portal`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('059b4a62f47a');

-- --------------------------------------------------------

--
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE IF NOT EXISTS `audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_id` int NOT NULL,
  `action` varchar(100) NOT NULL,
  `target_type` varchar(50) DEFAULT NULL,
  `target_id` int DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `details` text,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`)
) ENGINE=MyISAM AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `audit_logs`
--

INSERT INTO `audit_logs` (`id`, `admin_id`, `action`, `target_type`, `target_id`, `timestamp`, `details`) VALUES
(1, 2, 'Add Course', 'Course', 3, '2025-05-09 04:51:49', 'Added course Logical Thinking (BPS78)'),
(2, 2, 'Add Course', 'Course', 4, '2025-05-09 04:52:17', 'Added course AI learning (BNT65)'),
(3, 2, 'Enter Result', 'Result', 2, '2025-05-09 04:53:12', 'Entered result for student BPS0001827, course BNT65'),
(4, 2, 'Enter Result', 'Result', 3, '2025-05-09 04:54:45', 'Entered result for student BPS0001827, course BPS78'),
(5, 2, 'Enter Result', 'Result', 4, '2025-05-09 04:55:19', 'Entered result for student BIT0001927, course BPS78'),
(6, 2, 'Broadcast Notification', 'Student', NULL, '2025-05-09 05:13:41', 'Broadcasted notification to 3 students'),
(7, 2, 'Broadcast Notification', 'Student', NULL, '2025-05-09 05:22:22', 'Broadcasted notification to 3 students'),
(8, 2, 'Broadcast Notification', 'Student', NULL, '2025-05-09 05:25:57', 'Broadcasted notification to 3 students'),
(9, 2, 'Enter Result', 'Result', 5, '2025-05-09 05:58:30', 'Entered result for student BIT0001927, course BIT0067'),
(10, 2, 'Enter Result', 'Result', 6, '2025-05-09 06:11:34', 'Entered result for student BIT0001927, course BIT0067'),
(11, 2, 'Edit Result', 'Result', 6, '2025-05-09 06:13:14', 'Edited result for student BIT0001927, course BIT0067'),
(12, 2, 'Reset Password', 'Student', 2, '2025-05-09 06:44:15', 'Reset password for Joseph (BNS002)'),
(13, 2, 'Archive Student', 'Student', 1, '2025-05-11 05:00:40', 'Archived student Max Grip (BIT0001927)'),
(14, 2, 'Add Course', 'Course', 5, '2025-05-11 07:49:49', 'Added course fgf (vdr4t4) to program BNS'),
(15, 2, 'Delete Course', 'Course', 5, '2025-05-11 07:50:01', 'Deleted course fgf (vdr4t4)'),
(16, 2, 'Delete Course', 'Course', 2, '2025-05-11 08:47:06', 'Deleted course Python programming (BIT0067)'),
(17, 2, 'Delete Course', 'Course', 3, '2025-05-11 08:47:12', 'Deleted course Logical Thinking (BPS78)'),
(18, 2, 'Delete Course', 'Course', 4, '2025-05-11 08:47:15', 'Deleted course AI learning (BNT65)'),
(19, 2, 'Add Course', 'Course', 6, '2025-05-11 08:48:28', 'Added course Python programming (BIT0067) to program BIT'),
(20, 2, 'Add Course', 'Course', 7, '2025-05-11 08:48:44', 'Added course Logical Thinking (BPS78) to program BNS'),
(21, 2, 'Enter Result', 'Result', 1, '2025-05-11 08:54:22', 'Entered result for student BPS0001827, course BIT0067'),
(22, 2, 'Enter Result', 'Result', 2, '2025-05-11 08:55:11', 'Entered result for student BIT0001927, course BIT0067'),
(23, 2, 'Enter Result', 'Result', 3, '2025-05-11 08:55:36', 'Entered result for student BIT0001927, course BPS78'),
(24, 2, 'Delete Course', 'Course', 6, '2025-05-15 11:57:53', 'Deleted course Python programming (BIT0067)'),
(25, 2, 'Add Course', 'Course', 8, '2025-05-15 12:25:28', 'Added course Python programming (BIT0067) to program BIT'),
(26, 2, 'Send Notification', 'Student', 4, '2025-05-15 12:54:31', 'Sent notification to Agyenkwa Arthur  (BIT0001227)'),
(27, 2, 'Enter Result', 'Result', 1, '2025-05-15 17:23:23', 'Entered result for student BIT0001927, course BIT0067'),
(28, 2, 'Enter Result', 'Result', 2, '2025-05-15 17:24:03', 'Entered result for student BIT0001927, course BPS78'),
(29, 2, 'Enter Result', 'Result', 3, '2025-05-15 17:24:26', 'Entered result for student BIT0001927, course BIT0067'),
(30, 2, 'Enter Result', 'Result', 4, '2025-05-15 17:24:56', 'Entered result for student BIT0001927, course BPS78'),
(31, 2, 'Edit Student', 'Student', 1, '2025-05-15 21:01:05', 'Edited student Max Grip (BIT0001927)'),
(32, 2, 'Add Course', 'Course', 9, '2025-05-15 23:16:11', 'Added course IT PROJECT MANAGEMENT (BINT 302) to program BIT'),
(33, 2, 'Add Course', 'Course', 10, '2025-05-15 23:17:36', 'Added course DATABASE SYSTEMS II (BINT 304) to program BIT'),
(34, 2, 'Add Course', 'Course', 11, '2025-05-15 23:18:34', 'Added course DATA COMMUNICATION & COMPUTER NETWORKS II (BINT 306) to program BIT'),
(35, 2, 'Add Course', 'Course', 12, '2025-05-15 23:19:25', 'Added course RESEARCH METHODS (BINT 307) to program BIT'),
(36, 2, 'Enter Result', 'Result', 5, '2025-05-16 00:42:45', 'Entered result for student BPS0001827, course BINT 302'),
(37, 2, 'Edit Student', 'Student', 3, '2025-05-17 16:26:10', 'Edited student Micheal Ohene Asante (BPS0001827)'),
(38, 2, 'Edit Student', 'Student', 3, '2025-05-17 16:26:23', 'Edited student Micheal Ohene Asante (BPS0001827)'),
(39, 2, 'Edit Student', 'Student', 3, '2025-05-17 16:26:29', 'Edited student Micheal Ohene Asante (BPS0001827)'),
(40, 2, 'Edit Student', 'Student', 1, '2025-05-17 16:26:41', 'Edited student Max Grip (BIT0001927)'),
(41, 2, 'Edit Student', 'Student', 4, '2025-05-17 16:26:49', 'Edited student Agyenkwa Arthur  (BIT0001227)'),
(42, 2, 'Edit Student', 'Student', 1, '2025-05-17 17:31:39', 'Edited student Max Grip (BIT0001927)'),
(43, 2, 'Edit Student', 'Student', 1, '2025-05-17 17:40:54', 'Edited student Max Grip (BIT0001927)'),
(44, 2, 'Edit Student', 'Student', 1, '2025-05-17 17:41:19', 'Edited student Max Grip (BIT0001927)');

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
CREATE TABLE IF NOT EXISTS `courses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(20) NOT NULL,
  `title` varchar(100) NOT NULL,
  `credit_hours` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`id`, `code`, `title`, `credit_hours`) VALUES
(9, 'BINT 302', 'IT PROJECT MANAGEMENT', 3),
(7, 'BPS78', 'Logical Thinking', 3),
(8, 'BIT0067', 'Python programming', 3),
(10, 'BINT 304', 'DATABASE SYSTEMS II', 3),
(11, 'BINT 306', 'DATA COMMUNICATION & COMPUTER NETWORKS II', 3),
(12, 'BINT 307', 'RESEARCH METHODS', 3);

-- --------------------------------------------------------

--
-- Table structure for table `levels`
--

DROP TABLE IF EXISTS `levels`;
CREATE TABLE IF NOT EXISTS `levels` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `archived` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `levels`
--

INSERT INTO `levels` (`id`, `name`, `description`, `archived`) VALUES
(1, 'Level 100', 'First Year Students', 0),
(2, 'Level 200', 'Second Year Students', 0),
(3, 'Level 300', 'Third Year Students', 0),
(4, 'Level 400', 'Fourth Year Students', 0);

-- --------------------------------------------------------

--
-- Table structure for table `login_history`
--

DROP TABLE IF EXISTS `login_history`;
CREATE TABLE IF NOT EXISTS `login_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `ip_address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `login_history`
--

INSERT INTO `login_history` (`id`, `user_id`, `timestamp`, `ip_address`) VALUES
(1, 1, '2025-05-09 03:02:35', '127.0.0.1'),
(2, 1, '2025-05-09 04:42:09', '127.0.0.1'),
(3, 4, '2025-05-09 04:50:04', '127.0.0.1'),
(4, 2, '2025-05-09 04:50:32', '127.0.0.1'),
(5, 4, '2025-05-09 04:56:12', '127.0.0.1'),
(6, 2, '2025-05-09 05:02:06', '127.0.0.1'),
(7, 1, '2025-05-09 05:26:27', '127.0.0.1'),
(8, 2, '2025-05-09 05:32:41', '127.0.0.1'),
(9, 1, '2025-05-09 05:47:14', '127.0.0.1'),
(10, 2, '2025-05-09 05:57:00', '127.0.0.1'),
(11, 1, '2025-05-09 05:59:56', '127.0.0.1'),
(12, 2, '2025-05-09 06:10:00', '127.0.0.1'),
(13, 2, '2025-05-09 06:10:06', '127.0.0.1'),
(14, 2, '2025-05-09 06:11:58', '127.0.0.1'),
(15, 1, '2025-05-09 06:12:17', '127.0.0.1'),
(16, 2, '2025-05-09 06:12:47', '127.0.0.1'),
(17, 1, '2025-05-09 06:13:35', '127.0.0.1'),
(18, 2, '2025-05-09 06:43:27', '127.0.0.1'),
(19, 2, '2025-05-09 06:44:55', '127.0.0.1'),
(20, 3, '2025-05-09 06:47:29', '127.0.0.1'),
(21, 2, '2025-05-09 06:50:26', '127.0.0.1'),
(22, 1, '2025-05-11 04:57:55', '127.0.0.1'),
(23, 2, '2025-05-11 04:58:40', '127.0.0.1'),
(24, 1, '2025-05-11 07:16:07', '127.0.0.1'),
(25, 2, '2025-05-11 07:17:46', '127.0.0.1'),
(26, 1, '2025-05-11 08:51:54', '127.0.0.1'),
(27, 2, '2025-05-11 08:52:19', '127.0.0.1'),
(28, 1, '2025-05-11 08:56:08', '127.0.0.1'),
(29, 2, '2025-05-11 08:56:45', '127.0.0.1'),
(30, 1, '2025-05-15 11:55:23', '127.0.0.1'),
(31, 2, '2025-05-15 11:56:34', '127.0.0.1'),
(32, 5, '2025-05-15 12:52:34', '127.0.0.1'),
(33, 2, '2025-05-15 12:53:43', '127.0.0.1'),
(34, 1, '2025-05-15 16:57:18', '127.0.0.1'),
(35, 4, '2025-05-15 16:58:13', '127.0.0.1'),
(36, 1, '2025-05-15 17:13:16', '127.0.0.1'),
(37, 2, '2025-05-15 17:21:09', '127.0.0.1'),
(38, 1, '2025-05-15 17:25:17', '127.0.0.1'),
(39, 2, '2025-05-15 17:40:14', '127.0.0.1'),
(40, 1, '2025-05-15 17:45:16', '127.0.0.1'),
(41, 2, '2025-05-15 17:47:03', '127.0.0.1'),
(42, 1, '2025-05-15 17:59:36', '127.0.0.1'),
(43, 1, '2025-05-15 18:06:06', '127.0.0.1'),
(44, 2, '2025-05-15 18:06:47', '127.0.0.1'),
(45, 5, '2025-05-15 18:07:59', '127.0.0.1'),
(46, 2, '2025-05-15 18:08:36', '127.0.0.1'),
(47, 1, '2025-05-15 21:01:41', '127.0.0.1'),
(48, 2, '2025-05-15 21:26:30', '127.0.0.1'),
(49, 1, '2025-05-15 21:38:20', '127.0.0.1'),
(50, 2, '2025-05-15 21:43:50', '127.0.0.1'),
(51, 2, '2025-05-15 22:05:31', '127.0.0.1'),
(52, 1, '2025-05-15 22:21:14', '127.0.0.1'),
(53, 1, '2025-05-15 22:28:25', '127.0.0.1'),
(54, 2, '2025-05-15 22:31:12', '127.0.0.1'),
(55, 1, '2025-05-16 00:53:30', '127.0.0.1'),
(56, 2, '2025-05-16 01:17:08', '127.0.0.1'),
(57, 4, '2025-05-16 16:54:18', '127.0.0.1'),
(58, 2, '2025-05-16 16:54:57', '127.0.0.1'),
(59, 4, '2025-05-16 16:55:55', '127.0.0.1'),
(60, 2, '2025-05-16 16:57:51', '127.0.0.1'),
(61, 2, '2025-05-17 15:36:39', '127.0.0.1');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
CREATE TABLE IF NOT EXISTS `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`id`, `user_id`, `message`, `is_read`, `created_at`) VALUES
(1, 1, 'Good morning students, Exams will be held tomorrow at 9:00 am', 0, '2025-05-09 05:13:41'),
(2, 3, 'Good morning students, Exams will be held tomorrow at 9:00 am', 0, '2025-05-09 05:13:41'),
(3, 4, 'Good morning students, Exams will be held tomorrow at 9:00 am', 0, '2025-05-09 05:13:41'),
(4, 1, 'Also make sure you done cheat', 0, '2025-05-09 05:22:22'),
(5, 3, 'Also make sure you done cheat', 0, '2025-05-09 05:22:22'),
(6, 4, 'Also make sure you done cheat', 0, '2025-05-09 05:22:22'),
(7, 1, 'Learn', 0, '2025-05-09 05:25:57'),
(8, 3, 'Learn', 0, '2025-05-09 05:25:57'),
(9, 4, 'Learn', 0, '2025-05-09 05:25:57'),
(10, 5, 'Hello', 0, '2025-05-15 12:54:31');

-- --------------------------------------------------------

--
-- Table structure for table `programs`
--

DROP TABLE IF EXISTS `programs`;
CREATE TABLE IF NOT EXISTS `programs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `archived` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `programs`
--

INSERT INTO `programs` (`id`, `name`, `description`, `archived`) VALUES
(1, 'Bsc Information Technology', 'Info Tech', 0),
(2, 'BNS', 'Marine', 0),
(3, 'Ports and Shipping', 'Sea Fairing', 0),
(4, 'Logistics', 'Transportation', 0);

-- --------------------------------------------------------

--
-- Table structure for table `program_courses`
--

DROP TABLE IF EXISTS `program_courses`;
CREATE TABLE IF NOT EXISTS `program_courses` (
  `program_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`program_id`,`course_id`),
  KEY `course_id` (`course_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `program_courses`
--

INSERT INTO `program_courses` (`program_id`, `course_id`) VALUES
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(2, 7),
(3, 7);

-- --------------------------------------------------------

--
-- Table structure for table `results`
--

DROP TABLE IF EXISTS `results`;
CREATE TABLE IF NOT EXISTS `results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `course_id` int NOT NULL,
  `score` decimal(5,2) NOT NULL,
  `grade` varchar(2) NOT NULL,
  `semester` varchar(20) NOT NULL,
  `academic_year` varchar(20) NOT NULL,
  `remarks` text,
  `uploaded_by` int NOT NULL,
  `uploaded_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `course_id` (`course_id`),
  KEY `student_id` (`student_id`),
  KEY `uploaded_by` (`uploaded_by`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `results`
--

INSERT INTO `results` (`id`, `student_id`, `course_id`, `score`, `grade`, `semester`, `academic_year`, `remarks`, `uploaded_by`, `uploaded_at`) VALUES
(1, 1, 8, 45.00, 'D', '1', '1', 'Learn', 2, '2025-05-15 17:23:23'),
(2, 1, 7, 78.00, 'A-', '2', '1', 'good', 2, '2025-05-15 17:24:03'),
(3, 1, 8, 56.00, 'C+', '1', '2', 'learn', 2, '2025-05-15 17:24:26'),
(4, 1, 7, 99.00, 'A', '2', '2', 'read', 2, '2025-05-15 17:24:56'),
(5, 3, 9, 34.00, 'F', '1', '1', 'hot', 2, '2025-05-16 00:42:45');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
CREATE TABLE IF NOT EXISTS `students` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `index_number` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `program_id` int NOT NULL,
  `level` varchar(20) NOT NULL,
  `archived` tinyint(1) NOT NULL DEFAULT '0',
  `level_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `index_number` (`index_number`),
  KEY `idx_program_id` (`program_id`),
  KEY `fk_level_id` (`level_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `user_id`, `index_number`, `full_name`, `program_id`, `level`, `archived`, `level_id`) VALUES
(1, 1, 'BIT0001927', 'Max Grip', 1, '200', 0, 4),
(3, 4, 'BPS0001827', 'Micheal Ohene Asante', 1, '400', 0, 2),
(4, 5, 'BIT0001227', 'Agyenkwa Arthur ', 1, '100', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `user_type` enum('admin','student') NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `user_type`, `created_at`) VALUES
(1, 'max', 'maxgrip500@gmail.com', 'pbkdf2:sha256:1000000$7PkqW6s142WatTxK$0697ee2cbaa627967b2b80589394063736a35d9941bed59ab2ab5df57a7a4ac9', 'student', '2025-05-08 23:41:45'),
(2, 'admin', 'admin@example.com', 'pbkdf2:sha256:1000000$UejAFBDMqfgWixqC$2c8362ea040698b7244f3b52b0b08706c581b7ad8b78df751d1eb367e3e91d25', 'admin', '2025-05-09 00:01:33'),
(3, 'BNS002', 'BNS002@student.portal', 'pbkdf2:sha256:1000000$Dy9BaNUZXKQKnXrh$026300fd745789cb04a9c2246d25e4c5d8c80a3c377a78a93890def79ece8140', 'student', '2025-05-09 01:31:25'),
(4, 'Micheal', 'asantemichael044@gmail.com', 'pbkdf2:sha256:1000000$yMQZRAH71zRK7nsk$d0fda459391c171c5d77b94b267aaac277229d85e27b4e37bb4319de499dd4d0', 'student', '2025-05-09 04:49:38'),
(5, 'agyenkwa', 'agyenkwa@st.rmu.edu.gh', 'pbkdf2:sha256:1000000$4bH2bwcIePof0Yuo$0afaed5db05761e4d06b22d4e04192f3351042db86c609650d9a972bb10c6778', 'student', '2025-05-15 12:52:07');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
