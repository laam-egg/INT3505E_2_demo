#!/bin/bash

set +e  # allow all collections to run

cd "$(dirname "$0")"

mkdir -p newman-reports

ERRORS=0
for f in ./*.postman_collection.json; do
    base=$(basename "$f" .postman_collection.json)
    echo "▶ Running $base..."
    newman run "$f" -r htmlextra --reporter-htmlextra-export "newman-reports/${base}.html"
    if [ $? -ne 0 ]; then
        echo "❌ $base failed"
        ERRORS=1
    else
        echo "✅ $base passed"
    fi
    done
    if [ $ERRORS -ne 0 ]; then
        echo "💥 Some Newman collections failed"
        exit 1
    fi
