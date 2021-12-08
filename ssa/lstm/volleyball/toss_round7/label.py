file = open('test_toss_Y_round6.txt', 'a')
line = input("Label No: ")
num = int(int(input("How much this label will be print? ")))
print(num)
for i in range(num):
    tmp = int(line)
    file.write(str(tmp)+"\n")
file.close()
