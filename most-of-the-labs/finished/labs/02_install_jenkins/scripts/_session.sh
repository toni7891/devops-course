#!/usr/bin/env bash
# source this file to get $JENKINS_URL, $COOKIE_JAR, $CRUMB_HEADER, $AUTH
JENKINS_URL="http://localhost:8081"
AUTH="admin:admin"
COOKIE_JAR="$(mktemp)"

curl -s -c "$COOKIE_JAR" -u "$AUTH" "$JENKINS_URL/whoAmI/api/json" -o /dev/null
CRUMB_JSON=$(curl -s -b "$COOKIE_JAR" -c "$COOKIE_JAR" -u "$AUTH" "$JENKINS_URL/crumbIssuer/api/json")
CRUMB_FIELD=$(echo "$CRUMB_JSON" | python3 -c "import json,sys;print(json.load(sys.stdin)['crumbRequestField'])")
CRUMB_VALUE=$(echo "$CRUMB_JSON" | python3 -c "import json,sys;print(json.load(sys.stdin)['crumb'])")
CRUMB_HEADER="${CRUMB_FIELD}: ${CRUMB_VALUE}"
