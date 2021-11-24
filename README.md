# Userman2

## Development

### Setup

1. Install dependencies:

   - Python 3 ([Django 1.11 supports 3.4, 3.5, 3.6, or 3.7](https://docs.djangoproject.com/en/1.11/releases/1.11/))
   - Yarn
   - `libldap-common`, `libldap2-dev` and `libsasl2-dev`
       - `apt install libldap-common libldap2-dev libsasl2-dev` on Debian/Ubuntu
       - On macOS see https://stackoverflow.com/questions/43328378/python-ldap-macos-valueerror-option-error

2. Create a [Python virtual environment]:

```
python3 -m venv venv
```

3. Activate the virtual environment in your shell:

```
source venv/bin/activate
```

4. Install Python dependencies into the virtual environment:

```
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

5. Install JS dependencies:

```
yarn install
```

6. Copy default configuration:

```
cp userman2/local.py.example userman2/local.py
```

[Python virtual environment]: https://chriswarrick.com/blog/2018/09/04/python-virtual-environments/

### Running

Activate the virtual environment (see above) and run:

```
./manage.py runserver
```

Userman2 should now be reachable at http://localhost:8000/.
