# Stationeers SaveFile Debug Tools

A set of tools for dealing with corrupted files in stationeers

## What is this?

I keep running to issues with corrupted savefiles, I've created this repo to manage my scripts.  Feel free to use them?

## How do I use it?

For right now, use git to clone the repo, then in the repo directory run:

```
> pipenv install
Installing dependencies from Pipfile.lock (faed75)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 1/1 — 00:00:01
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.

> pipenv run python StationeersSaveFileDebugTools.py --help
Usage: StationeersSaveFileDebugTools.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate_start_condition
  restore_atmo
```

There are two utilities, the first can be used to restore atmospheres from a previous save file, the second is used to generate `startconditions.xml` from a savefile.  Both are explained in the wiki

## Does it work on Windows?

It's python, so probably.. but I haven't tested it because developing things on windows is irritating

## I have another question

Great, let me know what it is and I'll add it here


