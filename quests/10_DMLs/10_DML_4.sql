CREATE TABLE keyword_search_logs (
    log_id INT PRIMARY KEY,
    keyword VARCHAR(500),
    result_count INT,
    search_time VARCHAR(500)
);

INSERT INTO keyword_search_logs (log_id, keyword, result_count, search_time) VALUES
(1, 'python', 120, '2025-11-19 10:00:00'),
(2, 'chatgpt', 300, '2025-11-19 10:05:00'),
(3, 'docker', 90, '2025-11-19 10:10:00');

SELECT *
FROM keyword_search_logs;

SELECT log_id, keyword, result_count, search_time
FROM keyword_search_logs
WHERE result_count >= 100;

UPDATE keyword_search_logs
SET result_count = 150
WHERE keyword = 'docker';

DELETE FROM keyword_search_logs
WHERE keyword = 'python';