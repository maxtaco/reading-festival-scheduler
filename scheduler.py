
import sys
import json

##=======================================================================
##=======================================================================

class Date : 

    def __init__ (self, key, val):
        self._key = int (key)
        self._val = val
    def key (self):
        return self._key

##=======================================================================

class Person : 

    def __init__ (self, key, val, schedule):
        self._key = key
        self._name = val['name']
        self._dates = []
        self._dates = ( schedule._dates[d] for d in val['dates'] )

##=======================================================================

class Director (Person): 

    def __init__ (self, key, val, schedule):
        Person.__init__ (self, key, val, schedule)

##=======================================================================

class Writer (Person): 

    def __init__ (self, key, val, schedule):
        Person.__init__ (self, key, val, schedule)
        self._directors = ( schedule._director[d] for d in val['directors'])

##=======================================================================

class Schedule: 

    def __init__ (self):
        self._dates = {}
        self._writers = {}
        self._directors = {}

    def load_from_json (self, js):
        for k,v in js['dates'].items():
            self._dates[k] = Date (k, v)
        for k,v in js['directors'].items():
            self._directors[k] = Director (k, v, self)
        for k,v in js['writers'].items():
            self._writers[k] = Writer (k, v, self)

    def schedule (self) : 
        pass

    def output (self):
        pass


##=======================================================================

def main (argv):
    try:
        inf = argv[1]
        inh = open (inf, "r")
        line = inh.readlines()
        raw = ''.join (line)
        dat = json.loads (raw)

        schedule = Schedule ()
        schedule.load_from_json (dat)
        schedule.schedule()
        schedule.output()

    except IndexError, e:
        print "usage: %s <input-file>" % argv[0]
    except IOError, e:
        print "Cannot open input file %s: %s" % (inf, e)
    except ValueError, e:
        print "Could not decode json: %s" % e

##=======================================================================

main (sys.argv)
