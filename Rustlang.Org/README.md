# Rustlang.Org

Sample Rust programs from rustlang.org, along with notes on how to get my dev
environment working.

```bash
code --version
# 1.37.1
# f06011ac164ae4dc8e753a3fe7f9549844d15e35
# x64
uname -a
# Linux ub 5.0.0-25-generic #26-Ubuntu SMP Thu Aug 1 12:04:58 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```

## VSCode Build, Run, and Debug

In order to build, run, and debug Rust programs from VS Code, you need to
install the following 2 extensions:

```
Name: Rust (rls)
Id: rust-lang.rust
Description: Rust language support - code completion, Intellisense, refactoring, reformatting, errors, snippets. A client for the Rust Language Server, built by the RLS team.
Version: 0.6.1
Publisher: rust-lang
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust

Name: CodeLLDB
Id: vadimcn.vscode-lldb
Description: Debug your native code with LLDB.
Version: 1.3.0
Publisher: Vadim Chugunov
VS Marketplace Link: https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb
```

`rust-lang.rust` is a general purpose extension for Rust. Specifically, it helps
VSCode find the rust toolchain, and talks to the Rust Language Server (`rls`),
providing code completion and linting. It probably does more than that, but
those are the 2 most important in my opinion.

`vadimcn.vscode-lldb` is the extension that allows VSCode to debug rust
applications. It does a lot more than that, but you can go read all about [LLDB
and LLVM on http://lldb.llvm.org](http://lldb.llvm.org/), because it's way over
my head honestly.

The interaction between these 2 only takes a few configuration options in the
local `launch.json`. I've tried using the recommended base launch action, since
it uses cargo to build and run, meaning you shouldn't have to specify any of the
`${workspaceFolder}`-style variables for most use cases. Unfortunately, this
stopped working once I added a loop to `guessing_game`, and my CPU usage
indicated that the program was spinning, meaning "wait for user input" was not
blocking the loop's execution... The new tooling is not perfect by any means.

### Default launch.json for these 2 extensions.

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Launch Rust Console",
            "type": "lldb",
            "request": "launch",
            "preLaunchTask": "build",
            "program": "${workspaceFolder}/target/debug/${workspaceFolderBasename}",
            "args": [],
            "cwd": "${workspaceFolder}",
        }
    ]
}
```

### Default build task in tasks.json

```json
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558 
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build",
            "type": "cargo",
            "subcommand": "build",
            "problemMatcher": [
                "$rustc"
            ]
        }
    ]
}
```
