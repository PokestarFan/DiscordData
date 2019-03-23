from easygui import choicebox as cb
from easygui import multchoicebox as mcb
from easygui import textbox as tb
from easygui import msgbox as mb
from options import *
from urllib.parse import quote
from psutil import process_iter
import subprocess
# InvalidOptionException gen
from exceptiongen import exception_generator

InvalidOptionException = exception_generator('InvalidOptionException',
                                             message='The option provided below is invalid.')


# Github
def cb11():
    d = tb(msg="Enter the github username you want to visit.", title="Github username")
    return '/' + d


def cb10():
    d = tb(
        msg="Enter in repo in 1/2 line format. \n1 line format is when you type in the full directory, in [user]/[reponame]" \
            "\n2 line format is when you type in the username in one line, then the reponame in the other.",
        title='Repository Name')
    if '\n' in d:
        parts = d.split('\n')
        return '/' + parts[0] + '/' + parts[1]
    else:
        return '/' + d


def cb9():
    d = cb(msg='Choose the Github repo.',
           title='Repo',
           choices=[
               'Probability',
               'RedditMemes',
               'Custom'
           ])
    if d == 'Custom':
        return cb10()
    else:
        return cb9_d[d]


def cb8():
    d = cb(msg="What Github username would you like to visit?",
           title='Github username',
           choices=[
               'PokestarFan',
               'PokeTec',
               'iTecAi',
               'Custom'
           ])
    if d == 'Custom':
        return cb11()
    else:
        return cb8_d[d]


def cb6():
    d = cb(msg='What to do/view on github?',
           title='Github',
           choices=[
               'Users',
               'Repos',
               'Create Repo'
           ])
    if d == 'Create Repo':
        return '/new'
    elif d == 'Users':
        return cb8()
    elif d == 'Repos':
        return cb9()
    else:
        raise InvalidOptionException(d)


# Reddit
def cb5():
    db5 = [i for i in cb5_d]
    db5.extend(['Custom', 'Front Page'])
    d = cb(msg='Which subreddit do you want to visit?',
           title='Subreddits',
           choices=db5)
    if d == 'Custom':
        return '/r/' + cb12()
    elif d == 'Front Page':
        return ''
    else:
        return '/r/' + cb5_d[d]


def cb14():
    d = tb(msg='Input username of Redditor to visit', title='Reddit Username', text="PokestarFan")
    return '/u/' + d


def cb13():
    d = cb(msg='What option would you like to do on Reddit?',
           title='Reddit',
           choices=[
               'Users',
               'Subreddits'
           ])
    if d == 'Users':
        return cb14()
    elif d == 'Subreddits':
        return cb5()
    else:
        raise InvalidOptionException(d)


def cb12():
    d = tb(msg='Input subreddit username', title='Subreddit Name')
    return d


# chrome ops
def cb4():
    d = tb(msg='Google search query', title='Google Search')
    return quote(d)


def cb3():
    d = tb(msg='What website would you like to visit?', title='Custom Website')
    return d


def cb2():
    d = cb(msg='What user profile do you want to use?',
           title='User profile',
           choices=[
               'Personal',
               'School'
           ])
    if d == 'Personal':
        path = '--profile-directory=\"Profile 1\" '
    elif d == 'School':
        path = '--profile-directory="Profile 11" '
    else:
        raise InvalidOptionException(d)
    db_2 = [i for i in cb2_d[d]]
    db_2.extend([
        'Google',
        'Custom',
        'None'
    ])
    d2 = cb(msg='What website do you want to visit?',
            title='Website to visit',
            choices=db_2)
    if d2 == 'Google':
        return path + '-- ' + 'https://www.google.com/search?q=' + cb4()
    elif d2 == 'Custom':
        return path + '-- ' + cb3()
    elif d2 == 'None':
        return path
    elif d2 == 'Reddit':
        return path + '-- https://www.reddit.com' + cb13()
    elif d2 == 'Github':
        return path + '-- https://www.github.com' + cb6()
    else:
        return path + '-- ' + cb2_d[d][d2]


def working(option, dir, args=''):
    if len(args) == 0:
        d = mb(msg=f"Launching {option} at {dir}", title="Working")
    elif len(args) > 0:
        d = mb(msg=f"Launching {option} at {dir} with args {args}", title="Working")


def exiting():
    d = mb(msg='Exiting... Have a nice day.', title='Exiting')
    exit()


def taskkill():
    pc_l = [x for x in process_iter()]
    pc_ln = [x.name() for x in pc_l]
    pc_l_n = list(set([x.name() for x in pc_l]))
    pc_l_n.sort()
    d = mcb(msg='What process(es) would you like to taskkill?',
            title='Taskkill',
            choices=pc_l_n)
    do = [subprocess.run('taskkill /F /T /IM {x}'.format(x=str(x))) for x in d] if type(d) == list else subprocess.run(
        'taskkill /F /IM f{d}')


def main():
    cb1 = [i for i in main_d]
    cb1.extend(['Google Chrome', 'Taskkill', 'Shutdown', 'Copy Heading', 'None'])
    d = cb(msg='What would you like to do?',
           title='Main operation',
           choices=cb1)
    if d == 'Google Chrome':
        ar = cb2()
        working(d, r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"', args=ar)
        subprocess.run('"C:\PROGRA~2\Google\Chrome\Application\chrome.exe" ' + ar)
    elif d == 'None':
        exiting()
    elif d == 'Taskkill':
        taskkill()
    elif d == 'Shutdown':
        subprocess.run('shutdown /S /F /T 0 /hybrid')
    elif d == 'Copy Heading':
        import pyperclip, datetime
        date = datetime.datetime.now().strftime('%m/%d/%y')
        pyperclip.copy("""Aoyan Sarkar										         {}""".format(str(date)))
        main()
    else:
        working(d, main_d[d])
        subprocess.run(main_d[d])
