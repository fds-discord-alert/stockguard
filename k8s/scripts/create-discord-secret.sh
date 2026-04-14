#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <DISCORD_WEBHOOK_URL> [namespace]"
  exit 1
fi

WEBHOOK_URL="$1"
NAMESPACE="${2:-default}"

kubectl create secret generic discord-secret \
  --from-literal=webhook_url="$WEBHOOK_URL" \
  -n "$NAMESPACE" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "✅ discord-secret created/updated in namespace: $NAMESPACE"
