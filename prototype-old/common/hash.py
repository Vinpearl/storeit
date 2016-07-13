class Hash:
    """chunk data hashes."""

    __hsh_int = 0
    __hsh_str = '0'

    def __init__(self, hsh):

        if isinstance(hsh, str):
            self.__hsh_str = hsh
            self.__hsh_int = int(hsh, 16)
        else:
            self.__hsh_str = hex(hsh)[2:]
            self.__hsh_int = hsh

    def __str__(self):
        return self.__hsh_str

    def pretty(self):
        h_size = 4
        return self.__hsh_str[:h_size] + '...' + self.__hsh_str[-h_size:]

    def __eq__(self, other):
        return other.__hsh_int == self.__hsh_int

    def __hash__(self):
        return self.__hsh_int
