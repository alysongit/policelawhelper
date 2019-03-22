BEGIN;
--
-- Create model Bookmark
--
CREATE TABLE `xadmin_bookmark` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `title` varchar(128) NOT NULL, `url_name` varchar(64) NOT NULL, `query` varchar(1000) NOT NULL, `is_share` bool NOT NULL, `content_type_id` integer NOT NULL, `user_id` integer NULL);
--
-- Create model Log
--
CREATE TABLE `xadmin_log` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `action_time` datetime(6) NOT NULL, `ip_addr` char(39) NULL, `object_id` longtext NULL, `object_repr` varchar(200) NOT NULL, `action_flag` varchar(32) NOT NULL, `message` longtext NOT NULL, `content_type_id` integer NULL, `user_id` integer NOT NULL);
--
-- Create model UserSettings
--
CREATE TABLE `xadmin_usersettings` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `key` varchar(256) NOT NULL, `value` longtext NOT NULL, `user_id` integer NOT NULL);
--
-- Create model UserWidget
--
CREATE TABLE `xadmin_userwidget` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `page_id` varchar(256) NOT NULL, `widget_type` varchar(50) NOT NULL, `value` longtext NOT NULL, `user_id` integer NOT NULL);

ALTER TABLE `xadmin_bookmark` ADD CONSTRAINT `xadmin_bookmark_content_type_id_60941679_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
ALTER TABLE `xadmin_bookmark` ADD CONSTRAINT `xadmin_bookmark_user_id_42d307fc_fk_users_account_id` FOREIGN KEY (`user_id`) REFERENCES `users_account` (`id`);
ALTER TABLE `xadmin_log` ADD CONSTRAINT `xadmin_log_content_type_id_2a6cb852_fk_django_content_type_id` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
ALTER TABLE `xadmin_log` ADD CONSTRAINT `xadmin_log_user_id_bb16a176_fk_users_account_id` FOREIGN KEY (`user_id`) REFERENCES `users_account` (`id`);
ALTER TABLE `xadmin_usersettings` ADD CONSTRAINT `xadmin_usersettings_user_id_edeabe4a_fk_users_account_id` FOREIGN KEY (`user_id`) REFERENCES `users_account` (`id`);
ALTER TABLE `xadmin_userwidget` ADD CONSTRAINT `xadmin_userwidget_user_id_c159233a_fk_users_account_id` FOREIGN KEY (`user_id`) REFERENCES `users_account` (`id`);
COMMIT;