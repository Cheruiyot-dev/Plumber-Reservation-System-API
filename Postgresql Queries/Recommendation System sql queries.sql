SELECT u.username, u.public_id, u.id FROM users u
JOIN plumbers p ON u.id=p.id
WHERE u.public_id = '306f3645-5d5d-4aa5-b922-11cbcf3a8c4e';

