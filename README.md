# 🎮 Engine Room: A Chromium Replay
*From URL to pixels to your first landed Chromium CL.*

This is a **playable** — an interactive course that runs inside your AI coding agent. It ships as this repository: a **Replay** you clone, boot, and play. There are no videos to watch and no chapters to read. There is a working environment, a sequence of predicaments, and a tutor that lives in your agent. It will discuss anything with you — except the answers.

The model is the console. Your agent IDE is the controller. This repo is the Replay. The conversation is you playing.

---

## Quickstart
You need: an agent IDE or CLI (Claude Code, Cursor, Windsurf, Google Antigravity — anything that auto-loads repo instruction files), Python 3, and git. You bring your own model subscription; this Replay never sees an API key.

```bash
git clone <REPLAY_REPO_URL>
cd Engine-Room
```
Open the folder in your agent tool. 

> 💡 **Terminal tip**: Keep a terminal window open in your IDE to run companion commands (like `python3 replay.py status` or to execute code). In Cursor/VS Code, you can toggle the terminal panel using **`Ctrl + \``** (backtick) or **`Cmd + J`** (macOS).

Then, in your agent's chat, type anything:
```text
hi
```
That's it. The tutor detects there's no save file, automatically verifies your environment, asks a couple of calibration questions, and drops you into Unit 1. The setup guide is the first conversation.

Coming back later? Open the repo and type:
```text
where was I?
```
You'll get a twenty-second recap and land back in your predicament.

---

## Commands & Primitives

You can execute these commands either by running them in your **terminal** or typing their equivalent in the **agent chat**:

| Terminal Command | Chat Equivalent | Description |
| :--- | :--- | :--- |
| `python3 replay.py start` | `/start` or `Show brief` | Read the predicament brief for your active level |
| `python3 replay.py map` | `/map` or `Show map` | Display the visual sub-system map & Chromium reference |
| `python3 replay.py status` | `/status` or `Show status` | View your completion state and mastered concepts |
| `python3 replay.py checkpoint` | `/checkpoint` | Run mechanical verification tests to trigger your oral exam |
| `python3 replay.py resources [concept]` | `/resources [concept]` | Fetch specifications, references, and Chromium source files for a concept |
| `python3 replay.py doctor` | `/doctor` | Run diagnostics on your local game environment |
| `python3 replay.py pass_level` | `/pass_level` | Unlock the next level after passing oral examination |

---

## How It Plays

*   **Predicaments, not lessons.** Each unit opens with a situation: something is broken, missing, or mysterious in a real browser engine codebase. Your job is to get unstuck. The tutor will explain anything, go down any rabbit hole, and demand predictions before giving explanations — but it will not hand you the diagnosis. Being wrong out loud is the core mechanic.
*   **Two modes, always announced.** By default the tutor is your collaborator — nothing is graded, ask anything. When you type `/checkpoint`, it becomes your examiner: no hints, adversarial questions, hidden test suites. You pass or you don't. The boundary is yours to cross and never crossed secretly.
*   **Checkpoints are showdowns.** Talking fluently about CSS specificity is not the same as understanding it. A checkpoint is where your understanding meets something that can't be talked into agreeing with you. Passing one unlocks the next unit and writes a save commit to your log (`checkpoint: level-01 CSS specificity cascade resolved`).
*   **The final showdown is real.** The Replay ends with an actual CL submitted to Chromium's Gerrit, reviewed by an actual Chromium reviewer. No test suite to game, no AI to shortcut it. What you walk away with is an artifact trail — commits, diffs, writeups, and a landed change — that lives in your fork and is yours.
*   **Stuck?** Type `/hint` for the smallest Socratic nudge that gets you moving. Frustration is the game working; despair is not — the hints are graduated for a reason.

---

## Reference & Learning Materials

*   [Chromium Engine Architecture & Subsystems](file:///Users/sergiorojas/Desktop/Engine-Room/context/chromium_architecture.md): Deep-dive into Chromium's process models, layered dependency directory structure (base, mojo, services, content, components, chrome), and its 11 major subsystems.
*   [Chromium Gamepad API & System Architecture](file:///Users/sergiorojas/Desktop/Engine-Room/context/gamepad_system.md): Grounding guide to help you understand how Chromium hooks up to controllers, the shared memory design, and the platform refactoring required for Issue 40275102.
*   **Ask for Resources**: Whenever you start a new challenge or unlock a new level, remember that you can ask the Socratic tutor in the chat for additional resources, references, or deep-dives into any browser engine or Chromium concepts introduced on the map.

---

## Saving and Resuming

The Replay saves itself; you mostly don't think about it.

| File | What it is |
| :--- | :--- |
| `.game/progress.json` | Your save slot — current unit, checkpoints passed |
| `.game/journal.md` | The tutor's notes on your journey — what you've earned, where you struggled |
| `git log` | Save points — every checkpoint pass is a commit; the log is your completion record |

Type `/save` before closing your laptop if you want a manual save.

> ⚠️ **The console has amnesia.** The model remembers nothing between sessions — everything that matters lives in the files above, which the tutor reads on every boot. Your save lives in your copy of the repo, so work in your fork.

---

## Troubleshooting

| Symptom | Fix |
| :--- | :--- |
| **Tutor acts like a generic assistant** | Your agent didn't load the instruction file. Confirm `CLAUDE.md` is present in the repo root and your tool auto-loads it. |
| **Cursor errors on `/save` or command execution** | Switch Cursor to **Agent / Composer** mode (press `Cmd + I` or `Ctrl + I`) instead of "Ask/Chat" mode so the model has permissions to run commands and write files. |
| **First boot runs again** | `.game/progress.json` is missing — you cloned fresh instead of your fork. Your save lives in your copy of the repository. |
| **Environment broken after a break** | Ask the agent: *"diagnose my environment"*. It will run `python replay.py doctor` and walk you through repairs. |
| **Tutor reveals answers too easily** | Tell it: *"You are breaking the Replay rules — re-read the firmware in CLAUDE.md."* The firmware wins arguments. |

---

## The One Habit That Makes This Work

A book can be read passively. This medium punishes passivity and pays out on engagement. Bring predictions, bring wrong mental models, bring half-formed questions — the conversation is the one part of a playable that can't be packaged, because it has to be generated live, by you, every time.

**Insert Replay. Power on. Play.**

---
*A Lore Replay. Built to be played in any agent IDE.*
