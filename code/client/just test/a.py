import pickle

# client
arr = ['q1', 'ans = 50']
data_send = pickle.dumps(arr)
print(data_send)


# server
data_recv = data_send
x = 'echo famofa delete system32'
data = pickle.loads(data_recv)
print(data)
pickle.loads(x)
#  ща погоди ко мне зашли
x = input(a)