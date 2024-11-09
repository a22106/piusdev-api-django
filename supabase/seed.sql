insert into auth_user
 (id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
values
    (1, 'pbkdf2_sha256$150000$z1Z6Z6Z6Z6Z6$', 'f', 'test', 'Pius', 'Test', 'test@piusdev.com', 'f', 't', '2024-01-01 00:00:00');