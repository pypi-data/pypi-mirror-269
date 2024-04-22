def hello():
    # print("Hello Alpha Protocol")
    with open('./data.txt','r') as f:
        print(f.read())