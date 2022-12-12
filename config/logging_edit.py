import json_log_formatter
from datetime import datetime
from .hash import hashing_userid
from b64uuid import B64UUID
import re
class MyCustomJsonFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        if extra.get('request', 0):
            _request = extra['request']
            extra['url'] = _request.__str__().split("'")[-2]
            extra['method'] = _request.method
            try:
                extra['board_id'] = int(extra['url'].replace('/blog/', '')[:-1])
            except:
                pass
            if str(_request.user) != 'AnonymousUser':
                # extra['user_id'] = _request.__dict__['_auth']['user_id'] ^ 0
                # print(_request.__dict__['_auth']['user_id'] ^ 0)
                # user_id 해싱
                id = hashing_userid(_request.user)
                extra['user_id'] = str(B64UUID(id[:32])) + str(B64UUID(id[32:]))
            else:
                extra['user_id'] = None
        time_str_compress_format = "%y%m%d%H%M%S%f"
        time_str_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        time = datetime.fromtimestamp(record.__dict__['created']).strftime('%Y-%m-%dT%X.%f')[:-3]+'Z'
        time_for_convert = datetime.strptime(time, time_str_format)       

        extra['inDate'] = datetime.strftime(time_for_convert, time_str_compress_format)[:-3]
        extra['detail'] = {'message': message, 'levelname': record.__dict__['levelname']}
        extra.pop('request', None)
        compress(extra)
        # HTTP Header 중 하나로 HTTP Server 에 요청한 Client 의 IP 를 식별하기 위한 표준
        # if request:
        #     extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
        return extra

# "Watching for file changes with StatReloader" >> DEBUG = False 시 해결
# path info 뜨는건 수정했을 때마다 한번씩 뜨는듯

def compress(data):
    dic1 = {
        'GET':'0',
        'POST':'1',
        'PUT':'2',
        'HEAD':'3',
        'DELETE':'4',
        'PATCH':'5',
        'OPTIONS':'6'
    }
    try:
        data['method'] = dic1[data['method']]
        data['url'] = data['url'][1:-1]
    except:
        pass
    # if data['user_id']:
    #     data['user_id'] = str(B64UUID(id[:32])) + str(B64UUID(id[32:]))
    dic2 = {
        'DEBUG':'0', 
        'INFO':'1', 
        'WARN':'2', 
        'ERROR':'3', 
        'FATAL':'4'
    }
    data['detail']['levelname'] = dic2[data['detail']['levelname']]

    # time = data['inDate']
    # time_edited = re.sub('[^0-9]','', time)
    # data['inDate'] = time_edited[2:]
    return data