# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:  Nikoloz Aneli
# Collaborators:
# Time: -:-

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import collections


# -----------------------------------------------------------------------

# ======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
# ======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
        #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
        #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret


# ======================
# Data structure design
# ======================

# Problem 1


class NewsStory:
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


# ======================
# Triggers
# ======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError


# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        """
        Args:
            text: text may include some characters in string.punctuation
            phrase: words with only 1 space between
        Returns: True or False
        """

        text = [' ' if c in string.punctuation else c for c in text.lower()]
        text_words = [word for word in ''.join(text).split(' ') if len(word)]

        phrase_words = self.phrase.split()  # list of words


        if len(phrase_words) == 1:
            return self.phrase in text_words
        else:
            try:
                for word in phrase_words:
                    if word in text_words and word != text_words[-1]:
                        if text_words[text_words.index(word) + 1] == phrase_words[1]:
                            return True
            except ValueError:
                return False
# Problem 3

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        title = story.get_title()
        return self.is_phrase_in(title)


# Problem 4

class DescriptionTrigger(PhraseTrigger):
    def __init__(self,phrase):
        PhraseTrigger.__init__(self, phrase)
    def evaluate(self, story):
        description = story.get_description()
        return self.is_phrase_in(description)

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, time ):  #"3 Oct 2016 17:00:10
        date = datetime.strptime(time, '%d %b %Y %H:%M:%S')
        self.time = date.replace(tzinfo=pytz.timezone("EST"))
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6

class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self,time)

    def evaluate(self, story):
        if story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) < self.time:
            return True
        return False

class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self,time)

    def evaluate(self, story):
        if story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) > self.time:
            return True
        return False

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self,trigger):
        self.trigger = trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        r1 = self.trigger1.evaluate(story)
        r2 = self.trigger2.evaluate(story)
        return r1 and r2

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        r1 = self.trigger1.evaluate(story)
        r2 = self.trigger2.evaluate(story)
        return r1 or r2



# ======================
# Filtering
# ======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    result = []
    for story in stories:
        match = False
        for trigger in triggerlist:
            if trigger.evaluate(story):
                match = True
        if match:
            result.append(story)
    return result

# ======================
# User-Specified Triggers
# ======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    triggers = {}
    response = []
    for line in trigger_file:
        line = line.rstrip()
        # ignore comments and whitespace
        if len(line) == 0 or line.startswith('//'):
            continue
        args = line.split(',')
        [trigger_name, trigger_type] = args[:2]
        # make trigger objects and populate dict accordingly
        if trigger_name == 'ADD':  # finish making triggers
            response = [triggers.get(n) for n in args[1:] if triggers.get(n)]
            break
        if trigger_type == 'TITLE':
            triggers[trigger_name] = TitleTrigger(args[2])
        if trigger_type == 'DESCRIPTION':
            triggers[trigger_name] = DescriptionTrigger(args[2])
        if trigger_type == 'AFTER':
            triggers[trigger_name] = AfterTrigger(args[2])
        if trigger_type == 'BEFORE':
            triggers[trigger_name] = BeforeTrigger(args[2])
        if trigger_type == 'NOT':
            obj = triggers.get(args[2], None)
            if obj is None:  # ignore invalid triggers
                continue
            triggers[trigger_name] = NotTrigger(obj)
        if trigger_type == 'AND':
            obj1 = triggers.get(args[2], None)
            obj2 = triggers.get(args[3], None)
            if obj1 is None or obj2 is None:  # ignore invalid triggers
                continue
            triggers[trigger_name] = AndTrigger(obj1, obj2)
        if trigger_type == 'OR':
            obj1 = triggers.get(args[2], None)
            obj2 = triggers.get(args[3], None)
            if obj1 is None or obj2 is None:  # ignore invalid triggers
                continue
            triggers[trigger_name] = OrTrigger(obj1, obj2)
    return response


SLEEPTIME = 120  # seconds -- how often we poll


def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11

        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica", 14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []

        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title() + "\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()
