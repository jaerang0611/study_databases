CREATE TABLE news_articles (
    article_id INT PRIMARY KEY,
    title VARCHAR(500),
    url VARCHAR(500),
    author VARCHAR(500),
    published_at DATE
);

INSERT INTO news_articles (article_id, title, url, author, published_at) VALUES
(1, 'AI 시대 도래', 'https://news.com/ai', '홍길동', '2025-01-01'),
(2, '경제 성장률 상승', 'https://news.com/economy', '이영희', '2025-01-05');

SELECT *
FROM news_articles;

SELECT article_id, title, url, author, published_at
FROM news_articles
WHERE author = '홍길동';

UPDATE news_articles
SET title = '새로운 AI 뉴스 제목'
WHERE article_id = 1;

DELETE FROM news_articles
WHERE article_id = 2;