# emoji-xcompose

Type emoji on Linux with your keyboard's **Compose key**: no emoji picker, no mouse.

| Press, one key after the other | You get        |
|--------------------------------|----------------|
| `Compose` `Compose` `s` `o` `b`         | 😭             |
| `Compose` `Compose` `+` `1`             | 👍             |
| `Compose` `Compose` `h` `e` `a` `r` `t` | ❤️             |
| `Compose` `Compose` `f` `i` `r` `e`     | 🔥             |
| `Compose` `Compose` `t` `f` `l` `i` `p` | (╯°□°)╯︵ ┻━┻  |

Same idea as [WinCompose](https://github.com/samhocevar/wincompose) on Windows and
[mac-compose](https://github.com/adericbourg/mac-compose) on macOS.

## What it does

Linux already has a Compose key feature: press `Compose`, then a few keys, and get a special
character (`Compose` `e` `'` → é). The sequences live in plain text files, and you can add your
own in `~/.XCompose`.

This project adds about 800 emoji sequences to that file, using the emoji names you may know
from GitHub and Slack (`:sob:`, `:+1:`, `:fire:`…). It installs two files in your home folder:

- `~/.XCompose.emoji`: the generated emoji sequences;
- `~/.XCompose`: your personal Compose file. It gets one line that loads the emoji file. If it
  doesn't exist yet, it is created and also keeps your usual Compose sequences (é, ©, →…).

Nothing runs in the background and nothing is installed system-wide. It works in KDE, GNOME and
most other desktops, on Wayland and X11.

## Before you start: get a Compose key

You need a key set up as Compose. Most keyboards don't have one, so you pick an existing key,
usually **Right Alt** (also called AltGr) or **Menu**.

- **KDE Plasma:** System Settings → Keyboard → Key Bindings → tick *Configure keyboard
  options* → *Position of Compose key* → pick a key.
- **GNOME:** Settings → Keyboard → *Compose Key* (under Special Character Entry) → pick a key.
- **sway:** add `input * xkb_options compose:ralt` to your config.
- **Other X11 desktops:** `setxkbmap -option compose:ralt`.

Check it: `Compose` `e` `'` should type é.

## Install

You need `python3` (pre-installed on most distributions) and an internet connection: the emoji
lists are downloaded during installation.

```sh
git clone https://github.com/adericbourg/emoji-xcompose
cd emoji-xcompose
./install.sh
```

The script checks your system first and prints what it finds:

```
Required:
  [ok]   python3 3.12.3
  ...
Your setup (informational, never blocks the install):
  [ok]   Compose key configured (compose:ralt)
  ...
```

- `[FAIL]` means something required is missing. The install stops, **nothing is changed**,
  and the message says what to fix.
- `[warn]` means emoji might not work as expected (no Compose key found, for example). The
  install still goes ahead.

If you already had a `~/.XCompose`, it is kept as is: the script only adds one line at the end,
after saving a copy as `~/.XCompose.bak.<date>`.

**Then log out and log back in.** Applications only read the Compose files when they start.

## Use it

Press `Compose` twice, then type the emoji name. The emoji appears as soon as the name is
complete, with no Enter needed.

To find a name, search the installed file by name or by emoji:

```sh
grep heart ~/.XCompose.emoji
grep 🎉 ~/.XCompose.emoji
```

Names are the GitHub/Slack emoji short names (see this
[cheat sheet](https://github.com/ikatyang/emoji-cheat-sheet)), plus a few extras.

### Limits

- **Names are 8 characters max.** Linux ignores Compose sequences longer than 10 keys, and the
  two `Compose` presses count. Emoji whose names are all longer can't be typed this way (about
  half of them). Use your desktop's emoji picker for those (KDE: `Meta` + `.`).
- **Exact names only.** There's no search or autocompletion while you type.
- **No name can be the start of another one.** When two names clash, the shorter one wins
  (`heart` over `hearts`), except 1–2 letter names, which give way (`ok_hand` over `ok`).
- **Some older apps** (built with GTK 3) handle only shorter sequences, so only short names may
  work in them.

## Update

Run `./install.sh` again (after `git pull` to get the latest version of this project). It
downloads the latest emoji lists and leaves your `~/.XCompose` alone.

## Uninstall

1. Delete `~/.XCompose.emoji`.
2. Remove the line `include "%H/.XCompose.emoji"` from `~/.XCompose`. If the install script
   created that file and you never edited it, delete the whole file.
3. Log out and log back in.

## Troubleshooting

- **Nothing happens:** did you log out and back in? Does `Compose` `e` `'` give é? If not, set
  up the Compose key first (see above).
- **Other Compose sequences work but emoji don't:** check that `~/.XCompose` contains
  `include "%H/.XCompose.emoji"`. If the `XCOMPOSEFILE` environment variable is set, your
  system reads that file instead of `~/.XCompose`: add the include line there.
- **A box or question mark appears instead of the emoji:** your font has no emoji. Install an
  emoji font (e.g. `fonts-noto-color-emoji` on Debian/Ubuntu, `google-noto-emoji-fonts` on
  Fedora).

## Add your own sequences

Add lines to `~/.XCompose`, after the include line:

```
<Multi_key> <Multi_key> <l> <e> <n> <n> <y> : "( ͡° ͜ʖ ͡°)"
```

Pick a name that isn't the beginning of an existing name, and that no existing name is the
beginning of (check with `grep '# len' ~/.XCompose.emoji`). Otherwise one of the two sequences
stops working.
Don't edit `~/.XCompose.emoji`: it is replaced on every install.

## For developers

```sh
python3 -m unittest                 # tests (offline)
python3 gen_emoji_xcompose.py       # print the generated rules
```

Built-in extras (like `tflip`) live in [`custom.txt`](custom.txt).

## License

GPLv3, see [LICENSE](LICENSE). The emoji data is downloaded at install time, not
redistributed: [gemoji](https://github.com/github/gemoji) (MIT) and
[WinCompose](https://github.com/samhocevar/wincompose) (WTFPL).
