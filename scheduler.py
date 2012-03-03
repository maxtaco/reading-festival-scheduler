
import sys
import json

##=======================================================================
##=======================================================================

class Date : 

    def __init__ (self, key, val):
        self._key = int (key)
        self._val = val
        self._taken = 0
    def key (self):
        return self._key

##=======================================================================

class Person : 

    def __init__ (self, key, val, schedule):
        self._key = key
        self._name = val['name']
        self._date_list = ( schedule._dates[d] for d in val['dates'] )
        self._date_set = set( [ d._key for d in self._date_list ] )

##=======================================================================

class Director (Person): 

    def __init__ (self, key, val, schedule):
        Person.__init__ (self, key, val, schedule)
        self._num_gigs = 0

##=======================================================================

class Writer (Person): 

    def __init__ (self, key, val, schedule):
        Person.__init__ (self, key, val, schedule)
        l  = ( schedule._director[d] for d in val['directors'])
        self._director_list = l
        self._director_set = ( d._key for d in l )

##=======================================================================

class Schedule: 

    def __init__ (self):
        self._dates = {}
        self._writers = {}
        self._directors = {}

    def load_from_json (self, js):
        for k,v in js['dates'].items():
            self._dates[int(k)] = Date (k, v)
        for k,v in js['directors'].items():
            self._directors[int(k)] = Director (k, v, self)
        for k,v in js['writers'].items():
            self._writers[int(k)] = Writer (k, v, self)

    def schedule (self) : 
        writers = self._writers.values()
        res = self._schedule(writers[0], writers[1:])
        if not res:
            raise Exception ("no schedules worked!")

    def _schedule(self, w, rest):
        for date in w._date_list:
            for k,director in self._directors.values() :
                if not k in w._director_set and \
                    director._num_gigs < 2 and \
                    date._key in director._date_set:

                    director._num_gigs += 1
                    self._choice = [ date, director ] 
                    if self._schedule (rest[0], rest[1:]) :
                        return True
                    else:
                        director._num_gigs -= 1
                        self._choice = None
        return False

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
