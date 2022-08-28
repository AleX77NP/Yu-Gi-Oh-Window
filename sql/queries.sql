-- 1. Retrieve top 3 secret rare cards from every set (order is by card number in set)
SELECT * FROM (
	SELECT
		Card_name, Rarity, "Card type", "Card-set", Card_number,
		ROW_NUMBER() OVER(PARTITION BY "Card-set" ORDER BY Card_number) as "Set_rank"
		FROM cards c
		WHERE Rarity = "Secret Rare" ) x
WHERE x.Set_rank <= 3;

-- 2. Retrieve top 5 Link monsters with highest ATK in every set they were released in
WITH link_monsters AS (
	SELECT
		Card_name, "Card-set", Types, ATK, LINK,
		ROW_NUMBER() OVER(PARTITION BY "Card-set" ORDER BY CAST (ATK as int) desc) as "Set_rank"
		FROM cards c
		WHERE "Types" LIKE "%Link%"
)

SELECT * from link_monsters WHERE "Set_rank" <= 5;
-- Using CTE



