import chunk

def all():
    chunk.add_user('sevauk', ['a', 'b', 'c'])
    chunk.register_chunk('d', 'sevauk')
    chunk.register_chunk('a', 'matt')
    chunk.register_chunk('z', 'paul')
    chunk.remove_user('matt')
    chunk.register_chunk('a', 'joe')
    chunk.register_chunk('d', 'matt')
    chunk.register_chunk('chunk', 'sevauk')
    chunk.register_chunk('chunk', 'matt')
    chunk.register_chunk('chunk', 'marc')
    chunk.remove_chunk('chunk')
    chunk.remove_chunk('b')
    chunk.remove_chunk('c')
    assert chunk.has_user_chunk('d', 'sevauk')
    assert chunk.chunks == {'a': ['sevauk', 'joe'], 'z': ['paul'], 'd': ['sevauk', 'matt']}
    assert chunk.users == {'paul': ['z'], 'marc': [], 'sevauk': ['a', 'd'], 'joe': ['a'], 'matt': ['d']}

