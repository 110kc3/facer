import jwt
import json
import sys

json_file = open(sys.path[0] + '/well_known.json')
json_keys = json.load(json_file)
json_file.close()

public_keys = {}
for jwk in json_keys['keys']:
    kid = jwk['kid']
    public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))


def get_auth_header(headers):
    try:
        token_header = headers["Authorization"]
        token = token_header.split("Bearer ")[1]
        if (len(token) == 0):
            raise ValueError(
                '{"code": 401, "message": "Invalid authorization header"}')
        return verify_token_signature(token)
    except:
        raise ValueError(
            '{"code": 401, "message": "Invalid authorization header"}')


def verify_token_signature(jwt_token):
    try:
        header_kid = jwt.get_unverified_header(jwt_token)['kid']
        key = public_keys[header_kid]
        return jwt.decode(
            jwt_token, key=key, algorithms=['RS256'], do_time_check=True)
    except:
        raise ValueError(
            '{"code": 401, "message": "Invalid authorization header"}')
