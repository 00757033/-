file = open('train_toss_Y_round1.txt', 'a')
seq=input()
s1=seq.split("[")
s2=s1[1].split("]")
s3=s2[0].replace(", ","\n")
print(s3)
file.write(s3)
file.close()
