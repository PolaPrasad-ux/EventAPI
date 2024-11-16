SELECT 
    e.id AS event_id,
    e.name AS event_name,
    e.date AS event_date,
    e.total_tickets,
    e.tickets_sold
FROM 
    events e
ORDER BY 
    e.tickets_sold DESC
LIMIT 3;
