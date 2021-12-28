import jwt
import json

json_file = open("./well_known.json")
json_keys = json.load(json_file)
json_file.close()

public_keys = {}
for jwk in json_keys['keys']:
    kid = jwk['kid']
    public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))


def verify_token_signature(jwt_token):
    try:
        header_kid = jwt.get_unverified_header(jwt_token)['kid']
        key = public_keys[header_kid]
        return jwt.decode(
            jwt_token, key=key, algorithms=['RS256'], do_time_check=True)
    except Exception as i:
        raise Exception(i, 403)
