# Evaluating AI Agents — Workshop

In this workshop you build a small AI agent with **Google ADK** (Agent Development Kit),
give it a tool, and then learn how to **evaluate** it.

> ## 👉 Before the workshop
>
> Please complete **Part 0, Part 1 and Part 2** at home. It takes about **15-20 minutes**,
> mostly waiting for downloads. Installing over conference Wi-Fi might be slow, and this way
> we can spend the workshop on the fun part.
>
> You're ready when the [final check](#25-final-check-talk-to-your-agent) works.
> If you get stuck, see [Troubleshooting](#troubleshooting) at the bottom of this page.
> If you're still stuck after using trying out the guide - no worries, we will sort it out together during the workshop!

**Contents**

- [Before you start: how to open a terminal](#before-you-start-how-to-open-a-terminal)
- [Part 0 — Prerequisites](#part-0--prerequisites-do-this-before-the-workshop): Python, Git, VS Code, API key
- [Part 1 — Download the workshop code](#part-1--download-the-workshop-code-do-this-before-the-workshop)
- [Part 2 — One-time setup](#part-2--one-time-setup-do-this-before-the-workshop)
- [Part 3 — During the workshop](#part-3--during-the-workshop)
  - [Run evaluations](#run-evaluations)
- [Challenge: The Unicorn & Parrot](#challenge-the-unicorn--parrot-)
- [Troubleshooting](#troubleshooting)

---

# Before you start: how to open a terminal

A **terminal** is a window where you type commands instead of clicking. You'll
need one to check your installs.

- **macOS:** press **Cmd + Space**, type `Terminal`, press **Enter**.
- **Windows:** press the **Windows key**, type `PowerShell`, and click **Windows PowerShell**.
  (Not "Command Prompt" and not "PowerShell ISE".)
- **Linux:** press **Ctrl + Alt + T**, or open "Terminal" from your applications menu.

**How to run a command:** copy the line from a grey box on this page, paste it into
the terminal, and press **Enter**.

- Paste on macOS: **Cmd + V**
- Paste on Windows / Linux: **Ctrl + V** (in some Linux terminals: **Ctrl + Shift + V**)

> 💡 After installing a program, **close the terminal and open a new one**.
> An old terminal window doesn't know about programs installed after it was opened.

---

# Part 0 — Prerequisites (do this BEFORE the workshop)

## 0.1 Python

**Required: Python 3.12 or newer.** This guide uses **3.12** in every command.

> Already have Python 3.13 or 3.14? That works too. Replace `3.12` with your version
> in every command on this page (for example `python3.13` or `py -3.13`).

### Install it

**macOS — option A (recommended, no extra tools):**

1. Go to <https://www.python.org/downloads/macos/>
2. Under "Stable Releases", find the newest **3.12.x** entry.
3. Download the **macOS 64-bit universal2 installer** (`.pkg`).
4. Open it and follow the installation steps (click **Continue** / **Agree** / **Install**).

**macOS — option B (if you already use Homebrew):**

```bash
brew install python@3.12
```

**Windows:**

1. Go to <https://www.python.org/downloads/windows/>
2. Under "Stable Releases", find the newest **3.12.x** entry.
3. Download **Windows installer (64-bit)** (`.exe`).
4. Run it. On the **first screen**, before clicking anything else:
   - ✅ tick **"Add python.exe to PATH"** (bottom of the window)
   - ✅ make sure **"Install launcher for all users"** / py launcher is ticked
5. Then click **"Install Now"**.
6. When it says "Setup was successful", click **Close**.

**Linux (Debian/Ubuntu):**

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```

> If you see `Unable to locate package python3.12` (older Ubuntu, e.g. 22.04), add the
> deadsnakes repository first, then run the install command again:
> ```bash
> sudo add-apt-repository ppa:deadsnakes/ppa
> sudo apt update
> ```

**Linux (Fedora):**

```bash
sudo dnf install python3.12
```

### Verify your Python

Open a **new** terminal window and run:

**macOS / Linux**

```bash
python3.12 --version
```

**Windows**

```powershell
py -3.12 --version
```

Expected output: a line starting with `Python 3.12.`, for example:

```
Python 3.12.11
```

If you get `command not found` / `is not recognized`, see
[Troubleshooting → Python not found](#t1-python312-command-not-found--python-is-not-recognized).

## 0.2 Git

Git is how you download the workshop repository and switch between workshop branches.
**You don't need a GitHub account.**

- **macOS:** open a terminal and run `git --version`. If Git isn't installed, macOS
  offers to install the "command line developer tools". Click **Install** and wait.
  (Or download it from <https://git-scm.com/downloads>.)
- **Windows:** go to <https://git-scm.com/downloads>, click **Windows**, download the
  64-bit installer, run it and **accept all the defaults** (just keep clicking **Next**).
- **Linux:** `sudo apt install git` (Debian/Ubuntu) or `sudo dnf install git` (Fedora).

### Verify Git

Open a **new** terminal and run:

```bash
git --version
```

Expected: any version 2.x is fine.

```
git version 2.39.5
```

## 0.3 VS Code (code editor)

Any editor works, but this guide gives exact steps for **Visual Studio Code**.

1. **Install:** <https://code.visualstudio.com/download>. Download it for your OS,
   run the installer and accept the defaults.
   - **macOS:** the download is a `.zip`. Unzip it and drag
     `Visual Studio Code.app` into your `Applications` folder, then open it
     from there. (If you run it from Downloads it will complain later.)
   - **Windows:** on the "Select Additional Tasks" screen, keep **"Add to PATH"** ticked.
   - **Linux (Debian/Ubuntu):** download the `.deb` file, then double-click it, or run
     `sudo apt install ./code_*.deb` from the folder where you downloaded it.
2. **Install the Python extension** (you need this to pick the right interpreter):
   - Open VS Code.
   - Click the **Extensions** icon in the far-left vertical bar. It looks like
     four small squares. (Shortcut: **Cmd+Shift+X** on macOS, **Ctrl+Shift+X** on
     Windows/Linux.)
   - In the search box at the top, type `Python`.
   - Pick the first result: **"Python"**, publisher **Microsoft**, with a blue
     check mark and millions of downloads.
   - Click the blue **Install** button.

## 0.4 A free Google Gemini API key

The workshop agent needs an API key to talk to a Gemini model. The free tier is enough
for the whole workshop.

1. Open <https://aistudio.google.com> in your browser.
2. Sign in with a **personal Google account** if asked.
   > ⚠️ Corporate Google Workspace accounts are often blocked from AI Studio by
   > an admin policy. If you see "You don't have access" or the API keys page is
   > missing, use a personal @gmail.com account instead.
3. In the **left-hand menu**, click **"API keys"**.
4. Click the blue **"Create API key"** button.
5. If asked to pick a project, accept the suggested one or choose
   **"Create API key in new project"**.
6. A long string starting with **`AIza`** appears. Click the **copy** icon.
7. **Paste it somewhere safe right now** (a notes app is fine). The full key is
   shown only once, but you can always create another one.

> 🔒 Treat the key like a password: don't post it in chat, screenshots, or on GitHub.

---

# Part 1 — Download the workshop code (do this BEFORE the workshop)

### 1.1 Open a terminal inside VS Code

1. Open **VS Code**.
2. In the top menu, click **Terminal → New Terminal**.
   A terminal panel opens at the bottom of the window.
   - On Windows it should say **powershell** at the top right of the panel. That's what we want.

### 1.2 Download (clone) the repository

Run these two commands, one at a time:

```bash
cd ~
git clone https://github.com/teamlida/atd-eval-ai-agents.git
```

`cd ~` goes to your home folder, and `git clone` downloads the workshop into a new
folder there called `atd-eval-ai-agents`.

Expected: a few lines ending with something like `Resolving deltas: 100% ... done.`

### 1.3 Open the folder in VS Code

1. In the top menu, click **File → Open Folder…** (macOS: **File → Open…**).
2. Go to your home folder and select the **`atd-eval-ai-agents`** folder.
   - macOS: your home folder is the one with the house icon, named after your user.
   - Windows: `C:\Users\<your name>`
   - Linux: `/home/<your name>`
3. Click **Open** (or **Select Folder** on Windows).
4. If VS Code asks **"Do you trust the authors of the files in this folder?"**,
   click **"Yes, I trust the authors"**.

You should now see `README.md` in the file list on the left.

### 1.4 Open a terminal in the workshop folder

Click **Terminal → New Terminal** again. This new terminal opens **inside the
workshop folder**. All the remaining commands in this guide are typed here.

> ✅ To double-check, the line where you type should end with `atd-eval-ai-agents`
> (for example `~/atd-eval-ai-agents $` or `PS C:\Users\anna\atd-eval-ai-agents>`).

---

# Part 2 — One-time setup (do this BEFORE the workshop)

Do Part 2 **once**. Don't repeat it when you switch branches during the workshop.

### 2.1 Create a virtual environment

A **virtual environment** (the `.venv` folder) is a private box for this project's
Python packages, so they don't mess with anything else on your computer.

In the VS Code terminal (inside the workshop folder), run:

**macOS / Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

Expected: the start of your terminal line now shows **`(.venv)`**, for example:

```
(.venv) ~/atd-eval-ai-agents $
```

> **Windows:** if you see an error with `running scripts is disabled on this system`,
> see [Troubleshooting → T2](#t2-windows-running-scripts-is-disabled-on-this-system).

### 2.2 Install Google ADK (with the eval module)

With `(.venv)` showing, run:

```bash
pip install "google-adk[eval]"
```

This downloads a lot of packages and can take **a few minutes**. Wait until you get
your terminal line back. Some yellow `WARNING` lines are fine. Red `ERROR` lines are not.

Check that it works:

```bash
adk --version
```

Expected: a version number, for example `adk, version 2.14.1`.

### 2.3 Tell VS Code to use the virtual environment

1. Press **Cmd+Shift+P** (macOS) or **Ctrl+Shift+P** (Windows/Linux).
   A search box opens at the top.
2. Type `Python: Select Interpreter` and press **Enter**.
3. Pick the entry that mentions **`.venv`** (it often also says "Recommended").

From now on, VS Code activates `.venv` automatically in **new** terminals, and code
completion works in the agent files.

### 2.4 Create your agent

Run from the workshop folder:

```bash
adk create my_agent
```

Answer the questions like this (type the number, then press **Enter**):

```
Choose a model for the root agent:
1. gemini-3.5-flash
2. gemini-3.8-flash
3. Other models (fill later)
Choose model (1, 2, 3): 1
1. Google AI
2. Vertex AI
3. Login with Google
Choose a backend (1, 2, 3): 1
```

When it asks for your **Google API key**, paste the key from step 0.4 and press **Enter**.

Expected: a new `my_agent` folder appears on the left in VS Code, with
`agent.py`, `__init__.py` and `.env` inside. The `.env` file holds your API key.

> Didn't get asked for the key, or pasted the wrong one? Open `my_agent/.env` in
> VS Code and make it look like this (with your real key), then save with
> **Cmd+S** / **Ctrl+S**:
> ```
> GOOGLE_GENAI_USE_ENTERPRISE=0
> GOOGLE_API_KEY=AIza...your-key...
> ```

### 2.5 Final check: talk to your agent

Start the ADK web interface:

```bash
adk web --port 8000
```

Wait until you see a line like `Uvicorn running on http://127.0.0.1:8000`, then:

1. Open <http://localhost:8000> in your browser.
2. In the top-left dropdown, select **`my_agent`**.
3. Type `Hello!` in the chat box and press **Enter**.

✅ **If the agent replies, you're all set for the workshop!** 🎉

To stop the web interface, click in the terminal and press **Ctrl+C** (on macOS too,
it's **Ctrl**, not Cmd).

> Got an error instead of a reply? See [Troubleshooting](#troubleshooting).

---

# Part 3 — During the workshop

### Coming back to the project (every time)

1. Open VS Code. It usually reopens the workshop folder. If not, use
   **File → Open Folder…** and select `atd-eval-ai-agents`.
2. Open **Terminal → New Terminal**.
3. Check that the line starts with **`(.venv)`**. If it doesn't, activate it:
   - macOS / Linux: `source .venv/bin/activate`
   - Windows: `.venv\Scripts\activate`

**You don't need to reinstall anything.** Git ignores the `.venv` folder, so it
stays put when you switch branches.

### Get the latest version

The workshop materials may get small updates after you've cloned them. At the start
of the workshop, run:

```bash
git pull
```

### Switching branches

The workshop moves through these branches. Each one contains the finished code
for a step, so you can catch up any time:

| Branch | What it adds |
|---|---|
| `main` | Instructions only |
| `agent-with-tool` | `my_agent` with the `get_user_data` tool |
| `eval-agent` | Eval set and test config for `my_agent` |
| `challenge` | secret challenge |

To switch, run:

```bash
git checkout -f <branch-name>
```

For example: `git checkout -f agent-with-tool`

`-f` replaces your agent files with the versions from the branch. Your `.venv` and
your `my_agent/.env` (API key) are kept.

> ⚠️ If you've made changes you want to keep, copy them somewhere else first.
> Don't run `git clean -x`, because it deletes `.venv`.

### Run the web interface

```bash
adk web --port 8000
```

Run this command from the workshop folder, which contains your `my_agent/` folder,
then open <http://localhost:8000>.

### Run evaluations

An **evaluation** runs your agent on saved test conversations (an **eval set**)
and scores how close its answers and tool calls come to the expected ones.

From the workshop folder, with `(.venv)` showing, run this as **one line**:

```bash
adk eval my_agent my_agent/eval_set_1.evalset.json --config_file_path my_agent/test_config.json --print_detailed_results
```

What each part means:

- `my_agent`: the agent to test.
- `my_agent/eval_set_1.evalset.json`: the test conversations to run.
- `--config_file_path my_agent/test_config.json`: the criteria and thresholds to use.
- `--print_detailed_results`: shows the score for every criterion, for every case.
  Leave it out to see only the pass/fail summary.

Each case calls the Gemini model, so it can take a little while. At the end you see
which eval cases **passed** and which **failed**, with their scores.

> Getting `429` / `RESOURCE_EXHAUSTED`? See [T7](#t7-429--resource_exhausted--quota-errors).

---

# Challenge: The Unicorn & Parrot 🍺

Welcome to **The Unicorn & Parrot**, a pub in Potsdam. Its bartender, **Polly** the parrot,
is a chatbot that takes drink orders. Polly has bugs. Your job is to find them and
prove them with evals.

**👉 The pub's page: <https://teamlida.github.io/atd-eval-ai-agents/>**

The page has the menu, the house rules and the register's tools, plus a register you can try
yourself. **The page is always right.** Whenever Polly says or does something that
doesn't match it, you've found a bug.

### Your mission

Find **at least 4 bugs** and cover **each one with an eval that fails**:

- **2 deterministic evals**: checked exactly, with `tool_trajectory_avg_score`
  (did Polly call the right tools with the right inputs?) or `response_match_score`.
- **2 non-deterministic evals**: checked by an LLM judge, with
  `rubric_based_final_response_quality_v1` (does the answer follow a rule you write?).

> An eval that catches a bug **fails**. That's the goal! If your eval passes, either
> the bug isn't there, or the eval doesn't check what you think it checks.

### Set up

From the workshop folder, with `(.venv)` showing:

```bash
git checkout -f challenge
```

Give Polly your API key by copying the `.env` file you made for `my_agent`:

- macOS / Linux: `cp my_agent/.env beer_agent/.env`
- Windows: `Copy-Item my_agent\.env beer_agent\.env`

Then start the web interface and pick **`beer_agent`** in the top-left dropdown:

```bash
adk web --port 8000
```

### Find a bug

1. Read a house rule on the pub page.
2. Try to make Polly break it in the chat.
3. Click the events on the left of `adk web` to see which tools Polly called, with which
   inputs, and what the register answered. Compare with the page.

### Turn the bug into an eval

The quickest way is to record the conversation where the bug happened:

1. In `adk web`, open the **Eval** tab and create a new eval set, for example `test`.
2. Reproduce the bug in a **new session**, then click **Add current session** to `test`.
   ADK saves it to `beer_agent/test.evalset.json`.
3. ⚠️ **The recorded case expects exactly what Polly did, bug included.** Open the file in
   VS Code and correct the expectation:
   - **Deterministic:** fix the `function_call` entries (tool `name` and `args`) to what
     Polly *should* have called, or the `final_response` text to what he should have said.
   - **Non-deterministic:** leave the case as it is. The rubric in the config does the checking.
4. Create a config for your eval in `beer_agent/`, for example `trajectory_config.json`:

   ```json
   { "criteria": { "tool_trajectory_avg_score": 1.0 } }
   ```

   or, for an LLM judge, `rubric_config.json`, with a rule from the pub page in your own words:

   ```json
   {
     "criteria": {
       "rubric_based_final_response_quality_v1": {
         "threshold": 0.8,
         "judge_model_options": { "judge_model": "gemini-3.5-flash-lite", "num_samples": 1 },
         "rubrics": [
           {
             "rubric_id": "my_rule",
             "rubric_content": { "text_property": "Write the rule the answer must follow here." }
           }
         ]
       }
     }
   }
   ```

5. Run **only your new case**: add `:` and the case's `eval_id` to the file name.

   ```bash
   adk eval beer_agent beer_agent/test.evalset.json:<eval_id> --config_file_path beer_agent/trajectory_config.json --print_detailed_results
   ```

> 💡 Some bugs only show up some of the time. Add `--num_runs 3` to run a case
> several times.
>
> 💡 Free API keys allow about 15 requests per minute, and every chat message or eval
> run uses a few. If you hit `429`, wait a minute: that's a quota, not a bug. 
> Reach out to us and we will help.

---

# Troubleshooting

### T1. `python3.12: command not found` / `python is not recognized`

- **Close the terminal and open a new one**, then try again. Terminals opened before
  the install don't see it. In VS Code, close and reopen **VS Code itself**.
- **macOS:** make sure the installer from python.org finished. Then try
  `/usr/local/bin/python3.12 --version`. If that works, use that full path in step 2.1
  instead of `python3.12`.
- **Windows:**
  - Use `py -3.12`, not `python3.12`. That command doesn't exist on Windows.
  - If `py` isn't recognized either, run the Python installer again, choose
    **Modify**, and make sure **"py launcher"** is ticked. Then choose **Next** →
    tick **"Add Python to environment variables"** → **Install**.
  - If typing `python` opens the **Microsoft Store**: open **Settings → Apps →
    Advanced app settings → App execution aliases** and turn **off** the two
    entries for "python.exe" and "python3.exe".
- **Linux:** run `sudo apt install python3.12 python3.12-venv` again and check for errors.

### T2. Windows: `running scripts is disabled on this system`

PowerShell blocks the activation script by default. Run this once (it only affects
your user account), then try `.venv\Scripts\activate` again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Type `Y` and press **Enter** if it asks to confirm.

### T3. `adk: command not found` / `adk is not recognized`

The virtual environment isn't active (your terminal line doesn't start with `(.venv)`).
Activate it:

- macOS / Linux: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

Make sure you're in the workshop folder first. If the activate command says the file
doesn't exist, you're in the wrong folder (see step 1.4) or you skipped step 2.1.

### T4. `git: command not found` / `git is not recognized`

Git isn't installed, or the terminal was opened before installing it. Install it
(step 0.2), then **close and reopen VS Code** and try again.

### T5. `error: The following untracked working tree files would be overwritten by checkout`

You forgot the `-f`. Run the command again as `git checkout -f <branch-name>`.

### T6. The agent replies with an error about the API key (`API key not valid`, `401`, `403`)

- Open `my_agent/.env` and check that `GOOGLE_API_KEY=` is followed by your full key,
  with **no spaces and no quotes**.
- Save the file, stop `adk web` with **Ctrl+C**, and start it again.
- If it still fails, create a new key in AI Studio (step 0.4) and paste that one.

### T7. `429` / `RESOURCE_EXHAUSTED` / quota errors

You've hit the free-tier rate limit. Wait a minute and try again.

### T8. `address already in use` / port 8000 is busy

Another `adk web` is still running, maybe in another terminal. Stop it with **Ctrl+C**,
or use a different port: `adk web --port 8001`, then open <http://localhost:8001>.

### T9. `my_agent` doesn't appear in the dropdown in the browser

Run `adk web` from the **workshop folder** (the one that *contains* `my_agent`), not
from inside `my_agent` itself.

### T10. macOS: `SSL: CERTIFICATE_VERIFY_FAILED`

Open **Finder → Applications → Python 3.12** and double-click
**`Install Certificates.command`**. Then try again.

### T11. Starting over

Only if your environment is really broken: delete it and repeat Part 2, steps 2.1–2.3.

- macOS / Linux: `rm -rf .venv`
- Windows: `Remove-Item -Recurse -Force .venv`

Your `my_agent` folder and API key are not affected.
