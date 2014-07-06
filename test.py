from subprocess import Popen, PIPE

cat  = Popen(['cat'], stdin=PIPE, stdout=PIPE)
grep = Popen(['grep', 'pattern'], stdin=PIPE, stdout=cat.stdin)

print(grep.communicate(b'pattern'))
grep.wait()

print(cat.communicate())
cat.wait()
