import json_log_formatter
import datetime
from pythonjsonlogger import jsonlogger
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        log_record['environment'] = 'django'

# https://docs.python.org/ko/3/library/logging.html 참고
class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        # 로그된 메세지
        extra['message'] = message
        # 메세지의 텍스트 로깅 수준
        extra['levelname'] = record.__dict__['levelname']
        # extra['name'] = record.__dict__['name'] # 로거이름
        extra['lineno'] = record.__dict__['lineno'] # 소스 행 번호?
        extra['filename'] = record.__dict__['filename'] # pathname의 파일명
        extra['pathname'] = record.__dict__['pathname'] # 로깅호출이 일어난 소스파일 전체 경로명
        extra['created'] = record.__dict__['created'] # LogRecord가 생성된 시간(time.time())
        request = extra.pop('request', None)
        if request:
            # HTTP Header 중 하나로 HTTP Server 에 요청한 Client 의 IP 를 식별하기 위한 표준
            extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
        return extra

# 현수 님 코드
# 
class CustomisedJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):
        if extra.get('request', 0):
            _request = extra['request']
            extra['url'] = _request.__str__().split("'")[-2]
            extra['method'] = _request.method
            if not extra['url'].replace('/api/boards/', ''):
                pass
            else:
                extra['board_id'] = int(
                    extra['url'].replace('/api/boards/', ''))

            if _request.__dict__['_auth']:
                extra['user_id'] = _request.__dict__['_auth']['user_id'] ^ 0
                # user_id 해싱
                # extra['user_id'] = hashing_userid
            else:
                extra['user_id'] = None

        extra['name'] = record.__dict__['name']
        extra['inDate'] = datetime.fromtimestamp(
            record.__dict__['created']).strftime('%Y-%m-%dT%X.%f')[:-3]+'Z'
        extra['detail'] = {'message': message,
                           'levelname': record.__dict__['levelname']}
        request = extra.pop('request', None)
        if request:
            extra['x_forward_for'] = request.META.get('X-FORWARD-FOR')
        return extra