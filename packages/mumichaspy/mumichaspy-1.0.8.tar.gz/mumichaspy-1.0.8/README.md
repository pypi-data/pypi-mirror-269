# MUMiChasPy

![MuMiChasPy logo](logo.png)

**Mondragon Unibertsitatea**'s *Microservice Chassis* pattern implementation in *Python* (MuMiChasPy).

## Developers

- [Alain PEREZ RIAÑO](https://github.com/draperez)

## Testing

- Create virtual environment:

```bash
python -m venv env
source env/bin/activate
```

- Install dependencies:

```bash
python -m pip install .[test]
```

- Execute tests:

```bash
pytest
```

## Style guide with flake8

```bash
pip install flake8 flake8-html
flake8 --max-line-length=100 --format=html --htmldir=flake-report **/*.py
```

Open flake-report/index.html with your browser.


## Environment variables

See ```dot_env_example``` file.

### SQLALCHEMY_DATABASE_URL

Used as the URL to connect to the database.

### PUBLIC_KEY_FILE_PATH

File path where public key will be stored (or loaded if URL is not correctly working).

### PUBLIC_KEY_URL

When system starts (or when ```update_public_key``` is executed), a REST call will be made to that URL to get the public key. If rest call is not successful, PUBLIC_KEY_FILE_PATH file will be loaded.

To force public key, we could for example:

```python
from mumichaspy.fastapi_jwt_chassis.config import config
...
if config.public_key is None:
    config.update_public_key()
```

### JWT_ISSUER

When validating a JWT, provided issuer (iss) will be checked.

### JWT_ALGORITHM

The algorithm used for JWT validation (RS256 by default)


## License

MIT license (see LICENSE), provided WITHOUT WARRANTY.