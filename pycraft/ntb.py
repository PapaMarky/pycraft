import python_nbt.nbt as nbt

def read_bytes(data):
    _type = nbt.NBTTagByte(buffer=data).value
    return nbt.TAGLIST[_type](buffer=data)
