import logging  # the logging commands
import logging.handlers  # used for logging
import os

import discord
from colorlog import ColoredFormatter  # used for logging

from login import email, password


def _setup(name='PokestarBot', dir=None):
    if dir is not None:
        os.chdir(dir)
    log_format = "[%(log_color)s%(asctime)s%(reset)s] {%(log_color)s%(pathname)s:%(lineno)d%(reset)s} | " \
                 "%(log_color)s%(levelname)s%(reset)s : %(log_color)s%(message)s%(reset)s"  # idk
    file_format = "[%(asctime)s] {%(pathname)s:%(lineno)d}|%(levelname)s : %(message)s"  # same as log_format but
    # doesn't have the coloring
    formatter = ColoredFormatter(log_format)
    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)
    stream.setFormatter(formatter)
    log = logging.getLogger(name)

    log.setLevel(logging.DEBUG)
    log.addHandler(stream)

    fh = logging.FileHandler(r'%s_app.log' % name)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(fmt=file_format))
    log.addHandler(fh)

    if dir is not None:
        os.chdir("..")
    return log


if __name__ == '__main__':
    logger = _setup()
    os.chdir("App")


def multmkdir(dir, logger):
    parts = dir.split('\\')
    s = ''
    for i in parts:
        s += i + '\\'
        try:
            os.mkdir(s)
            logger.info("Folder %s created", s)
        except FileExistsError:
            pass


def chmkdir(name, lgr=None):
    try:
        if lgr is None:
            lgr = logger
        multmkdir(name, lgr)
    except FileExistsError:
        pass


if __name__ == '__main__':
    chmkdir("Servers")
    chmkdir("Authors")


def check_if_exists(filename, heading, text):
    try:
        with open(filename, 'x', encoding='utf-8') as file:
            heading = heading if heading[-1] == '\n' else heading + '\n'
            file.write(heading)
            logger.info("File %s created with heading %s", filename, heading.replace("\n", ""))
    except FileExistsError:
        pass
    finally:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(text)
            # logger.info("%s had %s written to it",filename,text)


client = discord.Client()


def return_csv_form(*args):
    s = ""
    for i in args:
        s += str(i).replace(",", "_").replace('\n', "NL") + ','
    s = s[:-1]
    s += '\n'
    return s


def format_msg(m):
    id = m.id
    server = m.server.name
    channel = m.channel.name
    author = m.author.name
    content = m.content
    content_length = len(content)
    server_dir = "Servers\\%s" % server
    server_dir = server_dir.replace("/", "_").replace(",", "_").replace(":", "_")
    server_all = server_dir + '\\all.csv'
    channel_dir = server_dir + '\\%s.csv' % channel
    author_dir = "Authors\\%s" % author
    author_dir = author_dir.replace("/", "_").replace(".", "_").replace("|", "_")
    author_all = author_dir + '\\all.csv'
    author_server_dir = author_dir + '\\' + server_dir
    author_server_all = author_server_dir + '\\all.csv'
    author_server_channel = author_dir + '\\' + channel_dir
    with open("all_all.csv", "a", encoding='utf-8') as a:
        a.write(return_csv_form(id, author, server, channel, content_length, content))
    chmkdir(server_dir)
    check_if_exists(server_all, "ID,Author,Channel,Content Length,Content",
                    return_csv_form(id, author, channel, content_length, content))
    check_if_exists(channel_dir, "ID,Author,Content Length,Content",
                    return_csv_form(id, author, content_length, content))
    chmkdir(author_dir)
    check_if_exists(author_all, "ID,Server,Channel,Content Length,Content",
                    return_csv_form(id, server, channel, content_length, content))
    chmkdir(author_server_dir)
    check_if_exists(author_server_all, "ID,Channel,Content Length,Content",
                    return_csv_form(id, channel, content_length, content))
    check_if_exists(author_server_channel, "ID,Content Length,Content", return_csv_form(id, content_length, content))


@client.event
async def on_ready():
    print("Ready!")


@client.event
async def on_message(message):
    try:
        format_msg(message)
    except Exception:
        logger.exception("Message with id %s could not formatted", message.id)


if __name__ == '__main__':
    client.run(email, password)
