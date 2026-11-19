#!/bin/sh
# Install emoji Compose sequences for the current user. Safe to re-run.
set -eu

cd "$(dirname "$0")"
python3 gen_emoji_xcompose.py "$HOME/.XCompose.emoji"

conf="$HOME/.XCompose"
inc='include "%H/.XCompose.emoji"'
if [ ! -e "$conf" ]; then
    # %L keeps the system Compose sequences of the current locale.
    printf 'include "%%L"\n%s\n' "$inc" > "$conf"
    echo "Created $conf"
elif ! grep -qF "$inc" "$conf"; then
    cp "$conf" "$conf.bak"
    printf '%s\n' "$inc" >> "$conf"
    echo "Added the emoji include to $conf (backup: $conf.bak)"
fi

echo "Done. Log out and back in for running applications to pick it up."
