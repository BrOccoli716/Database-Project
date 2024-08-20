-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: final
-- ------------------------------------------------------
-- Server version	8.0.30

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `Account` char(3) NOT NULL,
  PRIMARY KEY (`Account`),
  CONSTRAINT `AdminFK` FOREIGN KEY (`Account`) REFERENCES `user` (`Account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('004');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `affairrequest`
--

DROP TABLE IF EXISTS `affairrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `affairrequest` (
  `MNo` char(3) NOT NULL,
  `Account` char(3) NOT NULL,
  `State` int NOT NULL,
  `Detail` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`MNo`,`Account`),
  KEY `ARFK2_idx` (`Account`),
  CONSTRAINT `ARFK1` FOREIGN KEY (`MNo`) REFERENCES `match` (`MNo`),
  CONSTRAINT `ARFK2` FOREIGN KEY (`Account`) REFERENCES `user` (`Account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `affairrequest`
--

LOCK TABLES `affairrequest` WRITE;
/*!40000 ALTER TABLE `affairrequest` DISABLE KEYS */;
INSERT INTO `affairrequest` VALUES ('M02','099',1,'计时');
/*!40000 ALTER TABLE `affairrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audience`
--

DROP TABLE IF EXISTS `audience`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audience` (
  `Account` char(3) NOT NULL,
  PRIMARY KEY (`Account`),
  CONSTRAINT `AudienceFK` FOREIGN KEY (`Account`) REFERENCES `user` (`Account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audience`
--

LOCK TABLES `audience` WRITE;
/*!40000 ALTER TABLE `audience` DISABLE KEYS */;
INSERT INTO `audience` VALUES ('001'),('003'),('099');
/*!40000 ALTER TABLE `audience` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `court`
--

DROP TABLE IF EXISTS `court`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `court` (
  `CNo` char(3) NOT NULL,
  `CName` varchar(7) NOT NULL,
  `Position` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`CNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `court`
--

LOCK TABLES `court` WRITE;
/*!40000 ALTER TABLE `court` DISABLE KEYS */;
INSERT INTO `court` VALUES ('C01','斯台普斯球馆','洛杉矶'),('C02','紫荆篮球场','清华大学'),('C03','八万人体育场','上海'),('C04','大通中心','旧金山');
/*!40000 ALTER TABLE `court` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guestmatch`
--

DROP TABLE IF EXISTS `guestmatch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `guestmatch` (
  `GuestMatchNo` char(3) NOT NULL,
  `GuestTeamNo` char(3) NOT NULL,
  `Score` int NOT NULL,
  `result` char(1) NOT NULL,
  PRIMARY KEY (`GuestMatchNo`,`GuestTeamNo`),
  KEY `GuestMatchFK2_idx` (`GuestTeamNo`),
  CONSTRAINT `GuestMatchFK1` FOREIGN KEY (`GuestMatchNo`) REFERENCES `match` (`MNo`),
  CONSTRAINT `GuestMatchFK2` FOREIGN KEY (`GuestTeamNo`) REFERENCES `team` (`TNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guestmatch`
--

LOCK TABLES `guestmatch` WRITE;
/*!40000 ALTER TABLE `guestmatch` DISABLE KEYS */;
INSERT INTO `guestmatch` VALUES ('M01','T02',50,'W'),('M02','T02',58,'L'),('M03','T03',0,'N'),('M06','T04',0,'N');
/*!40000 ALTER TABLE `guestmatch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `homematch`
--

DROP TABLE IF EXISTS `homematch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `homematch` (
  `HomeMatchNo` char(3) NOT NULL,
  `HomeTeamNo` char(3) NOT NULL,
  `Score` int NOT NULL,
  `Result` char(3) NOT NULL,
  PRIMARY KEY (`HomeMatchNo`,`HomeTeamNo`),
  KEY `HomeMatchFK2_idx` (`HomeTeamNo`),
  CONSTRAINT `HomeMatchFK1` FOREIGN KEY (`HomeMatchNo`) REFERENCES `match` (`MNo`),
  CONSTRAINT `HomeMatchFK2` FOREIGN KEY (`HomeTeamNo`) REFERENCES `team` (`TNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homematch`
--

LOCK TABLES `homematch` WRITE;
/*!40000 ALTER TABLE `homematch` DISABLE KEYS */;
INSERT INTO `homematch` VALUES ('M01','T01',48,'L'),('M02','T03',60,'W'),('M03','T04',0,'N'),('M06','T02',0,'N');
/*!40000 ALTER TABLE `homematch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `INo` char(3) NOT NULL,
  `IName` varchar(5) NOT NULL,
  `Storage` int NOT NULL,
  `Price` int NOT NULL,
  PRIMARY KEY (`INo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES ('I01','水杯',90,30),('I02','头带',60,25),('I03','篮球',35,250),('I04','毛巾',70,40);
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemdeal`
--

DROP TABLE IF EXISTS `itemdeal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemdeal` (
  `IDNo` char(4) NOT NULL,
  `Date` varchar(40) NOT NULL,
  `Sum` double NOT NULL,
  `Account` char(3) NOT NULL,
  PRIMARY KEY (`IDNo`),
  KEY `ItemDealFK_idx` (`Account`),
  CONSTRAINT `ItemDealFK` FOREIGN KEY (`Account`) REFERENCES `user` (`Account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemdeal`
--

LOCK TABLES `itemdeal` WRITE;
/*!40000 ALTER TABLE `itemdeal` DISABLE KEYS */;
INSERT INTO `itemdeal` VALUES ('ID01','2022-12-19 10:57:13',2400,'099');
/*!40000 ALTER TABLE `itemdeal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itemsale`
--

DROP TABLE IF EXISTS `itemsale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itemsale` (
  `INo` char(3) NOT NULL,
  `IDNo` char(4) NOT NULL,
  `Quantity` int NOT NULL,
  `Sum` double NOT NULL,
  PRIMARY KEY (`INo`,`IDNo`),
  KEY `ItemSaleFK2_idx` (`IDNo`),
  CONSTRAINT `ItemSaleFK1` FOREIGN KEY (`INo`) REFERENCES `item` (`INo`),
  CONSTRAINT `ItemSaleFK2` FOREIGN KEY (`IDNo`) REFERENCES `itemdeal` (`IDNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itemsale`
--

LOCK TABLES `itemsale` WRITE;
/*!40000 ALTER TABLE `itemsale` DISABLE KEYS */;
INSERT INTO `itemsale` VALUES ('I02','ID01',20,500),('I03','ID01',5,1500),('I04','ID01',10,400);
/*!40000 ALTER TABLE `itemsale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `match`
--

DROP TABLE IF EXISTS `match`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `match` (
  `MNo` char(3) NOT NULL,
  `Time` char(20) NOT NULL,
  `State` int NOT NULL,
  `Referee` varchar(3) NOT NULL,
  `Court` char(3) NOT NULL,
  PRIMARY KEY (`MNo`),
  KEY `MatchFK_idx` (`Court`),
  CONSTRAINT `MatchFK` FOREIGN KEY (`Court`) REFERENCES `court` (`CNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `match`
--

LOCK TABLES `match` WRITE;
/*!40000 ALTER TABLE `match` DISABLE KEYS */;
INSERT INTO `match` VALUES ('M01','12月18日23:00-01:00',1,'小王','C02'),('M02','01月12日09:00-11:00',1,'张明','C01'),('M03','01月10日09:00-11:00',0,'小李','C02'),('M06','01月12日09:00-11:00',0,'小王','C02');
/*!40000 ALTER TABLE `match` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `team`
--

DROP TABLE IF EXISTS `team`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `team` (
  `TNo` char(3) NOT NULL,
  `TName` varchar(4) NOT NULL,
  `Statistic` char(7) NOT NULL,
  `NetScore` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`TNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `team`
--

LOCK TABLES `team` WRITE;
/*!40000 ALTER TABLE `team` DISABLE KEYS */;
INSERT INTO `team` VALUES ('T01','广东','W00-L01',-2),('T02','湖人','W01-L01',0),('T03','水木10','W01-L00',2),('T04','TES','W00-L00',0);
/*!40000 ALTER TABLE `team` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teamleader`
--

DROP TABLE IF EXISTS `teamleader`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teamleader` (
  `Account` char(3) NOT NULL,
  `Team` char(3) NOT NULL,
  PRIMARY KEY (`Account`),
  KEY `TLFK2_idx` (`Team`),
  CONSTRAINT `TLFK1` FOREIGN KEY (`Account`) REFERENCES `user` (`Account`),
  CONSTRAINT `TLFK2` FOREIGN KEY (`Team`) REFERENCES `team` (`TNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teamleader`
--

LOCK TABLES `teamleader` WRITE;
/*!40000 ALTER TABLE `teamleader` DISABLE KEYS */;
INSERT INTO `teamleader` VALUES ('006','T01'),('002','T02'),('007','T03'),('005','T04');
/*!40000 ALTER TABLE `teamleader` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test` (
  `id` char(3) NOT NULL,
  `new_tablecol` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES ('a01','sb'),('a02','2'),('a03','sgada');
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timedeal`
--

DROP TABLE IF EXISTS `timedeal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timedeal` (
  `TDNo` char(4) NOT NULL,
  `OldTime` char(20) NOT NULL,
  `NewTime` char(20) NOT NULL,
  `State` int NOT NULL,
  `Match` char(3) NOT NULL,
  PRIMARY KEY (`TDNo`),
  KEY `TimeDealFK_idx` (`Match`),
  CONSTRAINT `TimeDealFK` FOREIGN KEY (`Match`) REFERENCES `match` (`MNo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timedeal`
--

LOCK TABLES `timedeal` WRITE;
/*!40000 ALTER TABLE `timedeal` DISABLE KEYS */;
/*!40000 ALTER TABLE `timedeal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timerequest`
--

DROP TABLE IF EXISTS `timerequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timerequest` (
  `MNo` char(3) NOT NULL,
  `TeamAccount` char(3) NOT NULL,
  `NewTime` char(20) NOT NULL,
  `State` int NOT NULL,
  PRIMARY KEY (`MNo`,`TeamAccount`),
  KEY `TRFK2_idx` (`TeamAccount`),
  CONSTRAINT `TRFK1` FOREIGN KEY (`MNo`) REFERENCES `match` (`MNo`),
  CONSTRAINT `TRFK2` FOREIGN KEY (`TeamAccount`) REFERENCES `user` (`Account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timerequest`
--

LOCK TABLES `timerequest` WRITE;
/*!40000 ALTER TABLE `timerequest` DISABLE KEYS */;
INSERT INTO `timerequest` VALUES ('M02','002','01月12日09:00-11:00',2);
/*!40000 ALTER TABLE `timerequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `Account` char(8) NOT NULL,
  `password` varchar(8) NOT NULL,
  `Name` varchar(10) NOT NULL,
  `Age` int DEFAULT NULL,
  `Sex` char(1) DEFAULT NULL,
  `State` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`Account`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('001','123','李大飞',26,'男',0),('002','1234','詹姆斯',37,'男',1),('003','12345','小红',128,'女',0),('004','111111','Admin',25,'男',2),('005','123456','阿水',23,'男',1),('006','006','随便',30,'女',1),('007','007','田老师',18,'女',1),('099','123456','符亦铭',20,'男',0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'final'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-12-30 15:18:36
