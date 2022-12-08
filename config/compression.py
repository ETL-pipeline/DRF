from b64uuid import B64UUID
from uuid import uuid1

uid = uuid1()
print(uid)
print(str(uid))
id = "2413fb3709b05939f04cf2e92f7d0897fc2596f9ad0b8a9ea855c7bfebaae892"
bid = B64UUID(id[32:])
print(bid)
breakpoint()