import json_log_formatter
from datetime import datetime
from .hash import hashing_userid
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
                extra['user_id'] = hashing_userid(_request.user)
            else:
                extra['user_id'] = None

        # extra['name'] = record.__dict__['name']
        extra['inDate'] = datetime.fromtimestamp(record.__dict__['created']).strftime('%Y-%m-%dT%X.%f')[:-3]+'Z'
        extra['detail'] = {'message': message, 'levelname': record.__dict__['levelname']}
        request = extra.pop('request', None)
        # HTTP Header 중 하나로 HTTP Server 에 요청한 Client 의 IP 를 식별하기 위한 표준
        # if request:
        #     extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
        return extra

# "Watching for file changes with StatReloader" >> DEBUG = False 시 해결
# path info 뜨는건 수정했을 때마다 한번씩 뜨는듯