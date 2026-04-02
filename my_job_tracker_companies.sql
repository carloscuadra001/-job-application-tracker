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
-- Table structure for table `companies`
--

DROP TABLE IF EXISTS `companies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companies` (
  `company_id` int NOT NULL AUTO_INCREMENT,
  `company_name` varchar(100) NOT NULL,
  `industry` varchar(50) NOT NULL,
  `website` varchar(200) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `notes` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`company_id`),
  KEY `idx_company_industry` (`industry`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companies`
--

LOCK TABLES `companies` WRITE;
/*!40000 ALTER TABLE `companies` DISABLE KEYS */;
INSERT INTO `companies` VALUES (38,'TechNova Inc.','Technology','https://technova.example.com','San Francisco','CA','AI startup, Series B','2026-04-01 06:27:52'),(39,'DataStream Corp.','Technology','https://datastream.example.com','Seattle','WA','Big-data analytics platform','2026-04-01 06:27:52'),(40,'GreenLeaf Solutions','Healthcare','https://greenleaf.example.com','Austin','TX','Health-tech focused on EHR','2026-04-01 06:27:52'),(41,'FinEdge Partners','Finance','https://finedge.example.com','New York','NY','Fintech, Series C','2026-04-01 06:27:52'),(42,'CloudSphere Labs','Technology','https://cloudsphere.example.com','Denver','CO','Cloud infrastructure provider','2026-04-01 06:27:52'),(43,'BrightPath Media','Media','https://brightpath.example.com','Los Angeles','CA','Digital marketing agency','2026-04-01 06:27:52'),(44,'QuantumByte Systems','Technology','https://quantumbyte.example.com','Boston','MA','Quantum computing research','2026-04-01 06:27:52'),(45,'UrbanGrid Logistics','Logistics','https://urbangrid.example.com','Chicago','IL','Last-mile delivery platform','2026-04-01 06:27:52'),(46,'NovaPharma Inc.','Healthcare','https://novapharma.example.com','San Diego','CA','Biotech, gene therapy R&D','2026-04-01 06:27:52'),(47,'EduVault Learning','Education','https://eduvault.example.com','Portland','OR','EdTech SaaS for K-12','2026-04-01 06:27:52');
/*!40000 ALTER TABLE `companies` ENABLE KEYS */;
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
