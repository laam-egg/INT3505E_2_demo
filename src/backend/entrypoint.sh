#!/bin/bash
set -e

# If JWT_SECRET_KEY is not set or empty, generate a random one
if [ -z "$JWT_SECRET_KEY" ]; then
    echo "Generating dynamic JWT Secret..."
    export JWT_SECRET_KEY=$(python -c "import os; print(os.urandom(32).hex())")
else
    echo "Using provided JWT Secret."
fi

# Execute the CMD from Dockerfile (flask run ...)
exec "$@"
