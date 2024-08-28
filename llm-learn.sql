/*
 Navicat Premium Dump SQL

 Source Server         : 172.17.18.242
 Source Server Type    : MySQL
 Source Server Version : 80036 (8.0.36)
 Source Host           : localhost:3306
 Source Schema         : llm-assistant

 Target Server Type    : MySQL
 Target Server Version : 80036 (8.0.36)
 File Encoding         : 65001

 Date: 28/08/2024 20:26:37
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for learn
-- ----------------------------
DROP TABLE IF EXISTS `learn`;
CREATE TABLE `learn`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `hid` int NOT NULL COMMENT 'HID',
  `oid` int NOT NULL COMMENT 'OID',
  `bid` int NOT NULL COMMENT 'BID',
  `sid` int NOT NULL COMMENT 'SID',
  `user` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '用户',
  `pid` int NULL DEFAULT 0 COMMENT '父id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '学习表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for subject
-- ----------------------------
DROP TABLE IF EXISTS `subject`;
CREATE TABLE `subject`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `stage_id` int NOT NULL COMMENT '标题ID',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标题',
  `user` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '用户',
  `pid` int NOT NULL DEFAULT 0 COMMENT '父id',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '标题表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
