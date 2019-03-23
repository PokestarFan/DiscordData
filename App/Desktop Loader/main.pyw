from cb import main
from easygui import exceptionbox


if __name__ == '__main__':
    try:
        main()
    except KeyError:
        exit()
    except Exception:
        exceptionbox(msg = 'There has been an exception, please check exception.', title = 'Exception')
        input('Press enter to exit.')
else:
    print('Name is not main')
