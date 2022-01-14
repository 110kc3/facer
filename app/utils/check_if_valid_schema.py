from jsonschema import Draft3Validator
import json
import sys


def check_if_valid_schema(schema_name, request):
    try:
        schema = json.load(open(sys.path[0] + '/app/schemas/' + schema_name))
        if(not Draft3Validator(schema).is_valid(json.loads(request.data))):
            raise ValueError(
                '{"code": 400, "message": "Invalid body format"}')
    except Exception as i:
        print(str(i))
        raise
