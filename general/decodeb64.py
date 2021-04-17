import base64

msg = 'bDNhcm5fdGgzX3IwcDM1'
b64_bytes = msg.encode('ascii')
message_bytes = base64.b64decode(b64_bytes)
message = message_bytes.decode('ascii')
print(message)
