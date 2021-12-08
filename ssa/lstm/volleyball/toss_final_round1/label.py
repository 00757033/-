file = open('train_toss_Y_round2.txt', 'a')
line = input("Label No: ")
num = int(int(input("How much this label will be print? ")))
print(num)
for i in range(num):
    tmp = int(line)
    file.write(str(tmp)+"\n")
file.close()
