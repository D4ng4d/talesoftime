-- Like Statements --

-- LIKE example 1 - Where CharacterName contains Ghaz
SELECT CharacterID, CharacterName, Level
FROM Character
WHERE CharacterName LIKE '%Ghaz%'
ORDER BY CharacterName;

-- LIKE example 2 - Where QuestName starts with Death
SELECT QuestID, QuestName
FROM Quest
WHERE QuestName LIKE 'Death%'
ORDER BY QuestName;

-- LIKE example 3 - Where Species ends with f
SELECT SpeciesID, SpeciesName
FROM Species
WHERE SpeciesName LIKE '%f'
ORDER BY SpeciesName;


-- JOIN tables --

-- Join Table example 1 -- Character, Class, Species and Alignment
SELECT
    c.CharacterName,
    c.Level,
    cc.ClassName,
    s.SpeciesName,
    a.AlignmentName
FROM Character c
JOIN CharacterClass cc ON c.ClassID = cc.ClassID
JOIN Species s         ON c.SpeciesID = s.SpeciesID
JOIN Alignment a       ON c.AlignmentID = a.AlignmentID
ORDER BY CharacterName;

-- Join table example 2 -- Inventory, Item, ItemType, Rarity
SELECT
    c.CharacterName,
    i.ItemName,
    it.TypeName,
    r.RarityName,
    inv.Quantity
FROM Inventory inv
JOIN Character c ON inv.CharacterID = c.CharacterID
JOIN Item i      ON inv.ItemID      = i.ItemID
JOIN ItemType it ON i.ItemTypeID    = it.ItemTypeID
JOIN Rarity r    ON i.RarityID      = r.RarityID
ORDER BY c.CharacterName, i.ItemName;



-- STATISTICS From Functions --

-- Total Counts --
SELECT
    (SELECT COUNT(*) FROM Region) as total_regions,
    (SELECT COUNT(*) FROM Item)   as total_items,
    (SELECT COUNT(*) FROM Character) as total_characters;

-- Average, min and max --

SELECT
    AVG(Level) AS avg_level,
    MIN(Level) AS min_level,
    MAX(Level) AS max_level
FROM Character;

-- Number of Characters per class -- 
SELECT
    c.CharacterName,
    COUNT(*) as character_count
FROM Character c 
JOIN CHaracterClass cc ON c.ClassID = cc.ClassID
GROUP BY cc.ClassID
ORDER BY character_count DESC;

-- UPDATE Examples --

-- Increase Character Level --
SELECT CharacterName, Level
FROM Character
WHERE CharacterName = 'Ghazkull';

UPDATE Character
SEt Level = Level + 1
WHERE CharacterName = 'Ghazkull';

SELECT CharacterName, Level
FROM Character
WHERE CharacterName = 'Ghazkull';

-- Change Characters Alignment --
SELECT 
    c.CharacterID,
    c.CharacterName,
    c.AlignmentID,
    a.AlignmentName
FROM Character c 
JOIN Alignment a ON c. AlignmentID = a.AlignmentID
WHERE c.CharacterName = 'Ghazkull';

UPDATE Character
SET AlignmentID = (SELECT AlignmentID FROM Alignment WHERE AlignmentName = 'Divergent')
WHERE CharacterName = 'Ghazkull';

SELECT 
    c.CharacterID,
    c.CharacterName,
    c.AlignmentID,
    a.AlignmentName
FROM Character c 
JOIN Alignment a ON c. AlignmentID = a.AlignmentID
WHERE c.CharacterName = 'Ghazkull';

-- DELETE Examples --

-- Delete Quest --
SELECT cq.QuestID, q.QuestName
FROM Character c
JOIN CharacterQuest cq ON cq.CharacterID = c.CharacterID
JOIN Quest q           ON q.QuestID = cq.QuestID
WHERE c.CharacterName = 'Darryn'
ORDER BY q.QuestName;

DELETE FROM CharacterQuest
WHERE CharacterID = (SELECT CharacterID FROM CHaracter WHERE CharacterName = 'Darryn');

SELECT cq.QuestID, q.QuestName
FROM Character c
JOIN CharacterQuest cq ON cq.CharacterID = c.CharacterID
JOIN Quest q           ON q.QuestID = cq.QuestID
WHERE c.CharacterName = 'Darryn'
ORDER BY q.QuestName;


-- Delete Inventory --
SELECT 
    c.CharacterName,
    i.ItemName,
    inv.Quantity
FROM Character c
JOIN Inventory inv ON inv.CharacterID = c.CharacterID
JOIN Item i        ON i.ItemID        = inv.ItemID
WHERE c.CharacterName = 'Darryn'
ORDER BY i.ItemID;

DELETE FROM Inventory
WHERE CharacterID = (SELECT CharacterID FROM Character WHERE CharacterName = 'Darryn');

SELECT 
    c.CharacterName,
    i.ItemName,
    inv.Quantity
FROM Character c
JOIN Inventory inv ON inv.CharacterID = c.CharacterID
JOIN Item i        ON i.ItemID        = inv.ItemID
WHERE c.CharacterName = 'Darryn'
ORDER BY i.ItemID;