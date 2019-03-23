from atexit import register

from tqdm import tqdm

from msgs import _setup


class Analysis(object):
    def __init__(self, file):
        self.ids, self.authors, self.servers, self.channels, self.content_length, self.content = [], [], [], [], [], []
        self.logger = _setup("Analysis_%s" % file.split('App\\')[-1].replace("\\", "_"))
        # The methods debug, info, warning, error, critical, and exception are assigned to the class instead of
        # having to be called through self.logger.x
        self.exc = self.logger.exception # most used
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.f = open(file, 'r', encoding="utf-8")

        @register
        def close_file():
            """
            This function is registered to an atexit function.

            :return:
            """
            self.f.close()

        self.header = self.f.readline(1)
        self.parts = self.header.split(",")
        self._parts = self.parts
        self.parts.remove("ID")
        if "Author" in self.parts:
            self.author_all()

    def author_append_lists(self, row):
        try:
            a, b, c, d, e = row.split(",")
            self.ids.append(a)
            self.servers.append(b)
            self.channels.append(c)
            self.content_length.append(int(d))
            self.content.append(e)
        except ValueError:
            self.logger.exception("Value %s is not a valid integer", d)
        except Exception:
            self.logger.exception()

    def author_all(self):
        if self.header == "ID,Server,Channel,Content Length,Content":
            for i in tqdm(self.f.readlines()):
                self.author_append_lists(i)

    def average_content_length(self):
        return round(sum(self.content_length) / len(self.content_length), 0)
