import os
from dataclasses import dataclass, field
from SCons.Environment import Environment


@dataclass
class Build:
    name: str

    files: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    libs: list[str] = field(default_factory=list)

    output: str = "dist"
    shared: bool = False

    def __repr__(self) -> str:
        return self.name

    @property
    def target(self) -> str:
        return os.path.join(self.output, self.name)

    def path(self, file: str) -> str:
        root = os.path.splitext(os.path.normpath(file))[0]
        return f"{root.replace('.', '-')}-[{self.name}]"

    def nodes(self, env: Environment) -> list[str]:
        return [
            env.Object(self.path(file), file, CXXFLAGS=self.flags)
            for file in self.files
        ]

    def register(self, env: Environment) -> None:
        libs = env["LIBS"] + self.libs

        if self.shared:
            outputs = env.Library(self.target, self.nodes(env), LIBS=libs)
            env.Alias(self.name, outputs[0])
        else:
            env.Program(self.target, self.nodes(env), LIBS=libs)
            env.Alias(self.name, self.target)
