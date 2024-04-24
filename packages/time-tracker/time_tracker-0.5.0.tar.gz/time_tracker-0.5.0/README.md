# `time-tracker`

Time tracker cli

**Usage**:

```console
$ time-tracker [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `log`
* `track`: Run depending on mode

## `tt log`

**Usage**:

```console
$ time-tracker log [OPTIONS]
```

**Options**:

* `-l, --last`: Open last log file  [default: False]
* `-o, --output`: Return log file content to terminal  [default: False]
* `--help`: Show this message and exit.

## `tt track`

Run depending on mode

**Usage**:

```console
$ tt track [OPTIONS]
```

**Options**:

* `-w, --workDuration INTEGER`: Set work time (minutes)  [default: 25]
* `-b, --breakDuration INTEGER`: Set break time (minutes)  [default: 5]
* `-B, --bigBreakDuration INTEGER`: Set break time (minutes)  [default: 30]
* `-m, --mode [manual|pomodoro]`: Set pomodoro mode. This will change the flow of work to 4 work sessions with small breaks and finish with a big Break  [default: pomodoro]
* `-p, --prompt`: Set if it should prompt to go for next session  [default: True]
* `--help`: Show this message and exit.
