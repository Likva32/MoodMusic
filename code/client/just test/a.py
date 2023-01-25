import json

data1 = {'Name': 'artur', 'Email': 'arturtkach32@gmail.com', 'Passwords': '123', 'Code': '83a70f8b-9231-410b'}

b = json.dumps(data1, indent=2)
print(b)

c = json.loads(b)
print(c)
print(type(c))

print(c['Name'])

del c['Name']
print(c)