# leanvm-riscv

A RISC-V (rv64im) zkVM proven with the binary [Plonky3](https://github.com/Plonky3/Plonky3) backend.

**Status:** empty workspace. Nothing is implemented yet.

## Layout

| crate | role |
| --- | --- |
| `crates/isa` | rv64im decoding into instruction classes and the bytecode table |
| `crates/elf` | loads a guest ELF into a program and its initial memory image |
| `crates/emulator` | reference interpreter producing the execution record |
| `crates/circuits` | Boolean circuits of the instruction classes |
| `crates/memory` | registers, RAM and advice as timestamped read-write memories |
| `crates/chips` | one table per instruction class |
| `crates/precompiles` | precompile tables reached through custom instructions |
| `crates/prover` | witness generation, machine declaration, prove and verify |
| `crates/riscv` | public API |
| `crates/cli` | command-line entry point |

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Licensed under either of [Apache License, Version 2.0](LICENSE-APACHE) or [MIT license](LICENSE-MIT) at your option.
