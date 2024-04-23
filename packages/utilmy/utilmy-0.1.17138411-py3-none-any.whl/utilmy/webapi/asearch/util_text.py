"""

https://pypi.org/project/text-dedup/


https://chenghaomou.github.io/text-dedup/

https://github.com/seomoz/simhash-py/tree/master


pip install simhash-pybind

import simhash
v1="abc"
v2="abc"

a = simhash.compute(v1)
b = simhash.compute(v2)
simhash.num_differing_bits(a, b)


"""

import uuid

def uuid_64():
    ## 64 bits integer UUID
    return uuid.uuid4().int & ((1 << 64) - 1)








