# Command Line Interface

This python module is used to make your command line / terminal more fancy when printing / logging certain events.

## Quick install

```bash
pip install cli-log
```

## Examples

```python
import cli

cli.info("Hello world!\nInfo event.")
cli.debug("Debug event.")
cli.warn(prefix="CORE", message="Warning event.")
cli.error("Error event.")
```

```log
[16:30:52 / INFO] Hello world!
[16:30:52 / INFO] Info event.
[16:30:52 / DEBUG] Debug event.
[16:30:52 / WARN][CORE] Warning event.
[16:30:52 / ERROR] Error event.
```