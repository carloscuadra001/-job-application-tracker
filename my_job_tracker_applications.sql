-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: my_job_tracker
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications` (
  `application_id` int NOT NULL AUTO_INCREMENT,
  `job_id` int NOT NULL,
  `application_date` date NOT NULL,
  `status` enum('Applied','Screening','Interview','Offer','Rejected','Withdrawn') DEFAULT NULL,
  `resume_version` varchar(50) NOT NULL,
  `cover_letter_sent` tinyint(1) DEFAULT '0',
  `interview_data` json DEFAULT NULL,
  PRIMARY KEY (`application_id`),
  KEY `applications_ibfk_1` (`job_id`),
  CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
INSERT INTO `applications` VALUES (13,92,'2026-03-10','Interview','v2.1',1,'{\"interviews\": [{\"date\": \"2026-03-18\", \"notes\": \"Discussed Python experience and Flask projects\", \"round\": \"Phone Screen\", \"outcome\": \"Pass\", \"interviewer\": \"Bob Martinez\"}, {\"date\": \"2026-03-25\", \"notes\": \"Live coding session scheduled\", \"round\": \"Technical\", \"outcome\": \"Pending\", \"interviewer\": \"Alice Chen\"}], \"skills_on_resume\": [{\"level\": \"5+ years\", \"skill\": \"Python\"}, {\"level\": \"3+ years\", \"skill\": \"Flask\"}, {\"level\": \"3+ years\", \"skill\": \"SQL\"}, {\"level\": \"2+ years\", \"skill\": \"Docker\"}]}'),(14,94,'2026-03-12','Screening','v2.1',1,'{\"interviews\": [{\"date\": \"2026-04-08\", \"notes\": \"notes\", \"round\": \"Phone Screen\", \"outcome\": \"Pass\", \"interviewer\": \"bob\"}, {\"date\": \"2026-04-15\", \"notes\": \"Passed Test\", \"round\": \"Technical\", \"outcome\": \"Pass\", \"interviewer\": \"Carol Wu\"}], \"skills_on_resume\": [{\"level\": \"5+ years\", \"skill\": \"Python\"}, {\"level\": \"1+ year\", \"skill\": \"Spark\"}, {\"level\": \"2+ years\", \"skill\": \"AWS\"}, {\"level\": \"3+ years\", \"skill\": \"SQL\"}]}'),(15,96,'2026-03-08','Offer','v2.0',1,'{\"interviews\": [{\"date\": \"2026-03-14\", \"notes\": \"Great culture fit discussion\", \"round\": \"Phone Screen\", \"outcome\": \"Pass\", \"interviewer\": \"David Okafor\"}, {\"date\": \"2026-03-20\", \"notes\": \"Full-stack coding challenge went well\", \"round\": \"Technical\", \"outcome\": \"Pass\", \"interviewer\": \"David Okafor\"}, {\"date\": \"2026-03-27\", \"notes\": \"Team meet-and-greet, offer pending\", \"round\": \"Final\", \"outcome\": \"Pass\", \"interviewer\": \"David Okafor\"}], \"skills_on_resume\": [{\"level\": \"5+ years\", \"skill\": \"Python\"}, {\"level\": \"2+ years\", \"skill\": \"React\"}, {\"level\": \"2+ years\", \"skill\": \"PostgreSQL\"}, {\"level\": \"3+ years\", \"skill\": \"Flask\"}]}'),(16,97,'2026-03-11','Rejected','v2.0',0,'{\"interviews\": [{\"date\": \"2026-03-17\", \"notes\": \"Standard HR screening\", \"round\": \"Phone Screen\", \"outcome\": \"Pass\", \"interviewer\": \"Emily Rivera\"}, {\"date\": \"2026-03-23\", \"notes\": \"Struggled with Java Spring Boot questions\", \"round\": \"Technical\", \"outcome\": \"Fail\", \"interviewer\": \"Emily Rivera\"}], \"skills_on_resume\": [{\"level\": \"1+ year\", \"skill\": \"Java\"}, {\"level\": \"5+ years\", \"skill\": \"Python\"}, {\"level\": \"3+ years\", \"skill\": \"SQL\"}]}'),(17,99,'2026-03-20','Applied','v2.1',1,'{\"interviews\": [], \"skills_on_resume\": [{\"level\": \"3+ years\", \"skill\": \"AWS\"}, {\"level\": \"1+ year\", \"skill\": \"Kubernetes\"}, {\"level\": \"1+ year\", \"skill\": \"Terraform\"}]}'),(18,102,'2026-03-15','Interview','v2.1',0,'{\"interviews\": [{\"date\": \"2026-03-22\", \"notes\": \"Discussed Django and REST API experience, moving to technical\", \"round\": \"Phone Screen\", \"outcome\": \"Pass\", \"interviewer\": \"Isabel Nguyen\"}], \"skills_on_resume\": [{\"level\": \"5+ years\", \"skill\": \"Python\"}, {\"level\": \"2+ years\", \"skill\": \"Django\"}, {\"level\": \"3+ years\", \"skill\": \"REST APIs\"}, {\"level\": \"3+ years\", \"skill\": \"Flask\"}]}'),(19,105,'2026-03-28','Applied','v2.1',1,'{\"interviews\": [], \"skills_on_resume\": [{\"level\": \"5+ years\", \"skill\": \"Python\"}, {\"level\": \"3+ years\", \"skill\": \"Flask\"}, {\"level\": \"2+ years\", \"skill\": \"React\"}]}');
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-01  2:55:02
