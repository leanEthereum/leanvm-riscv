# Contributing to leanvm-riscv

The workspace uses stable Rust for builds and Clippy, nightly rustfmt for formatting, and Python 3.9 or newer for the repository commands.

Install the CI tools once:

```bash
cargo install cargo-nextest cargo-sort cargo-machete taplo-cli
rustup component add clippy
rustup toolchain install nightly --component rustfmt
```

Run `python3 scripts/check.py full` before opening a pull request.

## Command reference

| Command | Purpose | Options |
| --- | --- | --- |
| `fast` | Check all host targets without running them | `--package NAME` |
| `test` | Run tests through `cargo-nextest` | `--package NAME` |
| `doctest` | Run documentation tests | `--package NAME` |
| `lint` | Run the CI lint checks | `--check sort\|toml\|deps\|clippy\|docs\|fmt` |
| `full` | Run every routine host check | none |

Use `--dry-run` before the command name to print a recipe without running it.
