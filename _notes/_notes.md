# Backend Notes

- handle password
```py
from werkzeug.security import generate_password_hash, check_password_hash

hashed_passwd = generate_password_hash("some password")
check_password_hash(hashed_pashwd, "some password")
```

- generate a random uuid: `uuid = uuid4()` (`from uuid import uuid4`)

- handle a JsonWebToken (JWT):
```py
import jwt

token = jwt.encode({
    'foo': 'bar',
    'baz': -1,

    'exp': '01-01-1960' # for expiration date
}, 'a_secret_key', algorithm='HS256')

jwt.decode(token, SECRET, algorithms=['HS256'])
```
