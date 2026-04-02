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
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contacts` (
  `contact_id` int NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `contact_name` varchar(100) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `linkedin_url` varchar(200) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`contact_id`),
  KEY `contacts_ibfk_1` (`company_id`),
  CONSTRAINT `contacts_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`company_id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contacts`
--

LOCK TABLES `contacts` WRITE;
/*!40000 ALTER TABLE `contacts` DISABLE KEYS */;
INSERT INTO `contacts` VALUES (16,38,'Alice Chen','Engineering Manager','alice.chen@technova.example.com','415-555-0101','https://linkedin.com/in/alicechen','Met at PyCon 2025'),(17,38,'Bob Martinez','Senior Recruiter','bob.m@technova.example.com','415-555-0102','https://linkedin.com/in/bobmartinez','Initial phone screen contact'),(18,39,'Carol Wu','Tech Lead','carol.wu@datastream.example.com','206-555-0201','https://linkedin.com/in/carolwu','Former colleague'),(19,40,'David Okafor','VP of Engineering','david.o@greenleaf.example.com','512-555-0301','https://linkedin.com/in/davidokafor','Connected via referral'),(20,41,'Emily Rivera','Hiring Manager','emily.r@finedge.example.com','212-555-0401','https://linkedin.com/in/emilyrivera',NULL),(21,42,'Frank Kim','DevOps Lead','frank.k@cloudsphere.example.com','303-555-0501','https://linkedin.com/in/frankkim','Reached out on LinkedIn'),(22,43,'Grace Hernandez','Creative Director','grace.h@brightpath.example.com','310-555-0601',NULL,'Recruiter contacted me'),(23,44,'Hiroshi Tanaka','Research Scientist','hiroshi.t@quantumbyte.example.com','617-555-0701','https://linkedin.com/in/hiroshitanaka','Faculty advisor introduction'),(24,45,'Isabel Nguyen','Engineering Director','isabel.n@urbangrid.example.com','312-555-0801','https://linkedin.com/in/isabelnguyen',NULL),(25,46,'James Patel','Hiring Manager','james.p@novapharma.example.com','858-555-0901','https://linkedin.com/in/jamespatel','Met at BioIT conference'),(26,47,'Karen Liu','CTO','karen.l@eduvault.example.com','503-555-1001','https://linkedin.com/in/karenliu','Alumni network'),(27,39,'Bob Jones','Manager','Bob.Jones3@datastreamcorpit.com',NULL,NULL,NULL);
/*!40000 ALTER TABLE `contacts` ENABLE KEYS */;
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
