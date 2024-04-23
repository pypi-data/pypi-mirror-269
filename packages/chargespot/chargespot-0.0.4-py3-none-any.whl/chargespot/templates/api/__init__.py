from chargespot.api_decorator import request_mapping, Requester, Method
from chargespot.api_decorator import add_header, add_headers, get_session
from chargespot.api_decorator import before_request, after_response, RequestObject, ResponseObject

RequestMapping = request_mapping
BeforeRequest = before_request
AfterResponse = after_response