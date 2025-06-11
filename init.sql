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
    `note` VARCHAR(255) DEFAULT NULL COMMENT '备注'
) COMMENT '学生表';

-- 插入数据
INSERT INTO `student` (`name`, `age`, note) VALUES
('张三', 20, '这是张三的备注'),
('李四', 22, '这是李四的备注'),
('王五', 21, '这是王五的备注');
