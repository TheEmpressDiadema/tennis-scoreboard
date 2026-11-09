#!/usr/bin/env bash
#
# create_configs.sh
# Creates config files in root folder:
#   db_config.toml, test_db_config.toml, server_security.toml

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

create_file() {
    local path="$1"
    if [[ -e "$path" ]]; then
        echo "SKIP: $(basename "$path") already exists"
    else
        cat > "$path"
        echo "OK:   created $(basename "$path")"
    fi
}

# ---------- db_config.toml ----------
create_file "${PROJECT_ROOT}/db_config.toml" <<'EOF'
[mysql]
host = 'your host here'
port = 'your port here'
database = 'database_name_here'
driver = 'mysql+pymysql'
EOF

# ---------- test_db_config.toml ----------
create_file "${PROJECT_ROOT}/test_db_config.toml" <<'EOF'
[mysql]
host = 'your host here'
port = 'your port here'
database = 'database_name_here'
driver = 'mysql+pymysql'
EOF

# ---------- server_security.toml ----------
create_file "${PROJECT_ROOT}/server_security.toml" <<'EOF'
[mysql]
user = 'your db username'
password = 'db password'
EOF
