# coredumpy

coredumpy saves your crash site so you can better debug your python program.

## Highlights

* Easy to use
* Supports pdb interface
* Does not rely on pickle
* Dump file is independent of environment

## Usage

### dump

You can dump any frame (and its parent frames) manually by

```python
from coredumpy import dump

dump("coredumpy_dump", frame)

# without frame argument, it will dump the current frame stack
dump("coredumpy_dump")
```

You can hook the exception so a dump will be automatically created if your program crashes due to an exception

```python
from coredumpy import patch_excepthook
patch_excepthook()
```

### load