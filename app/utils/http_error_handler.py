import json


def http_error_handler(error):
    if(not isinstance(error, ValueError)):
        return json.dump(str(error)), 500
    json_error = json.loads(str(error))
    code = json_error["code"]
    message = json_error["message"]
    return json.dump(message), code
