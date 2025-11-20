CREATE TABLE web_links (
    link_id INT PRIMARY KEY,
    link_text VARCHAR(500),
    link_url VARCHAR(500),
    category VARCHAR(500)
);

INSERT INTO web_links (link_id, link_text, link_url, category) VALUES
(1, '네이버', 'https://naver.com', 'portal'),
(2, '구글', 'https://google.com', 'portal'),
(3, '깃허브', 'https://github.com', 'dev');

SELECT *
FROM web_links;

SELECT link_id, link_text, link_url, category
FROM web_links
WHERE category = 'portal';

UPDATE web_links
SET category = 'code'
WHERE link_text = '깃허브';

DELETE FROM web_links
WHERE link_text = '네이버';