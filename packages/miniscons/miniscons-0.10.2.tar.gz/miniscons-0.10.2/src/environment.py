import os
import psutil
from emoji import emojize
from SCons.Environment import Environment
from SCons.Script import SConscript


def conan(
    path: str = "SConscript_conandeps", defines: list[str] | None = None
) -> tuple[Environment, list[str]]:
    if defines is None:
        defines = []

    exported = SConscript(path)

    conandeps = exported["conandeps"]
    conandeps["CPPDEFINES"].extend(defines)

    env = Environment(
        **conandeps,
        CXXCOMSTR=emojize(":wrench: Compiling $TARGET"),
        LINKCOMSTR=emojize(":link: Linking $TARGET"),
        ENV={"PATH": os.getenv("PATH", "")},
        num_jobs=psutil.cpu_count(),
    )

    includes = [
        include
        for dependency in exported.values()
        if isinstance(dependency, dict)
        for include in dependency["CPPPATH"]
    ]

    return (env, includes)
