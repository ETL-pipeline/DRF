from b64uuid import B64UUID
import re
# from uuid import uuid1




# id = "2413fb3709b05939f04cf2e92f7d0897fc2596f9ad0b8a9ea855c7bfebaae892"
# bid = B64UUID(id[32:])
dict_method = {'GET':1, 'PUT':2, 'POST':3, 'DELETE':4} 

dict_levelname = {'DEBUG':1, 'INFO':2, 'WARNING':3, 'ERROR':4, 'CRITICAL':5}

#dict_url = {}

dictlist = []
dictlist.append(dict_method)

dictlist.append(dict_levelname)
#dictlist.append(dict_url)

class Compress:


    

    def compress_id(self,id):

        cid = str(B64UUID(id[:32])) + str(B64UUID(id[32:]))
        return cid

    def resub(self,date):

        new = re.sub(r"[^0-9]", "", date)
        return str(new)
    
    def transform_method(self,data):

        if data in dictlist[0]:
            return dictlist[0][data]

    def transform_levelname(self,data):

        if data in dictlist[1]:
            return dictlist[1][data]



    
# dict_method = {'GET':1, 'PUT':2, 'POST':3, 'DELETE':4} 

# dict_levelname = {'DEBUG':1, 'INFO':2, 'WARNING':3, 'ERROR':4, 'CRITICAL':5}

#dict_url = {}

    

