DROP TABLE IF EXISTS `temphumi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `temphumi` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `temp` float DEFAULT NULL,
  `humi` float DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp(),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=116694 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
