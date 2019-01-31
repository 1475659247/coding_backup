/*
Navicat MySQL Data Transfer

Source Server         : 比价
Source Server Version : 50173
Source Host           : 101.201.121.245:3306
Source Database       : parity

Target Server Type    : MYSQL
Target Server Version : 50173
File Encoding         : 65001

Date: 2017-03-13 09:35:57
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ez_parity_brand
-- ----------------------------
DROP TABLE IF EXISTS `ez_parity_brand`;
CREATE TABLE `ez_parity_brand` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `brand_id` int(10) unsigned  NOT NULL COMMENT '品牌id',
  `brand_zh_name` varchar(255) DEFAULT NULL COMMENT '品牌名称',
  `brand_en_name` varchar(255) DEFAULT NULL COMMENT '品牌名称',
  `brand_logo` varchar(255) DEFAULT NULL COMMENT '品牌logo',
  `brand_logo_url` varchar(255) DEFAULT NULL COMMENT '品牌logo url',
  `status` int(2) unsigned zerofill DEFAULT NULL COMMENT '状态（0：正常，1：异常）',
  PRIMARY KEY (`id`),
  UNIQUE KEY `brand_id` (`brand_id`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ez_parity_brand
-- ----------------------------

-- ----------------------------
-- Table structure for ez_parity_class
-- ----------------------------
DROP TABLE IF EXISTS `ez_parity_class`;
CREATE TABLE `ez_parity_class` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `class_id` int(10) unsigned DEFAULT NULL,
  `class_name` varchar(255) DEFAULT NULL COMMENT '分类名称',
  `class_image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ez_parity_class
-- ----------------------------

-- ----------------------------
-- Table structure for ez_parity_price
-- ----------------------------
DROP TABLE IF EXISTS `ez_parity_price`;
CREATE TABLE `ez_parity_price` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` varchar(32) NOT NULL COMMENT '产品ID映射product表产品id',
  `price` decimal(10,3) NOT NULL COMMENT '产品价格',
  `update_time` int(10) unsigned NOT NULL COMMENT '更新价格时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of ez_parity_price
-- ----------------------------

-- ----------------------------
-- Table structure for ez_parity_product
-- ----------------------------
DROP TABLE IF EXISTS `ez_parity_product`;
CREATE TABLE `ez_parity_product` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `product_id` varchar(32) NOT NULL COMMENT '产品ID值（唯一）',
  `model` varchar(255) NOT NULL COMMENT '型号',
  `class_id` int(10) unsigned DEFAULT NULL COMMENT '分类ID , (映射class表ID)',
  `site_id` int(10) unsigned NOT NULL COMMENT '商家id',
  `brand_id` int(10) unsigned NOT NULL COMMENT '品牌id',
  `price_id` int(10) unsigned NOT NULL COMMENT '产品当前价格对应price表价格id',
  `goods_time` int(10) unsigned zerofill DEFAULT NULL COMMENT '货期（天/  0：现货）',
  `sales` int(10) unsigned zerofill NOT NULL COMMENT '销量',
  `name` varchar(255) NOT NULL COMMENT '产品名称',
  `image_url` varchar(255) DEFAULT NULL COMMENT '图片',
  `image` varchar(255) DEFAULT NULL COMMENT '图片',
  `url` varchar(255) NOT NULL COMMENT '产品链接',
  `status` int(2) unsigned zerofill DEFAULT NULL COMMENT '产品状态（0正常，1链接失效）默认0',
  `type` int(2) unsigned zerofill DEFAULT NULL COMMENT '类型（0：三方，1：自营）默认0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ez_parity_product
-- ----------------------------

-- ----------------------------
-- Table structure for ez_parity_site
-- ----------------------------
DROP TABLE IF EXISTS `ez_parity_site`;
CREATE TABLE `ez_parity_site` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `site_id` int(10) unsigned NOT NULL COMMENT '商家ID',
  `site_name` varchar(255) NOT NULL COMMENT '商家名称',
  `site_type` int(10) unsigned zerofill DEFAULT NULL COMMENT '商家类型',
  `site_telephone` varchar(125) DEFAULT NULL COMMENT '商家联系电话',
  `site_logo` varchar(255) NOT NULL COMMENT '商家logo',
  `site_certification` varchar(255) DEFAULT NULL COMMENT '商家认证',
  `site_web` varchar(255) NOT NULL COMMENT '商家官网',
  `status` int(2) unsigned zerofill DEFAULT NULL COMMENT '状态（0：正常，1：异常）',
  PRIMARY KEY (`id`),
  UNIQUE KEY `site_id` (`site_id`) USING BTREE,
  UNIQUE KEY `site_name` (`site_name`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ez_parity_site
-- ----------------------------
