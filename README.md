This is a Unity3D URP Project that acts as a framework to build off upon in order to create a simple Unity3D multiplayer game.

The code is very barebones, with only simple lobby joining and player syncing, But it would be quite simple to add other synced values and features such as lobby leaving.

## Quick Run Helper (Python)

A new helper script `run_game.py` was added to make starting the project easier.

### 1) Run a built game (default mode)

```bash
python3 run_game.py
```

- By default this searches for a runnable build inside `./Build`.
- You can pass an explicit executable path:

```bash
python3 run_game.py --mode build --build-path "Build/MyGame.exe"
```

### 2) Open the project in Unity Editor

```bash
python3 run_game.py --mode editor
```

- By default it uses `unity` from PATH.
- You can set a custom Unity binary:

```bash
python3 run_game.py --mode editor --unity-path "/path/to/Unity"
```

or via environment variable:

```bash
UNITY_EDITOR_PATH="/path/to/Unity" python3 run_game.py --mode editor
```
