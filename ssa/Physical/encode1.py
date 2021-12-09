import base64
import json
data=dict()
data['happy']=123456
message = str(json.dumps(data)+'\n')
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')

print(message,base64_message)
