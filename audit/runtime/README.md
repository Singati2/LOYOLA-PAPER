# Optional adapter for the audit environment

The audit environment exposes a process namespace in which Lean's lookup of `/proc/<getpid()>/exe` fails, while `/proc/self/exe` works. `lean_proc_self.c` redirects only that lookup for the calling process. It does not change Lean proof code, the kernel or theorem statements.

For this audit the official Lean 4.34.1 release was used, with its pinned Mathlib dependencies. The adapter was compiled with `cc -shared -fPIC -o lean_proc_self.so lean_proc_self.c -ldl`, and the resulting absolute path supplied in `LD_PRELOAD` when running the verifier. `LEAN_SYSROOT`, `LAKE_HOME` and `PATH` pointed to the extracted official toolchain. Ordinary environments should run `formal/verify.sh` normally without this adapter.
