file = open('test_toss_X_round8.txt', 'a')
filepath='test_toss_X_round4.txt'
cnt = 0
with open(filepath) as fp:
  lines = fp.readlines()
  cnt+=1
  print(cnt)
  for line in lines:
    cnt+=1
    print(line)
    tmp=[]
    s1=line.split("\n")
    s3 = s1[0].split(",")
    tmp.clear()
    for i in s3:
        tmp.append((float(i)+500)/2000)
    tmp2 = str(tmp)
    ss1 = tmp2.split("[")
    ss2=ss1[1].split("]")
    file.write(str(ss2[0])+"\n")
    tmp.clear()

file.close()
