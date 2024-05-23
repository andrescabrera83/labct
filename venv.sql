-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: labct
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compras`
--

DROP TABLE IF EXISTS `compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras` (
  `id_compras` int NOT NULL AUTO_INCREMENT,
  `data_compras` datetime DEFAULT NULL,
  `estado_compras` enum('Pendente','Entregue') DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_compras`),
  KEY `fk_compras_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_compras_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras`
--

LOCK TABLES `compras` WRITE;
/*!40000 ALTER TABLE `compras` DISABLE KEYS */;
INSERT INTO `compras` VALUES (1,'2024-05-07 02:13:15','Entregue',1),(2,'2024-05-10 20:03:21','Entregue',1);
/*!40000 ALTER TABLE `compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comprasdados`
--

DROP TABLE IF EXISTS `comprasdados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comprasdados` (
  `id_comprasd` int NOT NULL AUTO_INCREMENT,
  `id_compras` int DEFAULT NULL,
  `nome_mp` varchar(75) DEFAULT NULL,
  `unidade_mp` enum('KG','UN') DEFAULT NULL,
  `pedido_comprasd` decimal(10,3) DEFAULT NULL,
  `fornecedor_comprasd` varchar(45) DEFAULT NULL,
  `valorpedido_comprasd` decimal(10,2) DEFAULT NULL,
  `departamento_comprasd` enum('Carnes','Farinhas','Hortifruti','Mercearia','Misturas','Ovos','Queijos') DEFAULT NULL,
  `previsao_comprasd` datetime DEFAULT NULL,
  `vencimento_comprasd` datetime DEFAULT NULL,
  `fechado_comprasd` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_comprasd`),
  KEY `fk_comprasdados_id_compras_compras` (`id_compras`),
  KEY `fk_comprasdados_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_comprasdados_id_compras_compras` FOREIGN KEY (`id_compras`) REFERENCES `compras` (`id_compras`),
  CONSTRAINT `fk_comprasdados_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comprasdados`
--

LOCK TABLES `comprasdados` WRITE;
/*!40000 ALTER TABLE `comprasdados` DISABLE KEYS */;
INSERT INTO `comprasdados` VALUES (1,1,'Farinha de Mandioca','KG',40.000,'PifPaf',1481.60,'Farinhas','2024-05-17 02:13:15','2024-05-28 02:13:15',1,1),(2,2,'Farinha de trigo','KG',300.000,'PifPaf',1032.00,'Farinhas','2024-05-20 20:03:21','2024-05-31 20:03:21',1,1);
/*!40000 ALTER TABLE `comprasdados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estoque`
--

DROP TABLE IF EXISTS `estoque`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estoque` (
  `id_estq` int NOT NULL AUTO_INCREMENT,
  `id_mp` int NOT NULL,
  `nome_mp` varchar(75) DEFAULT NULL,
  `unidade_mp` enum('KG','UN') DEFAULT NULL,
  `gms_mp` decimal(10,3) DEFAULT NULL,
  `pedidomin_mp` decimal(10,3) DEFAULT NULL,
  `quantidade_estq` decimal(10,3) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_estq`),
  KEY `fk_estoque_id_mp_materiasprimas` (`id_mp`),
  KEY `fk_estoque_user_id_usuarios` (`user_id`),
  KEY `fk_inventariodados_quantidade_estq_estoque` (`quantidade_estq`),
  CONSTRAINT `fk_estoque_id_mp_materiasprimas` FOREIGN KEY (`id_mp`) REFERENCES `materiasprimas` (`id_mp`),
  CONSTRAINT `fk_estoque_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estoque`
--

LOCK TABLES `estoque` WRITE;
/*!40000 ALTER TABLE `estoque` DISABLE KEYS */;
INSERT INTO `estoque` VALUES (1,1,'Farinha de Mandioca','KG',90.000,100.000,492.500,1),(2,2,'Farinha de trigo','KG',450.000,25.000,500.000,1),(3,3,'Manteiga sem sal','KG',30.000,5.000,478.000,1),(4,4,'Açúcar refinado','KG',12.000,10.000,493.000,1),(5,5,'Bandeja Isopor pequena','UN',420.000,500.000,430.000,1);
/*!40000 ALTER TABLE `estoque` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fabrica`
--

DROP TABLE IF EXISTS `fabrica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fabrica` (
  `id_fab` int NOT NULL AUTO_INCREMENT,
  `nome_fab` varchar(150) NOT NULL,
  `endereco_fab` varchar(150) NOT NULL,
  `bairro_fab` varchar(50) NOT NULL,
  `cidade_fab` varchar(50) NOT NULL,
  `estado_fab` varchar(50) NOT NULL,
  `telefone_fab` varchar(30) NOT NULL,
  `email_fab` varchar(50) NOT NULL,
  `responsavel_fab` varchar(50) NOT NULL,
  `wpp_fab` varchar(50) NOT NULL,
  `cnpj_fab` varchar(17) DEFAULT NULL,
  `status_fab` int DEFAULT NULL,
  `cadastrado_em_fab` datetime NOT NULL,
  `atualizado_em_fab` datetime DEFAULT NULL,
  PRIMARY KEY (`id_fab`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fabrica`
--

LOCK TABLES `fabrica` WRITE;
/*!40000 ALTER TABLE `fabrica` DISABLE KEYS */;
INSERT INTO `fabrica` VALUES (1,'ARCESIO CABRERA B','Calle 53AB #8299','castelo','Medellín','Antioquia','3172689228','andrescabrera192@gmail.com','fabia','3216549875','13456789564',1,'2024-05-07 02:11:28','2024-05-07 02:11:28');
/*!40000 ALTER TABLE `fabrica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `filiais`
--

DROP TABLE IF EXISTS `filiais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `filiais` (
  `id_fil` int NOT NULL AUTO_INCREMENT,
  `loja_fil` varchar(50) NOT NULL,
  `endereco_fil` varchar(50) NOT NULL,
  `bairro_fil` varchar(50) NOT NULL,
  `cidade_fil` varchar(50) NOT NULL,
  `codigorota_fil` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_fil`),
  KEY `fk_filiais_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_filiais_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `filiais`
--

LOCK TABLES `filiais` WRITE;
/*!40000 ALTER TABLE `filiais` DISABLE KEYS */;
INSERT INTO `filiais` VALUES (1,'loja dama 1','testando endereco para filiais','Aenean imperdiet. ','gfggfgfgf',1,1),(2,'loja dama 2','rua das palmeiras','uniao','belo horizonte',1,1);
/*!40000 ALTER TABLE `filiais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fornecedores`
--

DROP TABLE IF EXISTS `fornecedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fornecedores` (
  `id_fornecedor` int NOT NULL AUTO_INCREMENT,
  `nome_fornecedor` varchar(45) DEFAULT NULL,
  `tempo_entrega` int DEFAULT NULL,
  `prazo_pagamento` int DEFAULT NULL,
  `dia_pedido` enum('Segunda-Feira','Terça-Feira','Quarta-Feira','Quinta-Feira','Sexta-Feira','Sábado','Domingo') DEFAULT NULL,
  `nome_vendedor` varchar(45) DEFAULT NULL,
  `contato_tel` varchar(45) DEFAULT NULL,
  `email_vendedor` varchar(100) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_fornecedor`),
  KEY `fk_fornecedores_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_fornecedores_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fornecedores`
--

LOCK TABLES `fornecedores` WRITE;
/*!40000 ALTER TABLE `fornecedores` DISABLE KEYS */;
INSERT INTO `fornecedores` VALUES (1,'PifPaf',10,21,'Segunda-Feira','Mario','58966666','cabrera192@gmail.com',1);
/*!40000 ALTER TABLE `fornecedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giromedio`
--

DROP TABLE IF EXISTS `giromedio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giromedio` (
  `id_gm` int NOT NULL AUTO_INCREMENT,
  `giro_medio` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_gm`),
  KEY `fk_giromedio_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_giromedio_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giromedio`
--

LOCK TABLES `giromedio` WRITE;
/*!40000 ALTER TABLE `giromedio` DISABLE KEYS */;
/*!40000 ALTER TABLE `giromedio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historico`
--

DROP TABLE IF EXISTS `historico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historico` (
  `id_hst` int NOT NULL AUTO_INCREMENT,
  `date_change` datetime DEFAULT NULL,
  `id_mp` int NOT NULL,
  `nome_mp` varchar(75) DEFAULT NULL,
  `ultimaquantidade_hst` decimal(10,3) DEFAULT NULL,
  `novaquantidade_hst` decimal(10,3) DEFAULT NULL,
  `difference_hst` decimal(10,3) DEFAULT NULL,
  `modo_hst` enum('Registro Manual','Compra','Inventario','Produção') DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_hst`),
  KEY `fk_historico_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_historico_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historico`
--

LOCK TABLES `historico` WRITE;
/*!40000 ALTER TABLE `historico` DISABLE KEYS */;
INSERT INTO `historico` VALUES (1,'2024-05-07 02:12:59',1,'Farinha de Mandioca',0.000,50.000,50.000,'Registro Manual',1),(2,'2024-05-07 02:13:31',1,'Farinha de Mandioca',50.000,90.000,40.000,'Compra',1),(3,'2024-05-08 18:57:07',1,'Farinha de Mandioca',90.000,80.000,-10.000,'Produção',1),(4,'2024-05-08 23:14:23',1,'Farinha de Mandioca',80.000,75.000,-5.000,'Produção',1),(5,'2024-05-08 23:14:23',1,'Farinha de Mandioca',75.000,70.000,-5.000,'Produção',1),(6,'2024-05-08 23:54:04',1,'Farinha de Mandioca',70.000,65.000,-5.000,'Produção',1),(7,'2024-05-08 23:54:04',1,'Farinha de Mandioca',65.000,60.000,-5.000,'Produção',1),(8,'2024-05-10 20:03:34',2,'Farinha de trigo',0.000,300.000,300.000,'Compra',1),(9,'2024-05-10 20:16:26',1,'Farinha de Mandioca',60.000,500.000,440.000,'Registro Manual',1),(10,'2024-05-10 20:16:26',2,'Farinha de trigo',300.000,500.000,200.000,'Registro Manual',1),(11,'2024-05-10 20:16:26',3,'Manteiga sem sal',0.000,500.000,500.000,'Registro Manual',1),(12,'2024-05-10 20:16:26',4,'Açúcar refinado',0.000,500.000,500.000,'Registro Manual',1),(13,'2024-05-10 20:16:26',5,'Bandeja Isopor pequena',0.000,500.000,500.000,'Registro Manual',1),(14,'2024-05-10 20:16:43',1,'Farinha de Mandioca',500.000,499.500,-0.500,'Produção',1),(15,'2024-05-10 20:16:43',3,'Manteiga sem sal',500.000,498.000,-2.000,'Produção',1),(16,'2024-05-10 20:16:43',4,'Açúcar refinado',500.000,499.000,-1.000,'Produção',1),(17,'2024-05-10 20:16:43',5,'Bandeja Isopor pequena',500.000,490.000,-10.000,'Produção',1),(18,'2024-05-10 23:22:34',1,'Farinha de Mandioca',499.500,499.000,-0.500,'Produção',1),(19,'2024-05-10 23:22:34',3,'Manteiga sem sal',498.000,496.000,-2.000,'Produção',1),(20,'2024-05-10 23:22:34',4,'Açúcar refinado',499.000,498.000,-1.000,'Produção',1),(21,'2024-05-10 23:22:34',5,'Bandeja Isopor pequena',490.000,480.000,-10.000,'Produção',1),(22,'2024-05-11 00:29:27',1,'Farinha de Mandioca',499.000,498.500,-0.500,'Produção',1),(23,'2024-05-11 00:29:27',3,'Manteiga sem sal',496.000,494.000,-2.000,'Produção',1),(24,'2024-05-11 00:29:27',4,'Açúcar refinado',498.000,497.000,-1.000,'Produção',1),(25,'2024-05-11 00:29:27',5,'Bandeja Isopor pequena',480.000,470.000,-10.000,'Produção',1),(26,'2024-05-22 01:23:54',1,'Farinha de Mandioca',498.500,497.000,-1.500,'Produção',1),(27,'2024-05-22 01:23:54',3,'Manteiga sem sal',494.000,488.000,-6.000,'Produção',1),(28,'2024-05-22 01:23:54',4,'Açúcar refinado',497.000,494.000,-3.000,'Produção',1),(29,'2024-05-22 01:23:54',5,'Bandeja Isopor pequena',470.000,440.000,-30.000,'Produção',1),(30,'2024-05-22 18:15:33',1,'Farinha de Mandioca',497.000,496.500,-0.500,'Produção',1),(31,'2024-05-22 18:15:33',3,'Manteiga sem sal',488.000,486.000,-2.000,'Produção',1),(32,'2024-05-22 18:15:33',4,'Açúcar refinado',494.000,493.000,-1.000,'Produção',1),(33,'2024-05-22 18:15:33',5,'Bandeja Isopor pequena',440.000,430.000,-10.000,'Produção',1),(34,'2024-05-22 18:25:19',1,'Farinha de Mandioca',496.500,493.500,-3.000,'Produção',1),(35,'2024-05-22 18:25:19',3,'Manteiga sem sal',486.000,480.000,-6.000,'Produção',1),(36,'2024-05-23 17:25:56',1,'Farinha de Mandioca',493.500,492.500,-1.000,'Produção',1),(37,'2024-05-23 17:25:56',3,'Manteiga sem sal',480.000,478.000,-2.000,'Produção',1);
/*!40000 ALTER TABLE `historico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario` (
  `id_invt` int NOT NULL AUTO_INCREMENT,
  `data_invt` datetime DEFAULT NULL,
  `estado_invt` enum('Aberto','Fechado') DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_invt`),
  KEY `fk_inventario_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_inventario_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario`
--

LOCK TABLES `inventario` WRITE;
/*!40000 ALTER TABLE `inventario` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventariodados`
--

DROP TABLE IF EXISTS `inventariodados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventariodados` (
  `id_invtdados` int NOT NULL AUTO_INCREMENT,
  `id_invt` int NOT NULL,
  `data_invt` datetime NOT NULL,
  `id_mp` int NOT NULL,
  `nome_mp` varchar(75) NOT NULL,
  `unidade_mp` enum('KG','UN') DEFAULT NULL,
  `quantidade_estq` decimal(10,3) NOT NULL,
  `quantidade_invtdados` decimal(10,3) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_invtdados`),
  KEY `fk_inventariodados_id_invt_inventario` (`id_invt`),
  KEY `fk_inventariodados_id_mp_materiasprimas` (`id_mp`),
  KEY `fk_inventariodados_quantidade_estq_estoque` (`quantidade_estq`),
  KEY `fk_inventariodados_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_inventariodados_id_invt_inventario` FOREIGN KEY (`id_invt`) REFERENCES `inventario` (`id_invt`),
  CONSTRAINT `fk_inventariodados_id_mp_materiasprimas` FOREIGN KEY (`id_mp`) REFERENCES `materiasprimas` (`id_mp`),
  CONSTRAINT `fk_inventariodados_quantidade_estq_estoque` FOREIGN KEY (`quantidade_estq`) REFERENCES `estoque` (`quantidade_estq`),
  CONSTRAINT `fk_inventariodados_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventariodados`
--

LOCK TABLES `inventariodados` WRITE;
/*!40000 ALTER TABLE `inventariodados` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventariodados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materiasprimas`
--

DROP TABLE IF EXISTS `materiasprimas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materiasprimas` (
  `id_mp` int NOT NULL AUTO_INCREMENT,
  `nome_mp` varchar(75) DEFAULT NULL,
  `unidade_mp` enum('KG','UN') DEFAULT NULL,
  `pesounitario_mp` decimal(10,3) DEFAULT NULL,
  `pesototal_mp` decimal(10,3) DEFAULT NULL,
  `custo_mp` decimal(10,2) DEFAULT NULL,
  `custoemkg_mp` decimal(10,2) DEFAULT NULL,
  `departamento_mp` enum('Carnes','Farinhas','Hortifruti','Mercearia','Misturas','Ovos','Queijo','EMBALAGEM') DEFAULT NULL,
  `pedidomin_mp` decimal(10,3) DEFAULT NULL,
  `gastomedio_mp` decimal(10,3) DEFAULT NULL,
  `gms_mp` decimal(10,3) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_mp`),
  KEY `fk_materiasprimas_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_materiasprimas_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materiasprimas`
--

LOCK TABLES `materiasprimas` WRITE;
/*!40000 ALTER TABLE `materiasprimas` DISABLE KEYS */;
INSERT INTO `materiasprimas` VALUES (1,'Farinha de Mandioca','KG',0.500,50.000,1852.00,37.04,'Farinhas',100.000,15.000,90.000,1),(2,'Farinha de trigo','KG',25.000,25.000,85.90,3.44,'Farinhas',25.000,75.000,450.000,1),(3,'Manteiga sem sal','KG',5.000,5.000,38.00,7.60,'Mercearia',5.000,5.000,30.000,1),(4,'Açúcar refinado','KG',1.000,10.000,42.50,4.25,'Mercearia',10.000,2.000,12.000,1),(5,'Bandeja Isopor pequena','UN',0.100,1.000,150.00,150.00,'EMBALAGEM',500.000,70.000,420.000,1);
/*!40000 ALTER TABLE `materiasprimas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `planomestre`
--

DROP TABLE IF EXISTS `planomestre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `planomestre` (
  `id_pm` int NOT NULL AUTO_INCREMENT,
  `codigo_rct` int DEFAULT NULL,
  `nome_rct` varchar(75) DEFAULT NULL,
  `class_rct` varchar(45) DEFAULT NULL,
  `departamento_rct` varchar(45) DEFAULT NULL,
  `estoque_pm` int DEFAULT NULL,
  `pedidototal_pm` int DEFAULT NULL,
  `pedidokgtotal_pm` decimal(10,3) DEFAULT NULL,
  `rctnecessaria_pm` int DEFAULT NULL,
  `data_pm` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_pm`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `planomestre`
--

LOCK TABLES `planomestre` WRITE;
/*!40000 ALTER TABLE `planomestre` DISABLE KEYS */;
INSERT INTO `planomestre` VALUES (1,NULL,'Pao Com Batata','Fresco','Paes',0,0,0.000,0,'2024-05-23 02:35:41.844009'),(2,NULL,'Pao Com Batata','Fresco','Paes',0,0,0.000,0,'2024-05-23 14:42:57.165344'),(3,NULL,'Pao Com Batata','Fresco','Paes',0,0,0.000,0,'2024-05-23 17:54:28.891636');
/*!40000 ALTER TABLE `planomestre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `planomestrefiliais`
--

DROP TABLE IF EXISTS `planomestrefiliais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `planomestrefiliais` (
  `id_pmf` int NOT NULL AUTO_INCREMENT,
  `id_pm` int DEFAULT NULL,
  `filial_pdc` int DEFAULT NULL,
  `nomefilial_pdc` varchar(50) DEFAULT NULL,
  `quantidade_pdc` int DEFAULT NULL,
  PRIMARY KEY (`id_pmf`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `planomestrefiliais`
--

LOCK TABLES `planomestrefiliais` WRITE;
/*!40000 ALTER TABLE `planomestrefiliais` DISABLE KEYS */;
INSERT INTO `planomestrefiliais` VALUES (1,1,2,'loja dama 2',21),(2,2,1,'loja dama 1',7),(3,3,1,'loja dama 1',21);
/*!40000 ALTER TABLE `planomestrefiliais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produc`
--

DROP TABLE IF EXISTS `produc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produc` (
  `id_pdc` int NOT NULL AUTO_INCREMENT,
  `data_pdc` datetime NOT NULL,
  `estado_pdc` enum('Pendente','Fechado') NOT NULL,
  `nome_rct` varchar(75) NOT NULL,
  `user_id` int NOT NULL,
  `filial_pdc` varchar(45) NOT NULL,
  `nomefilial_pdc` varchar(50) DEFAULT NULL,
  `departamento_rct` varchar(45) DEFAULT NULL,
  `class_rct` varchar(45) DEFAULT NULL,
  `pedidomin_rct` int DEFAULT NULL,
  `fechadoem_pdc` datetime DEFAULT NULL,
  `quantidade_pdc` int DEFAULT NULL,
  PRIMARY KEY (`id_pdc`),
  KEY `fk_produc_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_produc_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produc`
--

LOCK TABLES `produc` WRITE;
/*!40000 ALTER TABLE `produc` DISABLE KEYS */;
INSERT INTO `produc` VALUES (8,'2024-05-10 23:50:53','Fechado','test',1,'1','loja dama 1','test','test',2,'2024-05-11 00:29:27',10),(9,'2024-05-11 01:29:53','Fechado','test',1,'1','loja dama 1','test','test',2,'2024-05-22 18:15:33',10),(10,'2024-05-22 01:20:57','Fechado','test',1,'2','loja dama 2','test','test',2,'2024-05-22 01:23:54',30),(11,'2024-05-22 01:52:27','Pendente','test',1,'2','loja dama 2','test','test',2,'2024-05-22 01:49:17',20),(12,'2024-05-22 18:24:27','Fechado','Pao Com Batata',1,'1','loja dama 1','Paes','Fresco',5,'2024-05-22 18:25:19',21),(13,'2024-05-22 18:50:32','Pendente','Pao Com Batata',1,'2','loja dama 2','Paes','Fresco',5,'2024-05-22 18:47:09',7),(14,'2024-05-22 18:51:53','Pendente','Pao Com Batata',1,'2','loja dama 2','Paes','Fresco',5,'2024-05-22 18:47:09',28),(15,'2024-05-23 02:35:42','Pendente','Pao Com Batata',1,'2','loja dama 2','Paes','Fresco',5,'2024-05-23 02:35:24',21),(16,'2024-05-23 14:42:57','Fechado','Pao Com Batata',1,'1','loja dama 1','Paes','Fresco',5,'2024-05-23 17:25:56',7),(17,'2024-05-23 17:54:29','Pendente','Pao Com Batata',1,'1','loja dama 1','Paes','Fresco',5,'2024-05-23 17:51:16',21);
/*!40000 ALTER TABLE `produc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producdados`
--

DROP TABLE IF EXISTS `producdados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producdados` (
  `id_pdcd` int NOT NULL AUTO_INCREMENT,
  `id_pdc` int NOT NULL,
  `id_rct` int NOT NULL,
  `id_mp` int NOT NULL,
  `nome_mp` varchar(75) DEFAULT NULL,
  `quantidade_pdcd` decimal(10,3) DEFAULT NULL,
  `unidade_pdcd` enum('KG','UN') DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id_pdcd`),
  KEY `fk_producdados_id_pdc_produc` (`id_pdc`),
  KEY `fk_producdados_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_producdados_id_pdc_produc` FOREIGN KEY (`id_pdc`) REFERENCES `produc` (`id_pdc`),
  CONSTRAINT `fk_producdados_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producdados`
--

LOCK TABLES `producdados` WRITE;
/*!40000 ALTER TABLE `producdados` DISABLE KEYS */;
INSERT INTO `producdados` VALUES (17,8,16,1,'Farinha de Mandioca',0.500,'KG',1),(18,8,16,3,'Manteiga sem sal',2.000,'KG',1),(19,8,16,4,'Açúcar refinado',1.000,'KG',1),(20,8,16,5,'Bandeja Isopor pequena',10.000,'UN',1),(21,9,16,1,'Farinha de Mandioca',0.500,'KG',1),(22,9,16,3,'Manteiga sem sal',2.000,'KG',1),(23,9,16,4,'Açúcar refinado',1.000,'KG',1),(24,9,16,5,'Bandeja Isopor pequena',10.000,'UN',1),(25,10,16,1,'Farinha de Mandioca',1.500,'KG',1),(26,10,16,3,'Manteiga sem sal',6.000,'KG',1),(27,10,16,4,'Açúcar refinado',3.000,'KG',1),(28,10,16,5,'Bandeja Isopor pequena',30.000,'UN',1),(29,11,16,1,'Farinha de Mandioca',1.000,'KG',1),(30,11,16,3,'Manteiga sem sal',4.000,'KG',1),(31,11,16,4,'Açúcar refinado',2.000,'KG',1),(32,11,16,5,'Bandeja Isopor pequena',20.000,'UN',1),(33,12,17,1,'Farinha de Mandioca',3.000,'KG',1),(34,12,17,3,'Manteiga sem sal',6.000,'KG',1),(35,13,17,1,'Farinha de Mandioca',1.000,'KG',1),(36,13,17,3,'Manteiga sem sal',2.000,'KG',1),(37,14,17,1,'Farinha de Mandioca',4.000,'KG',1),(38,14,17,3,'Manteiga sem sal',8.000,'KG',1),(39,15,17,1,'Farinha de Mandioca',3.000,'KG',1),(40,15,17,3,'Manteiga sem sal',6.000,'KG',1),(41,16,17,1,'Farinha de Mandioca',1.000,'KG',1),(42,16,17,3,'Manteiga sem sal',2.000,'KG',1),(43,17,17,1,'Farinha de Mandioca',3.000,'KG',1),(44,17,17,3,'Manteiga sem sal',6.000,'KG',1);
/*!40000 ALTER TABLE `producdados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receitamateriasprimas`
--

DROP TABLE IF EXISTS `receitamateriasprimas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receitamateriasprimas` (
  `id_rctmp` int NOT NULL AUTO_INCREMENT,
  `nome_mp` varchar(75) DEFAULT NULL,
  `quantidade` decimal(10,3) DEFAULT NULL,
  `unidade` enum('KG','UN') DEFAULT NULL,
  `tipo_rctmp` enum('Ingrediente','Embalagem') DEFAULT NULL,
  `user_id` int NOT NULL,
  `id_rct` int DEFAULT NULL,
  `id_mp` int DEFAULT NULL,
  PRIMARY KEY (`id_rctmp`),
  UNIQUE KEY `id_rctmp_UNIQUE` (`id_rctmp`),
  KEY `fk_receitamateriasprimas_user_id_usuarios` (`user_id`),
  KEY `fk_receitamateriasprimas_id_rct_receitas_idx` (`id_rct`),
  KEY `fk_receitamateriasprimas_id_mp_materiasprimas_idx` (`id_mp`),
  CONSTRAINT `fk_receitamateriasprimas_id_mp_materiasprimas` FOREIGN KEY (`id_mp`) REFERENCES `materiasprimas` (`id_mp`),
  CONSTRAINT `fk_receitamateriasprimas_id_rct_receitas` FOREIGN KEY (`id_rct`) REFERENCES `receitas` (`id_rct`),
  CONSTRAINT `fk_receitamateriasprimas_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receitamateriasprimas`
--

LOCK TABLES `receitamateriasprimas` WRITE;
/*!40000 ALTER TABLE `receitamateriasprimas` DISABLE KEYS */;
INSERT INTO `receitamateriasprimas` VALUES (5,'Farinha de Mandioca',0.200,'KG','Ingrediente',1,NULL,1),(6,'Farinha de Mandioca',0.300,'KG','Ingrediente',1,NULL,1),(7,'Farinha de Mandioca',0.500,'KG','Ingrediente',1,NULL,1),(17,'Manteiga sem sal',2.000,'KG','Embalagem',1,NULL,3),(18,'Farinha de Mandioca',5.000,'KG','Ingrediente',1,NULL,1),(19,'Farinha de Mandioca',2.000,'KG','Ingrediente',1,NULL,1),(20,'Farinha de Mandioca',0.500,'KG','Ingrediente',1,NULL,1),(21,'Açúcar refinado',1.500,'KG','Ingrediente',1,NULL,4),(22,'Manteiga sem sal',0.150,'KG','Ingrediente',1,NULL,3),(23,'Bandeja Isopor pequena',10.000,'UN','Embalagem',1,NULL,5),(24,'Farinha de Mandioca',0.500,'KG','Ingrediente',1,NULL,1),(25,'Manteiga sem sal',2.000,'KG','Ingrediente',1,NULL,3),(26,'Açúcar refinado',1.000,'KG','Ingrediente',1,NULL,4),(27,'Bandeja Isopor pequena',10.000,'UN','Embalagem',1,NULL,5),(28,'Farinha de Mandioca',1.000,'KG','Ingrediente',1,17,1),(29,'Manteiga sem sal',2.000,'KG','Ingrediente',1,17,3);
/*!40000 ALTER TABLE `receitamateriasprimas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receitas`
--

DROP TABLE IF EXISTS `receitas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receitas` (
  `id_rct` int NOT NULL AUTO_INCREMENT,
  `nome_rct` varchar(75) DEFAULT NULL,
  `cod_rct` varchar(10) DEFAULT NULL,
  `descricao_rct` text,
  `preparo_rct` text,
  `rendimento_rct` int DEFAULT NULL,
  `class_rct` varchar(45) DEFAULT NULL,
  `departamento_rct` varchar(45) DEFAULT NULL,
  `validade_rct` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `rendimentokg_rct` decimal(10,3) DEFAULT NULL,
  `unidadeporkg_rct` int DEFAULT NULL,
  `pedidomin_rct` int DEFAULT NULL,
  `contador_rct` varchar(45) DEFAULT NULL,
  `estoque_rct` int DEFAULT NULL,
  PRIMARY KEY (`id_rct`),
  KEY `fk_receitas_user_id_usuarios` (`user_id`),
  CONSTRAINT `fk_receitas_user_id_usuarios` FOREIGN KEY (`user_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receitas`
--

LOCK TABLES `receitas` WRITE;
/*!40000 ALTER TABLE `receitas` DISABLE KEYS */;
INSERT INTO `receitas` VALUES (17,'Pao Com Batata',NULL,'Pao Com Batata','Se fasz',7,'Fresco','Paes',21,1,3.000,3,5,'4',14);
/*!40000 ALTER TABLE `receitas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rotas`
--

DROP TABLE IF EXISTS `rotas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rotas` (
  `id_rota` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `veiculo` varchar(20) NOT NULL,
  `placa` varchar(10) NOT NULL,
  `horario` varchar(15) NOT NULL,
  `whatsapp` varchar(50) NOT NULL,
  PRIMARY KEY (`id_rota`),
  UNIQUE KEY `uq_rotas_nome` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rotas`
--

LOCK TABLES `rotas` WRITE;
/*!40000 ALTER TABLE `rotas` DISABLE KEYS */;
INSERT INTO `rotas` VALUES (1,'jose antonio','fiorino','JHZ-7073','06hrs','31986598988');
/*!40000 ALTER TABLE `rotas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` enum('admin','master') NOT NULL,
  `nomecompleto` varchar(100) NOT NULL,
  `funcao` varchar(50) NOT NULL,
  `whatsapp` varchar(50) NOT NULL,
  `cpf` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_usuarios_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'dama','432','master','Dama Ribera','Gerente','982186320','70624058689','andresexplorer83@gmail.com');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-23 18:08:40
