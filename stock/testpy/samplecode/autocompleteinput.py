import os
import sys 
import readline
import glob

class tabCompleter(object):
    """ 
    A tab completer that can either complete from
    the filesystem or from a list.
    
    Partially taken from:
    http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
    """

    def pathCompleter(self,text,state):
        """ 
        This is the tab completer for systems paths.
        Only tested on *nix systems
        """
        line   = readline.get_line_buffer().split()

        return [x for x in glob.glob(text+'*')][state]

    
    def createListCompleter(self,ll):
        """ 
        This is a closure that creates a method that autocompletes from
        the given list.
        
        Since the autocomplete function can't be given a list to complete from
        a closure is used to create the listCompleter function with a list to complete
        from.
        """
        def listCompleter(text,state):
            line   = readline.get_line_buffer()

            if not line:
                return [c + " " for c in ll][state]

            else:
                return [c + " " for c in ll if c.startswith(line)][state]
    
        self.listCompleter = listCompleter

if __name__=="__main__":
    t = tabCompleter()
    t.createListCompleter(["ab","aa","bcd","bdf"])

    readline.set_completer_delims('\t')
    readline.parse_and_bind("tab: complete")

    readline.set_completer(t.listCompleter)

    ans = raw_input("Complete from list ")
    print ans
    
    readline.set_completer(t.pathCompleter)
    ans = raw_input("What file do you want? ")
    print ans
    
# readline.set_completer(completer.complete)
# readline.parse_and_bind('tab:complete')


# def interact(mydict=None,argv=None,mybanner=None,loglevel=1):
#     import code,sys,cPickle,types,os,imp,getopt,logging

#     logging.getLogger("scapy").setLevel(loglevel)

#     the_banner = "Welcome to Scapy (%s)"
#     if mybanner is not None:
#         the_banner += "\n"
#         the_banner += mybanner

#     if argv is None:
#         argv = sys.argv

# #    scapy_module = argv[0][argv[0].rfind("/")+1:]
# #    if not scapy_module:
# #        scapy_module = "scapy"
# #    else:
# #        if scapy_module.endswith(".py"):
# #            scapy_module = scapy_module[:-3]
# #
# #    scapy=imp.load_module("scapy",*imp.find_module(scapy_module))


#     import __builtin__
# #    __builtin__.__dict__.update(scapy.__dict__)
#     __builtin__.__dict__.update(globals())
#     if mydict is not None:
#         __builtin__.__dict__.update(mydict)


#     import re, atexit
#     try:
#         import rlcompleter,readline
#     except ImportError:
#         log_loading.info("Can't load Python libreadline or completer")
#         READLINE=0
#     else:
#         READLINE=1
#         class ScapyCompleter(rlcompleter.Completer):
#             def global_matches(self, text):
#                 matches = []
#                 n = len(text)
#                 for lst in [dir(__builtin__), session.keys()]:
#                     for word in lst:
#                         if word[:n] == text and word != "__builtins__":
#                             matches.append(word)
#                 return matches


#             def attr_matches(self, text):
#                 m = re.match(r"(\w+(\.\w+)*)\.(\w*)", text)
#                 if not m:
#                     return
#                 expr, attr = m.group(1, 3)
#                 try:
#                     object = eval(expr)
#                 except:
#                     object = eval(expr, session)
#                 if isinstance(object, Packet) or isinstance(object, Packet_metaclass):
#                     words = filter(lambda x: x[0]!="_",dir(object))
#                     words += [x.name for x in object.fields_desc]
#                 else:
#                     words = dir(object)
#                     if hasattr( object,"__class__" ):
#                         words = words + rlcompleter.get_class_members(object.__class__)
#                 matches = []
#                 n = len(attr)
#                 for word in words:
#                     if word[:n] == attr and word != "__builtins__":
#                         matches.append("%s.%s" % (expr, word))
#                 return matches

#         readline.set_completer(ScapyCompleter().complete)
#         readline.parse_and_bind("C-o: operate-and-get-next")
#         readline.parse_and_bind("tab: complete")


#     session=None
#     session_name=""
#     CONFIG_FILE = DEFAULT_CONFIG_FILE

#     iface = None
#     try:
#         opts=getopt.getopt(argv[1:], "hs:Cc:")
#         for opt, parm in opts[0]:
#             if opt == "-h":
#                 usage()
#             elif opt == "-s":
#                 session_name = parm
#             elif opt == "-c":
#                 CONFIG_FILE = parm
#             elif opt == "-C":
#                 CONFIG_FILE = None

#         if len(opts[1]) > 0:
#             raise getopt.GetoptError("Too many parameters : [%s]" % string.join(opts[1]),None)


#     except getopt.GetoptError, msg:
#         log_loading.error(msg)
#         sys.exit(1)


#     if CONFIG_FILE:
#         read_config_file(CONFIG_FILE)

#     if session_name:
#         try:
#             os.stat(session_name)
#         except OSError:
#             log_loading.info("New session [%s]" % session_name)
#         else:
#             try:
#                 try:
#                     session = cPickle.load(gzip.open(session_name,"rb"))
#                 except IOError:
#                     session = cPickle.load(open(session_name,"rb"))
#                 log_loading.info("Using session [%s]" % session_name)
#             except EOFError:
#                 log_loading.error("Error opening session [%s]" % session_name)
#             except AttributeError:
#                 log_loading.error("Error opening session [%s]. Attribute missing" %  session_name)

#         if session:
#             if "conf" in session:
#                 conf.configure(session["conf"])
#                 session["conf"] = conf
#         else:
#             conf.session = session_name
#             session={"conf":conf}

#     else:
#         session={"conf": conf}

#     __builtin__.__dict__["scapy_session"] = session


#     if READLINE:
#         if conf.histfile:
#             try:
#                 readline.read_history_file(conf.histfile)
#             except IOError:
#                 pass
#         atexit.register(scapy_write_history_file,readline)

#     sys.ps1 = ColorPrompt()
#     code.interact(banner = the_banner % (VERSION), local=session)

#     if conf.session:
#         save_session(conf.session, session)

#     sys.exit()
# interact(mydict=None, argv=None, mybanner=None, loglevel=1)

class MyCompleter(object):  # Custom completer

    def __init__(self, options):
        self.options = sorted(options)

    def complete(self, text, state):
        if state == 0:  # on first trigger, build possible matches
            if text:  # cache matches (entries that start with entered text)
                # self.matches = [s for s in self.options 
                #                     if s and s.startswith(text)]
                self.matches = [s for s in self.options 
                                   if text in s]                                    
            else:  # no text entered, all matches possible
                self.matches = self.options[:]

        # return match indexed by state
        try: 
            return self.matches[state]
        except IndexError:
            return None

# completer = MyCompleter(["hello", "hi", "how are you", "goodbye", "great"])
# readline.set_completer(completer.complete)
# readline.parse_and_bind('tab: complete')
# 
# import rlcompleter
# import tushare as ts
# import pandas as pd
# readline.parse_and_bind('tab:complete')

# input = raw_input("Input: ")
# print "You entered", input