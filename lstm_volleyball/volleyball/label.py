file = open('train_serve_Y_round2.txt', 'a')
line = input("Label No: ")
num = int(int(input("How much this label will be print? "))/25)
print(num)
for i in range(num):
    file.write(line+"\n")
file.close()
