import python_nbt.nbt as nbt

def read_bytes(data):
    type = nbt.NBTTagByte(buffer=data).value
    return nbt.TAGLIST[type](buffer=data)
