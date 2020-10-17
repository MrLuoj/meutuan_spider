# meutuan_spider

数据库操作
SET FOREIGN_KEY_CHECKS=0;
 
-- ----------------------------
-- Table structure for t_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `mt_test5`;
CREATE TABLE `mt_test5` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `meituanid` varchar(50) DEFAULT NULL COMMENT '美团ID',
  `companyname` varchar(80) DEFAULT NULL COMMENT '商家名称',
  `companyaddress` varchar(100) DEFAULT NULL COMMENT '商家地址',
  `businesstime` varchar(100) DEFAULT NULL COMMENT '运营时间',
  `destinephone` varchar(50) DEFAULT NULL COMMENT '联系方式',
  `score` varchar(50) DEFAULT NULL COMMENT '评分',
  `averagecost` varchar(50) DEFAULT NULL COMMENT '平均消费',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='用户信息表';
