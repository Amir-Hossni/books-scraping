-- 1. Average price for each rating

SELECT
    rating,
    ROUND(AVG(price), 2) AS average_price
FROM books
GROUP BY rating;


-- 2. 5 most expensive books rated 4 or 5

SELECT
    title,
    price,
    rating
FROM books
WHERE rating IN (4, 5)
ORDER BY price DESC
LIMIT 5;


-- 3. Count out-of-stock books per rating

SELECT
    rating,
    SUM(CASE WHEN in_stock = 0 THEN 1 ELSE 0 END) AS out_of_stock_count
FROM books
GROUP BY rating
ORDER BY rating;