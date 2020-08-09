-- MariaDB dump 10.17  Distrib 10.4.13-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: scad
-- ------------------------------------------------------
-- Server version	10.4.13-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Administrador`
--

DROP TABLE IF EXISTS `Administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Administrador` (
  `Usuario` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Contrasena` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`Usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Administrador`
--

LOCK TABLES `Administrador` WRITE;
/*!40000 ALTER TABLE `Administrador` DISABLE KEYS */;
INSERT INTO `Administrador` VALUES ('brocolio','brocolio');
/*!40000 ALTER TABLE `Administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AsignacionCurso`
--

DROP TABLE IF EXISTS `AsignacionCurso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AsignacionCurso` (
  `AsignacionCursoID` int(11) NOT NULL AUTO_INCREMENT,
  `DocenteDNI` char(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `CursoNombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `SalonID` int(11) NOT NULL,
  `HoraInicio` time NOT NULL,
  `HoraFin` time NOT NULL,
  `Dia` varchar(8) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`AsignacionCursoID`),
  KEY `DocenteDNI` (`DocenteDNI`),
  KEY `CursoNombre` (`CursoNombre`),
  KEY `SalonID` (`SalonID`),
  CONSTRAINT `AsignacionCurso_ibfk_1` FOREIGN KEY (`DocenteDNI`) REFERENCES `Docente` (`DocenteDNI`),
  CONSTRAINT `AsignacionCurso_ibfk_2` FOREIGN KEY (`CursoNombre`) REFERENCES `Curso` (`CursoNombre`),
  CONSTRAINT `AsignacionCurso_ibfk_3` FOREIGN KEY (`SalonID`) REFERENCES `Salon` (`SalonID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AsignacionCurso`
--

LOCK TABLES `AsignacionCurso` WRITE;
/*!40000 ALTER TABLE `AsignacionCurso` DISABLE KEYS */;
INSERT INTO `AsignacionCurso` VALUES (1,'77675913','Logica Matematica',1,'14:00:00','16:00:00','lunes'),(2,'77675913','Estructuras Discretas 1',1,'12:00:00','14:00:00','lunes'),(4,'77675913','Estructuras Discretas 1',2,'14:00:00','16:00:00','martes'),(5,'77675913','Estructuras Discretas 1',1,'07:00:00','09:00:00','jueves'),(6,'77675913','Estructuras Discretas 1',1,'14:00:00','16:00:00','jueves'),(7,'77675913','Estructuras Discretas 2',2,'07:00:00','09:00:00','viernes'),(8,'77675913','Estructuras Discretas 2',1,'10:00:00','12:00:00','viernes'),(9,'77675913','Estructuras Discretas 2',2,'14:00:00','16:00:00','viernes'),(10,'77675913','Logica Matematica',2,'17:15:00','18:00:00','viernes');
/*!40000 ALTER TABLE `AsignacionCurso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Curso`
--

DROP TABLE IF EXISTS `Curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Curso` (
  `CursoNombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `FechaInicio` date NOT NULL,
  `FechaFin` date NOT NULL,
  PRIMARY KEY (`CursoNombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Curso`
--

LOCK TABLES `Curso` WRITE;
/*!40000 ALTER TABLE `Curso` DISABLE KEYS */;
INSERT INTO `Curso` VALUES ('Calculo en una variable','2020-10-10','2021-04-10'),('Estructuras Discretas 1','2020-10-12','2021-04-15'),('Estructuras Discretas 2','2020-10-05','2021-04-15'),('Logica Matematica','2020-10-10','2021-04-10');
/*!40000 ALTER TABLE `Curso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Docente`
--

DROP TABLE IF EXISTS `Docente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Docente` (
  `DocenteDNI` char(8) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Apellido` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Usuario` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Contrasena` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`DocenteDNI`),
  UNIQUE KEY `Usuario` (`Usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Docente`
--

LOCK TABLES `Docente` WRITE;
/*!40000 ALTER TABLE `Docente` DISABLE KEYS */;
INSERT INTO `Docente` VALUES ('12312312','Franci ','Suni Lopez','fsunilo','ella no te ama'),('47675983','Angel Jack','Manglares Marciano ','amanm','amanm'),('77675913','Luis Angel','Prado Postigo','lpradop','lpradop');
/*!40000 ALTER TABLE `Docente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Marcacion`
--

DROP TABLE IF EXISTS `Marcacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Marcacion` (
  `AsignacionCursoID` int(11) NOT NULL,
  `Fecha` date NOT NULL,
  `Hora` time NOT NULL,
  `SalonID` int(11) DEFAULT NULL,
  KEY `AsignacionCursoID` (`AsignacionCursoID`),
  KEY `SalonID` (`SalonID`),
  CONSTRAINT `Marcacion_ibfk_1` FOREIGN KEY (`AsignacionCursoID`) REFERENCES `AsignacionCurso` (`AsignacionCursoID`),
  CONSTRAINT `Marcacion_ibfk_2` FOREIGN KEY (`SalonID`) REFERENCES `Salon` (`SalonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Marcacion`
--

LOCK TABLES `Marcacion` WRITE;
/*!40000 ALTER TABLE `Marcacion` DISABLE KEYS */;
INSERT INTO `Marcacion` VALUES (5,'2020-08-06','07:10:00',1),(10,'2020-08-06','05:25:00',2),(8,'2020-08-07','10:10:00',1);
/*!40000 ALTER TABLE `Marcacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Salon`
--

DROP TABLE IF EXISTS `Salon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Salon` (
  `SalonID` int(11) NOT NULL AUTO_INCREMENT,
  `Pabellon` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Numero` char(3) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`SalonID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Salon`
--

LOCK TABLES `Salon` WRITE;
/*!40000 ALTER TABLE `Salon` DISABLE KEYS */;
INSERT INTO `Salon` VALUES (1,'Sistemas','105'),(2,'Sistemas','205'),(3,'Sistemas','305'),(4,'Electronica','205'),(5,'Electronica','105');
/*!40000 ALTER TABLE `Salon` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-08 23:46:08
