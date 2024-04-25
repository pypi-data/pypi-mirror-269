


__all__ = [
    'bool',
    'int8',
    'uint8',
    'int16',
    'int32',
    'int64',
    'float',
    'double'
]

def to_ptype(dtype):
    dtype_to_ptype_map = {
        "uint8": "unsigned char",
        "uint16": "unsigned short",
        "uint32": "unsigned int",
        "float32": "float",
        "float64": "double",
    }
    return dtype_to_ptype_map[dtype]

def to_dtype(ptype):
    ptype_to_dtype_map = {
         "unsigned char" : "uint8",
         "unsigned short" : "uint16",
         "unsigned int" : "uint32",
         "float" : "float32",
         "double" : "float64"
    }
    return ptype_to_dtype_map[ptype]