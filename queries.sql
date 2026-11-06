SELECT r.id, e.inventory_number, e.name, r.priority, r.status, r.description
FROM maintenance_request r
JOIN equipment e ON e.id = r.equipment_id
ORDER BY CASE r.priority
             WHEN 'critical' THEN 1 WHEN 'high' THEN 2
             WHEN 'medium'   THEN 3 ELSE 4 END,
         r.created_at;

SELECT status, COUNT(*) AS cnt
FROM maintenance_request
GROUP BY status
ORDER BY cnt DESC;

SELECT e.inventory_number, e.name
FROM equipment e
WHERE NOT EXISTS (
    SELECT 1 FROM maintenance_request r
    WHERE r.equipment_id = e.id AND r.status IN ('open', 'in_progress')
);

SELECT e.inventory_number, e.name, COUNT(r.id) AS requests_total
FROM equipment e
JOIN maintenance_request r ON r.equipment_id = e.id
GROUP BY e.id
ORDER BY requests_total DESC, e.inventory_number
LIMIT 3;
