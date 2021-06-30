import datetime
import sys
time=datetime.datetime.now()
output="Hi %s welcome to Hackanons & time is %s" % (sys.argv[1],time)
print(output)