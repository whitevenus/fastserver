CREATE DATABASE IF NOT EXISTS test;
USE test;

-- 数据库初始化SQL
CREATE TABLE IF NOT EXISTS `student` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL COMMENT '姓名',
    `age` INT NOT NULL COMMENT '年龄',
    `create_id` INT NOT NULL DEFAULT 0 COMMENT '创建人ID',
    `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_id` INT NOT NULL DEFAULT 0 COMMENT '更新人ID',
    `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `note` VARCHAR(255) DEFAULT NULL DEFAULT "" COMMENT '备注'
) COMMENT '学生表';

-- 插入数据
INSERT INTO `student` (`name`, `age`, note) VALUES
('alex', 20, 'this is a test note'),
('bob', 21, 'this is a test note'),
('cathy', 22, 'this is a test note'),
('david', 23, 'this is a test note'),
('eve', 24, 'this is a test note');
