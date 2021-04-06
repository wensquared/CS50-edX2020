SELECT people.name from people 
JOIN stars ON stars.person_id = people.id
JOIN movies ON movies.id = stars.movie_id
WHERE movies.year = 2004
GROUP BY name, person_id
ORDER BY people.birth