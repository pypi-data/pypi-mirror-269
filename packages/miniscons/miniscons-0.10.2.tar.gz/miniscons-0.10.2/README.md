# Miniscons

SCons builders.

![Review](https://img.shields.io/github/actions/workflow/status/JoelLefkowitz/miniscons/review.yml)
![Version](https://img.shields.io/pypi/v/miniscons)
![Downloads](https://img.shields.io/pypi/dw/miniscons)
![Quality](https://img.shields.io/codacy/grade/97f4a968fe554186b58c2f49903a09f4)
![Coverage](https://img.shields.io/codacy/coverage/97f4a968fe554186b58c2f49903a09f4)


## Motivation

When writing an `SConstruct.py` configuration it is difficult to:

- Specify libraries and warnings for each build since the default environment is global.
- Declare executable targets that depend on builds and don't need to be built themselves
- Parse outputs from `conan` to get include paths for build dependencies since they don't appear in the exported `conandeps`
- Declare and chain together aliases for external scripts

We can use `miniscons` to keep the `SConstruct.py` file short and get an interface like this:

```
builds:
  build
  tests

targets:
  start -> build
  test -> tests

scripts:
  clang-tidy
  cppclean

routines:
  lint -> [clang-tidy, cppclean]

flags:
  --dump
```

## Installation

```bash
pip install miniscons
```

## Documentation

Documentation and more detailed examples are hosted on [Github Pages](https://joellefkowitz.github.io/miniscons).

##  Usage

Parse the `SConscript_conandeps` if you are using `conan`:

```py
from miniscons import conan

env, includes = conan()
```

Add the builds with their specific warning flags and libs to include:

```py
from miniscons import Build, flags
from walkmate import tree

build = Build(
    "build",
    tree("src", r"\.cpp$", ["main.cpp"]),
    flags("c++11", ["shadow"]),
)

tests = Build(
    "tests",
    tree("src", r"\.cpp$", ["main.cpp"]),
    flags("c++11"),
    ["gtest"],
)
```

Add the executable targets that depend on the builds with their runtime arguments:

```py
from miniscons import Target

start = Target("start", build)

test = Target("test", tests, ["--gtest_brief"])
```

Add the scripts to invoke your tooling:

```py
from miniscons import Script
from walkmate import tree

cppclean = Script("cppclean", ["."])

tidy = Script(
    "clang-tidy",
    [tree("src", r"\.(cpp)$"), "--", [f"-I{i}" for i in includes]],
)
```

Add the routines and flags for your interface:

```py
from miniscons import Flag, Routine

lint = Routine("lint", [cppclean, tidy])

dump = Flag("--dump")
```

Register all the declarations with the environment and add handlers for each flag:

```py
from miniscons import Tasks
from SCons.Script.Main import GetOption

cli = Tasks(
    [build, tests],
    [start, test],
    [tidy, cppclean],
    [lint],
    [dump],
)

cli.register(env)

if GetOption("dump"):
    cli.dump()
```

Now if we run

```sh
scons --dump
```

We get our interface:

```
scons: Reading SConscript files ...

builds:
  build
  tests

targets:
  start -> build
  test -> tests

scripts:
  clang-tidy
  cppclean

routines:
  lint -> [clang-tidy, cppclean]

flags:
  --dump
```

## Discussion

Why not use a simple task runner for scripts and routines?

Some scripts need access to the include paths that appear in the `SConstruct.py` file so they need to be integrated into the scons workflow.

## Tooling

### Tests

To run tests:

```bash
thx test
```

### Documentation

To generate the documentation locally:

```bash
thx docs
```

### Linters

To run linters:

```bash
thx lint
```

### Formatters

To run formatters:

```bash
thx format
```

## Contributing

Please read this repository's [Code of Conduct](CODE_OF_CONDUCT.md) which outlines our collaboration standards and the [Changelog](CHANGELOG.md) for details on breaking changes that have been made.

This repository adheres to semantic versioning standards. For more information on semantic versioning visit [SemVer](https://semver.org).

Bump2version is used to version and tag changes. For example:

```bash
bump2version patch
```

### Contributors

- [Joel Lefkowitz](https://github.com/joellefkowitz) - Initial work

## Remarks

Lots of love to the open source community!

<p align='center'>
    <img width=200 height=200 src='https://media.giphy.com/media/osAcIGTSyeovPq6Xph/giphy.gif' alt='Be kind to your mind' />
    <img width=200 height=200 src='https://media.giphy.com/media/KEAAbQ5clGWJwuJuZB/giphy.gif' alt='Love each other' />
    <img width=200 height=200 src='https://media.giphy.com/media/WRWykrFkxJA6JJuTvc/giphy.gif' alt="It's ok to have a bad day" />
</p>
