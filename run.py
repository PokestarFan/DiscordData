from os import system as run
from datetime import datetime

entries = ['git add App',
           'git commit -m "Added files through python program at %s"' % datetime.now(),
           'git push', ]

while True:
#if True:
    for i in entries:
        run('cmd.exe /C' + i)
