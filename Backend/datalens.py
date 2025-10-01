import time
import jwt
import json
from settings import private_key
# private_key = private_key


now = int(time.time())
payload = {
      'embedId': "8e0tatm9jpjit",
      'dlEmbedService': "YC_DATALENS_EMBEDDING_SERVICE_MARK",
      'iat': now,
      'exp': now + 3600,
      "params": {}
}

encoded_token = jwt.encode(payload, private_key, algorithm='PS256')
print(encoded_token)