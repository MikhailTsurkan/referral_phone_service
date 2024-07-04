# Для запуска:
1. Заполнить файл .env.sample, изменить его название на .env
2. ввести команду "docker compose up"

# Эндпоинты:

---

request: 
```
POST /users/auth/get-code/
```
```json
{
  "phone": "+79000000000"
}
```

response:
```json
{
  "phone": "+79000000000"
}
```

**Описание:**
Принимает в теле запроса номер телефона и отправляет по нему код аутентификации

---

request: 
```
POST /users/auth/send-code/
```
```json
{
  "phone": "+79000000000",
  "password": "0000"
}
```

response:
```json
{
  "access": "some_strange_symbols_but_this_is_a_token",
  "refresh": "this_is_token_too_but_for_update_access_token"
}
```

**Описание:**
Принимает в теле запроса номер телефона и код аутентификации.
Возвращает два токена: один для доступа, второй для обновления токена доступа.

---

request: 
```
POST /users/auth/refresh/
```
```json
{
  "refresh": "this_is_refresh_token_from_previous_request"
}
```

response:
```json
{
  "access": "this_a_new_access_token"
}
```

**Описание:**
Принимает в теле запроса refresh токен.
Возвращает новый токен доступа

---

request: 
```
GET /users/retrieve-current/
```

response:
```json
{
  "phone": "+79000000000", 
  "invite_code": "0aA0Bb",
  "invited_by_code": null,
  "referrals": [
    "+79000000001",
    "+79000000002"
  ]
}
```

**Описание:**
Возвращает данные текущего пользователя, в том числе его рефералов

---

request: 
```
POST /users/set-referer/
```
```json
{
    "invite_code": "0aA0Bb"
}
```
response:
```json
{
  "message": "you have become referral of user with invite code 0aA0Bb0"
}
```
or
```json
{
  "message": "you have already been referral of user with invite code 0aA0Bb0"
}
```
**Описание:**
Принимает инвайт код другого пользователя, возвращает сообщение о становлении рефералом другого пользователя или сообщение
о текущем реферере

---