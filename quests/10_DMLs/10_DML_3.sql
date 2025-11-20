CREATE TABLE scraping_html_results (
    result_id INT PRIMARY KEY,
    page_title VARCHAR(500),
    page_url VARCHAR(500),
    html_length INT,
    status_code INT
);

INSERT INTO scraping_html_results (result_id, page_title, page_url, html_length, status_code) VALUES
(1, '홈페이지', 'https://site.com', 15700, 200),
(2, '블로그', 'https://blog.com', 9800, 200),
(3, '404 페이지', 'https://site.com/notfound', 0, 404);

SELECT *
FROM scraping_html_results;

SELECT result_id, page_title, page_url, html_length, status_code
FROM scraping_html_results
WHERE status_code = 200;

UPDATE scraping_html_results
SET html_length = 12000
WHERE page_title = '블로그';

DELETE FROM scraping_html_results
WHERE status_code = 404;