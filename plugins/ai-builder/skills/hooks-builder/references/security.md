# Why a hook is the risky one

A skill that is wrong gives a wrong answer. A hook that is wrong **runs a command**.
It executes with the user's full rights, unattended, on input an agent produced — and
if it is a project hook, it runs on every colleague's machine too.

That is the whole reason this file exists. Nothing here is exotic; it is ordinary shell
discipline, applied somewhere the consequences are unusual.

## The five rules

### 1. Parse structured input as structured data

The payload is JSON. Read it with a JSON parser.

```bash
# fragile: matches the wrong thing as soon as a value contains the pattern
tool=$(grep -o '"tool_name":"[^"]*"' <<< "$input")

# correct
tool=$(jq -r '.tool_name // empty' <<< "$input")
```

Text pattern matching on JSON fails on nested values, on escaped quotes, and on any
field whose content happens to look like another field. Those are not edge cases: file
contents travel in this payload.

```python
data = json.load(sys.stdin)  # correct
path = data.get("tool_input", {}).get("file_path", "")
```

Note the defaults. A missing field must not become a confident empty string that then
passes a check.

### 2. Quote everything, and terminate arguments

```bash
rm $path            # a path with a space becomes two arguments
rm "$path"          # better
rm -- "$path"       # correct: a path starting with - cannot become a flag
```

The `--` matters more than it looks. A path the agent generated could begin with a
dash, and without the terminator it is read as an option to whatever you are running.

### 3. Validate paths rather than trusting them

Check what you were given before acting on it: reject `..`, resolve to an absolute path,
and confirm it is inside the boundary you expect. A hook meant to protect one directory
that never checks containment protects nothing.

Compare after normalisation, not before — `a/../b` and `b` are the same path written two
ways, and only one of them matches a naive string test.

### 4. Never log the payload wholesale

```bash
echo "$input" >> /tmp/hook.log      # writes file contents, and possibly secrets
echo "$tool_name" >> /tmp/hook.log  # writes what you actually need
```

The payload carries the tool's input, which for a write is the file's entire contents.
An audit log that captures it becomes a copy of everything the agent touched, in a
location with no access control. Log the decision, not the material.

### 5. Fail safe, deliberately

Decide, and encode, what happens when the hook itself breaks:

```python
try:
    decision = evaluate(data)
except Exception as exc:
    # A gatekeeper refuses when it cannot decide. Anything else exits non-2,
    # which does NOT block, and the protection silently disappears.
    print(f"BLOCKED: validator failed: {exc}", file=sys.stderr)
    sys.exit(2)
```

For a gatekeeper the safe direction is to refuse; for an observer it is to get out of
the way. Both are defensible — silence about which one you chose is not.

## Two failure modes worth naming

**Failing open under stress.** A validator that crashes on unusual input allows exactly
the cases most worth blocking, because unusual input is what an attack looks like. This
is why step 7 of `SKILL.md` requires deliberately breaking the hook and watching what
happens.

**Being worked around.** A hook that blocks too much teaches people to disable it, and a
disabled hook protects nothing. Over-broad filtering is a security problem, not merely
an annoyance — which is why step 3 asks what the filter catches unintentionally.

## Reviewing someone else's hook

A project hook is a committed instruction to run shell on every contributor's machine.
Before accepting one, read the script, and check: does it parse properly, is every
variable quoted, does it log the payload, does it escalate privilege, and what does it
do when it fails? A hook is the one part of a repository where "looks fine" is not a
review.

## Not verified

The exit-code behaviour these patterns rely on comes from the documentation — see
`events.md`. Confirm with mock input that a non-2 exit really does not block on your
build before trusting a fail-safe path that depends on it.
