import json_log_formatter
from b64uuid import B64UUID
from datetime import datetime
from pythonjsonlogger import jsonlogger
from .hash import hashing_userid
from .compression import Compress

class MyCustomJsonFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):

        cp = Compress()

        if extra.get('request', 0):
            _request = extra['request']
            extra['url'] = _request.__str__().split("'")[-2]
            tran_method = cp.transform_method(_request.method)
            extra['method'] = tran_method
            if not extra['url'].replace('/blog/', ''):
                pass
            else:
                extra['board_id'] = int(extra['url'].replace('/blog/', '')[:-1])
            
            
            if str(_request.user) != 'AnonymousUser':
                               
                hid = hashing_userid(_request.user)
                cid = cp.compress_id(hid)
                extra['user_id'] = cid
                                
            else:
                extra['user_id'] = None

        time_str_compress_format = "%y%m%d%H%M%S%f"
        time_str_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        
        time = datetime.fromtimestamp(record.__dict__['created']).strftime('%Y-%m-%dT%X.%f')[:-3]+'Z'
        time_for_convert = datetime.strptime(time, time_str_format)       
        
        extra['inDate'] = datetime.strftime(time_for_convert, time_str_compress_format)[:-3]
       
        tran_levelname = cp.transform_levelname(record.__dict__['levelname'])
        extra['detail'] = {'message': message, 'levelname': tran_levelname}
        #extra['detail'] = {'message': message, 'levelname': record.__dict__['levelname']}
        request = extra.pop('request', None)
        # HTTP Header 중 하나로 HTTP Server 에 요청한 Client 의 IP 를 식별하기 위한 표준
        # if request:
        #     extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
        return extra
