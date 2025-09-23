---------------- README / Usage ----------------

Save this file as app.py or campuscircle_backend.py

Install dependencies (recommended inside a virtualenv):

pip install flask flask-cors werkzeug

Run:

python app.py



Endpoints summary (JSON input unless otherwise noted):

POST /signup -> {name, email, password}  (returns session_token)

POST /login -> {email, password} (returns session_token)

POST /logout -> Authorization: Bearer <token>

GET /alumni -> public, returns list for "Show data in network" button

POST /alumni -> protected, create alumnus (provide Authorization header)

GET /alumni/<id> -> get record

PUT /alumni/<id> -> protected, update fields

DELETE /alumni/<id> -> protected

GET /alumni/export -> protected, downloads CSV

POST /init_db -> create tables (optional)



Frontend notes:

- To show "network" data, call GET /alumni and render the array in the UI.

- For signup/login, call POST /signup and POST /login respectively and store session_token in client storage.

- For protected actions (create/update/delete/export), include header: Authorization: Bearer <session_token>



Security notes:

- Passwords are stored as hashes. Session tokens are UUIDs saved in DB.

- This is a simple auth approach suitable for MVP. For production, use HTTPS, expiry for tokens, refresh tokens or JWTs, and additional protections (rate limiting, input validation, CSRF protections for cookie flows).



If you want, I can also provide:

- a requirements.txt

- a sample Postman collection

- a minimal frontend fetch example (JS) to hook into your existing site

- deploy instructions for Render/Heroku/Vercel (as API)
