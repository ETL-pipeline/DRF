import json_log_formatter
from b64uuid import B64UUID
from datetime import datetime
from pythonjsonlogger import jsonlogger
from .hash import hashing_userid
from .compression import Compress
# class CustomJsonFormatter(jsonlogger.JsonFormatter):
#     def add_fields(self, log_record, record, message_dict):
#         super(CustomJsonFormatter, self).add_fields(
#             log_record, record, message_dict)
#         if not log_record.get('timestamp'):
#             # this doesn't use record.created, so it is slightly off
#             now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
#             log_record['timestamp'] = now
#         if log_record.get('level'):
#             log_record['level'] = log_record['level'].upper()
#         else:
#             log_record['level'] = record.levelname
#         log_record['environment'] = 'django'

# # https://docs.python.org/ko/3/library/logging.html 참고
# class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
#     def json_record(self, message, extra, record):
#         # 로그된 메세지
#         extra['message'] = message
#         # 메세지의 텍스트 로깅 수준
#         extra['levelname'] = record.__dict__['levelname']
#         # extra['name'] = record.__dict__['name'] # 로거이름
#         extra['lineno'] = record.__dict__['lineno'] # 소스 행 번호?
#         extra['filename'] = record.__dict__['filename'] # pathname의 파일명
#         extra['pathname'] = record.__dict__['pathname'] # 로깅호출이 일어난 소스파일 전체 경로명
#         extra['created'] = record.__dict__['created'] # LogRecord가 생성된 시간(time.time())
#         request = extra.pop('request', None)
#         if request:
#             extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
#         return extra

# 현수 님 코드
# class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
#     def json_record(self, message, extra, record):
#         if extra.get('request', 0):
#             _request = extra['request']
#             extra['url'] = _request.__str__().split("'")[-2]
#             extra['method'] = _request.method
#             if not extra['url'].replace('/api/boards/', ''):
#                 pass
#             else:
#                 extra['board_id'] = int(
#                     extra['url'].replace('/api/boards/', ''))

#             if _request.__dict__['_auth']:
#                 extra['user_id'] = _request.__dict__['_auth']['user_id'] ^ 0
#                 # user_id 해싱
#                 # extra['user_id'] = hashing_userid
#             else:
#                 extra['user_id'] = None

#         extra['name'] = record.__dict__['name']
#         extra['inDate'] = datetime.fromtimestamp(
#             record.__dict__['created']).strftime('%Y-%m-%dT%X.%f')[:-3]+'Z'
#         extra['detail'] = {'message': message,
#                            'levelname': record.__dict__['levelname']}
#         request = extra.pop('request', None)
#         if request:
#             extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
#         return extra
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
            
            print('[', _request.user,']')
            if str(_request.user) != 'AnonymousUser':
                #extra['user_id'] = _request.__dict__['_auth']['user_id'] ^ 0
                # print(_request.__dict__['_auth']['user_id'] ^ 0)
                # user_id 해싱
                
                #hid = HashDjango.hashing_userid(_request.user)
                hid = hashing_userid(_request.user)
                #print(type(hid))
                #print(hid)
                cid = cp.compress_id(hid)
                extra['user_id'] = cid
                #print(B64UUID(hid).string)
                #extra['user_id'] = hashing_userid(_request.user)
                #print(type(cid))
                #print(cid)
                
                #breakpoint()
                #print(extra['user_id'])
                #breakpoint()   # 
            else:
                extra['user_id'] = None

        # extra['name'] = record.__dict__['name']
        #indate = datetime.fromtimestamp(record.__dict__['created']).strftime('%Y-%m-%dT%X.%f')[:-3]+'Z'
        #print(type(indate))
        #newindate = cp.resub((indate))[2:]
        #print(type(newindate))
        #extra['inDate'] = str(newindate)
        extra['inDate'] = datetime.fromtimestamp(record.__dict__['created']).strftime('%Y-%m-%dT%X.%f')[:-3]+'Z'
        #print(type(extra['inDate']))
        #breakpoint()
        tran_levelname = cp.transform_levelname(record.__dict__['levelname'])
        extra['detail'] = {'message': message, 'levelname': tran_levelname}
        #extra['detail'] = {'message': message, 'levelname': record.__dict__['levelname']}
        request = extra.pop('request', None)
        # HTTP Header 중 하나로 HTTP Server 에 요청한 Client 의 IP 를 식별하기 위한 표준
        # if request:
        #     extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
        return extra
