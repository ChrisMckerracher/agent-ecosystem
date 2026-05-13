# Baseline smoke test: state of the repo before strip-and-rename epic begins

Captured as Task 0 (`claude_stuff-xi6.1`) of the strip-and-rename epic. Documents
the *starting* state so before/after comparisons are unambiguous and the
pre-existing latent bug is on record before any code is touched.

## Cache layout

`ls -la /Users/chrismck/.claude/plugins/cache/agent-ecosystem-marketplace/agent-ecosystem/0.14.1/`:

```
drwxr-xr-x@ 12 chrismck  staff  384 May 11 10:51 .
drwxr-xr-x@  3 chrismck  staff   96 Feb 28 10:18 ..
drwxr-xr-x@  3 chrismck  staff   96 Feb 28 10:18 .claude-plugin
drwxr-xr-x@  6 chrismck  staff  192 May 12 19:31 .in_use
drwxr-xr-x@  9 chrismck  staff  288 Feb 28 10:18 agents
drwxr-xr-x@ 18 chrismck  staff  576 Feb 28 10:18 commands
drwxr-xr-x@  6 chrismck  staff  192 Feb 28 10:18 dashboard
drwxr-xr-x@  6 chrismck  staff  192 Feb 28 10:18 hooks
drwxr-xr-x@ 11 chrismck  staff  352 Feb 28 10:18 lib
drwxr-xr-x@  6 chrismck  staff  192 Feb 28 10:18 scripts
drwxr-xr-x@ 19 chrismck  staff  608 Feb 28 10:18 skills
drwxr-xr-x@  4 chrismck  staff  128 Feb 28 10:18 templates
```

**Confirmed:** no `plugin/` subdir in the cache. The marketplace flattens the
plugin contents directly under the version directory. Anything that prefixes
paths with `plugin/` against `${CLAUDE_PLUGIN_ROOT}` is broken at runtime.

## Test script output

`./scripts/test-ecosystem.sh` from repo root:

```
Testing Agent Ecosystem...

PASS: beads installed
FAIL: plugin directory missing
```

Exit code: `1` (FAIL). The script checks `$HOME/.claude/plugins/local/agent-ecosystem`,
which does not exist on this machine — only the marketplace cache path is
populated. Failure is environmental (no `local/` install), not a code regression.

## Latent path bug demonstration

`plugin/agents/architecture.md:132` instructs the architect agent to invoke:

```
${CLAUDE_PLUGIN_ROOT}/plugin/scripts/decompose-init.sh
```

With `CLAUDE_PLUGIN_ROOT=/Users/chrismck/.claude/plugins/cache/agent-ecosystem-marketplace/agent-ecosystem/0.14.1`:

| Path attempted | Result |
|---|---|
| `${CLAUDE_PLUGIN_ROOT}/plugin/scripts/decompose-init.sh` (as written) | `ls: ... No such file or directory` |
| `${CLAUDE_PLUGIN_ROOT}/scripts/decompose-init.sh` (no prefix) | exists, executable, 4779 bytes |

**Latent bug confirmed.** The `plugin/` prefix in the agent prompt does not
match the marketplace cache layout. The architect agent's `/decompose` step
would fail at runtime against a marketplace-installed plugin. This pre-dates
the strip-and-rename epic — it is part of the motivation for promoting
`plugin/` to repo root (which collapses the two layouts into one).

## Conclusion

- Cache layout: no `plugin/` subdir (as predicted).
- Test script: FAIL on missing `~/.claude/plugins/local/agent-ecosystem` (environmental).
- Latent path bug: confirmed — `${CLAUDE_PLUGIN_ROOT}/plugin/...` resolves to nothing in the marketplace cache.

Baseline established. Subsequent tasks (T1+) can be evaluated against this
snapshot to show the strip-and-rename does not introduce these failures and,
in the case of the path bug, eliminates it.
