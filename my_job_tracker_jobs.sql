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
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `job_id` int NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `job_title` varchar(100) NOT NULL,
  `job_type` enum('Full-time','Part-time','Contract','Internship') NOT NULL,
  `salary_min` decimal(10,2) NOT NULL,
  `salary_max` decimal(10,2) NOT NULL,
  `job_url` varchar(300) NOT NULL,
  `date_posted` date NOT NULL,
  `requirements` json DEFAULT NULL,
  PRIMARY KEY (`job_id`),
  KEY `jobs_ibfk_1` (`company_id`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (92,38,'Backend Engineer','Full-time',110000.00,150000.00,'https://technova.example.com/careers/be','2026-03-01','[{\"level\": \"3+ years\", \"skill\": \"Python\"}, {\"level\": \"2+ years\", \"skill\": \"Flask\"}, {\"level\": \"2+ years\", \"skill\": \"SQL\"}]'),(93,38,'ML Engineer','Full-time',130000.00,170000.00,'https://technova.example.com/careers/ml','2026-03-05','[{\"level\": \"4+ years\", \"skill\": \"Python\"}, {\"level\": \"2+ years\", \"skill\": \"PyTorch\"}, {\"level\": \"1+ year\", \"skill\": \"Docker\"}]'),(94,39,'Data Engineer','Full-time',120000.00,155000.00,'https://datastream.example.com/careers/de','2026-03-02','[{\"level\": \"3+ years\", \"skill\": \"Python\"}, {\"level\": \"2+ years\", \"skill\": \"Spark\"}, {\"level\": \"2+ years\", \"skill\": \"AWS\"}]'),(95,39,'Frontend Developer','Contract',90000.00,120000.00,'https://datastream.example.com/careers/fe','2026-03-10','[{\"level\": \"3+ years\", \"skill\": \"React\"}, {\"level\": \"2+ years\", \"skill\": \"TypeScript\"}]'),(96,40,'Full-Stack Developer','Full-time',100000.00,140000.00,'https://greenleaf.example.com/careers/fsd','2026-03-03','[{\"level\": \"2+ years\", \"skill\": \"Python\"}, {\"level\": \"2+ years\", \"skill\": \"React\"}, {\"level\": \"1+ year\", \"skill\": \"PostgreSQL\"}]'),(97,41,'Software Engineer','Full-time',125000.00,165000.00,'https://finedge.example.com/careers/se','2026-03-04','[{\"level\": \"3+ years\", \"skill\": \"Java\"}, {\"level\": \"2+ years\", \"skill\": \"Spring Boot\"}, {\"level\": \"2+ years\", \"skill\": \"SQL\"}]'),(98,41,'DevOps Engineer','Full-time',115000.00,150000.00,'https://finedge.example.com/careers/devops','2026-03-12','[{\"level\": \"2+ years\", \"skill\": \"Terraform\"}, {\"level\": \"3+ years\", \"skill\": \"AWS\"}, {\"level\": \"2+ years\", \"skill\": \"Docker\"}]'),(99,42,'Cloud Architect','Full-time',140000.00,190000.00,'https://cloudsphere.example.com/careers/ca','2026-03-06','[{\"level\": \"5+ years\", \"skill\": \"AWS\"}, {\"level\": \"3+ years\", \"skill\": \"Kubernetes\"}]'),(100,43,'Web Developer','Part-time',50000.00,70000.00,'https://brightpath.example.com/careers/wd','2026-03-07','[{\"level\": \"2+ years\", \"skill\": \"HTML/CSS\"}, {\"level\": \"2+ years\", \"skill\": \"JavaScript\"}, {\"level\": \"1+ year\", \"skill\": \"WordPress\"}]'),(101,44,'Quantum Software Intern','Internship',40000.00,55000.00,'https://quantumbyte.example.com/careers/qsi','2026-03-08','[{\"level\": \"1+ year\", \"skill\": \"Python\"}, {\"level\": \"coursework\", \"skill\": \"Linear Algebra\"}]'),(102,45,'Python Developer','Full-time',100000.00,130000.00,'https://urbangrid.example.com/careers/pd','2026-03-09','[{\"level\": \"3+ years\", \"skill\": \"Python\"}, {\"level\": \"2+ years\", \"skill\": \"Django\"}, {\"level\": \"2+ years\", \"skill\": \"REST APIs\"}]'),(103,45,'Data Analyst','Full-time',85000.00,110000.00,'https://urbangrid.example.com/careers/da','2026-03-14','[{\"level\": \"3+ years\", \"skill\": \"SQL\"}, {\"level\": \"2+ years\", \"skill\": \"Tableau\"}, {\"level\": \"1+ year\", \"skill\": \"Python\"}]'),(104,46,'Bioinformatics Engineer','Full-time',120000.00,160000.00,'https://novapharma.example.com/careers/bio','2026-03-11','[{\"level\": \"3+ years\", \"skill\": \"Python\"}, {\"level\": \"2+ years\", \"skill\": \"R\"}, {\"level\": \"2+ years\", \"skill\": \"Genomics\"}]'),(105,47,'EdTech Platform Engineer','Full-time',95000.00,130000.00,'https://eduvault.example.com/careers/epe','2026-03-13','[{\"level\": \"2+ years\", \"skill\": \"Python\"}, {\"level\": \"1+ year\", \"skill\": \"Flask\"}, {\"level\": \"1+ year\", \"skill\": \"React\"}]'),(106,42,'Site Reliability Engineer','Full-time',130000.00,170000.00,'https://cloudsphere.example.com/careers/sre','2026-03-15','[{\"level\": \"4+ years\", \"skill\": \"Linux\"}, {\"level\": \"3+ years\", \"skill\": \"Kubernetes\"}, {\"level\": \"2+ years\", \"skill\": \"Go\"}]');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
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
