# emoji-xcompose

Emoji through the Compose key on Linux, in the spirit of
[WinCompose](https://github.com/samhocevar/wincompose) and
[mac-compose](https://github.com/adericbourg/mac-compose):

| Keys                         | Result          |
|------------------------------|-----------------|
| `Compose Compose s o b`      | 😭              |
| `Compose Compose + 1`        | 👍              |
| `Compose Compose h e a r t`  | ❤️              |
| `Compose Compose t f l i p`  | (╯°□°)╯︵ ┻━┻   |

It generates a plain `~/.XCompose` include, so it works wherever the system Compose
handling reads `~/.XCompose` (libxkbcommon: KDE/GNOME on Wayland, Qt, Chromium, Firefox…).
No daemon or input method is needed.

## Install

Requires `python3` and network access (the emoji lists are fetched at install time).

```sh
git clone https://github.com/adericbourg/emoji-xcompose
cd emoji-xcompose
./install.sh
```

This writes `~/.XCompose.emoji` and makes sure `~/.XCompose` includes it:

- if `~/.XCompose` doesn't exist, it is created with `include "%L"` (your locale's standard
  Compose sequences) and the emoji include;
- if it exists, the include is appended (after a backup to `~/.XCompose.bak`);
- running it again refreshes the emoji list and leaves `~/.XCompose` alone.

Then log out and back in. You need a Compose key set up in your keyboard settings.

## Names

Names are [gemoji](https://github.com/github/gemoji) short names (the GitHub/Slack ones),
plus WinCompose's emoji names and a few custom entries (`CUSTOM` in `gen_emoji_xcompose.py`).

Limits, due to how XCompose works:

- **8 characters max.** libxkbcommon ignores sequences longer than 10 keys, and the two
  Compose presses use two of them. About 800 emoji have a name that short.
- **Exact names only**: no fuzzy or prefix search. A sequence can't be a prefix of another
  one, so on conflict the shorter name wins (`heart` over `hearts`), except 1–2 character names,
  which give way (`ok_hand` over `ok`).
- **GTK3 apps** use their own Compose engine with a shorter limit, so only short names may
  work there. GTK4 apps are fine.

For anything else, use your desktop's emoji picker (KDE: `Meta+.`).

## Development

```sh
python3 -m unittest
python3 gen_emoji_xcompose.py            # print the generated rules
```

## License

GPLv3, see [LICENSE](LICENSE). The emoji data is downloaded at install time, not
redistributed: gemoji (MIT) and WinCompose (WTFPL).
