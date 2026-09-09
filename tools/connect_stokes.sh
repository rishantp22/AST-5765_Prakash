#!/bin/bash
# Rishant Prakash - connect to Stokes for this homework session.
set -euo pipefail
if [[ $# -ne 1 || ! "$1" =~ ^[a-zA-Z]+[0-9]+$ ]]; then
  printf 'Usage: bash tools/connect_stokes.sh YOUR_NID\n' >&2
  exit 2
fi
course_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
socket_dir="${course_dir}/../audit/runtime/ssh"
mkdir -p "$socket_dir"
chmod 700 "$socket_dir"
printf 'Enter your UCF password only at the SSH prompt.\n'
printf 'Leave this Terminal window open while the homework runs.\n'
printf 'The connection closes 10 minutes after its last session ends.\n'
exec ssh -M -S "$socket_dir/stokes" \
  -o ControlPersist=10m -o ServerAliveInterval=60 \
  -o ServerAliveCountMax=3 "$1@stokes.ist.ucf.edu"
