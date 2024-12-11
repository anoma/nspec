# Example Subsystem

This folder contains an example subsystem with example engines.

## Minimum Template

This engine template can be used as a quick start template for writing new engines.

To use it, copy the files and replace the engine name:

```bash
for p in '' _messages _config _environment _behaviour; do
  sed '
    s/template\([-_]\)\minimum/some\1example/g;
    s/Template\( \)\?Minimum/Some\1Example/g;
  ' examples/template_minimum$p.juvix.md > test/some_example$p.juvix.md
done
```

!!! note "sed command"

    On Mac & BSD systems use `gsed` instead of `sed`.
