
msg = ""
for i in range(50):
    msg= msg+"flag"+str(i)+"=(\S*) "
print(msg+" #(\S*)")