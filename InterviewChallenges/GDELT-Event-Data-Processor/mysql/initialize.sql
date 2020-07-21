-- Initializes the "data" table, which will keep track of the data that is sent to
-- the recipient, as well as the response that was sent back.
CREATE TABLE IF NOT EXISTS `data` (
    `id` int unsigned auto_increment primary key,
    `global_event_id` varchar(50) not null,
    `file_url` varchar(255) not null,
    `data_sent` text not null,
    `data_received` text not null,
    `timestamp` timestamp
);

-- Initializes the "processed_files" table, which will keep track of the MD5 hashes
-- of the files that have already been uploaded to the recipient.
CREATE TABLE IF NOT EXISTS `processed_files` (
    `id` int unsigned auto_increment primary key,
    `md5_hash` char(32) not null,
    `file_url` varchar(255) not null,
    `successful` bit not null default 0
);
