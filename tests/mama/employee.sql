SELECT e.id as id, e.name as name, c.name as company
FROM employees as e
LEFT JOIN company as c
on e.company_id = c.id
WHERE e.id = %(id)s;