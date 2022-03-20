# pycraft
python libs for having fun with minecraft data sets.

Requires python3

## Installing

Build or otherwise obtain the package file: `pycraft-0.0.1-py3-none-any.whl`

Run the command `pip3 pycraft-0.0.1-py3-none-any.whl`

I used a modified version of python-nbt. Once I make a fork and make my version available (or the orginal author applies my changes) I will update this document.

## Building the Package File

Setting up a python build environment is not difficult, but it is beyond the scope of this document. Google is your friend.

To build pycraft into something you can install with pip simply run the command `python3 -m build` from the base directory.

This will create two files under `dist` that can be used to install pycraft:

```
% ls dist
pycraft-0.0.1-py3-none-any.whl	pycraft-0.0.1.tar.gz
```

The tar file tries to build the source and is harder to use.

`pycraft-*.whl` is recommended.
