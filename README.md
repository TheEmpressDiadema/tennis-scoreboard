# Tennis scoreboard python backend project

## Technologies:
Back-end: `python Waitress`  
Databases: `MySql\Mariadb`   
ORM: `sqlalchemy`  
migrations: `alembic`  
Tests: `pytest`  
Linters: `mypy`, `ruff`   
Dependency-management: `uv`  

## How to run the project:

### Step 1. Sync requirements

Install uv and sync dependencies:

```bash
pip install uv
uv sync
```

### Step 2. Generate config files

Create necessary `.toml` files in the project root directory:
`db_config.toml`, `test_db_config.toml` and `server_security.toml`.  

**Linux / macOS** — execute `create_configs.sh` from the project root directory:

```bash
bash create_configs.sh
```

**Windows** — execute `create_configs.bat` from the project root directory

Scripts are not rewriting existing files, so relaunch won't clear settings.  

### Step 3. Fill in the settings of the created files

For `test_db_config.toml` and `db_config.toml`

```toml
[mysql]
host = 'your host here'
port = 'your port here'
database = 'database_name_here'
driver = 'mysql+pymysql'
```

For `server_security.toml`:

```toml
[mysql]
user = 'your db username'
password = 'db password'
```

Replace plugs with real MySql server settings to use.

### Step 4. Run!

```uv run tennis-scoreboard```