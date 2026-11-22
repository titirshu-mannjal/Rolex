# Instructions for Claude

If the user asks you to install this repository (for example "install this repo" or "install https://github.com/titirshu-mannjal/Rolex"):

1. Clone it if it is not already on disk: `git clone --depth 1 https://github.com/titirshu-mannjal/Rolex.git`
2. Show the user the packs (`bash install.sh --list`) and say that `core` is the default Instagram video stack.
3. Run `bash install.sh` for core, or `bash install.sh --packs core,blender,...` / `bash install.sh --all` if the user asked for more.
   Add `--tools` to install yt-dlp, auto-editor, whisper-ctranslate2, edge-tts and DepthFlow through uv.
4. Report the summary line (installed / skipped / failed), list any failures, and any MISSING system tools with the command to install them on the user's OS (ffmpeg, Node.js 18+, Python 3.10+, uv).
5. Tell the user to restart Claude Code.

Never delete existing skills: the installer moves replaced folders to `~/.claude/rolex-backup/<timestamp>/`.
On Windows, run the installer from Git Bash or WSL.
