import python_nbt.nbt as nbt


def read_bytes(data):
    _type = nbt.NBTTagByte(buffer=data).value
    # The line below has some side effects that cause the data to actually be loaded.
    # Without it everything comes back empty
    _name = nbt.NBTTagString(buffer=data).value
    return nbt.TAGLIST[_type](buffer=data)
