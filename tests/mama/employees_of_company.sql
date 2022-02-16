SELECT e.id as id, e.name as name, c.name as company
FROM company as c
LEFT JOIN employees as e
on c.id = e.company_id
WHERE c.id=%(id)s;