
import sys
import json
import datetime

##=======================================================================
##=======================================================================

class Date : 

    def __init__ (self, key, val):
        self._key = int (key)
        self._val = val
        [mon,day] = [ int (i) for i in val.split (".") ]
        year = 2012
        self._date = datetime.date (2012, mon, day)
        self._taken = False

    def name (self) : return self._val

    def key (self):
        return self._key

    def __str__ (self):
        return "Date %d: %s" % (self._key, self._val)

    def is_adjacent (self, d2):
        delta = self._date - d2._date
        return (abs(delta.days) <= 1)

##=======================================================================

class Person : 

    def __init__ (self, key, val, schedule):
        self._key = int (key)
        self._name = val['name']
        self._date_list = [ schedule._dates[d] for d in val['dates'] ]
        self._date_set = set( [ d._key for d in self._date_list ] )
    def name (self) : return self._name

##=======================================================================

class Director (Person): 

    def __init__ (self, key, val, schedule):
        Person.__init__ (self, key, val, schedule)
        self._num_gigs = 0
    def __str__ (self):
        return "Director %d: %s" % (self._key, self._name)


##=======================================================================

class Writer (Person): 

    def __init__ (self, key, val, schedule):
        Person.__init__ (self, key, val, schedule)
        l  = [ schedule._directors[d] for d in val['directors'] ]
        self._director_list = l
        self._director_set = set([ d._key for d in l ])

    def __str__ (self):
        return "Writer %d: %s" % (self._key, self._name)

    def output (self):
        print " %s --> w/ %s on %s" % \
            (self, self._choice[1].name(), self._choice[0].name ())

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
        print "+ Schedule %s @ length %d" % (w, len (rest))
        for date in w._date_list:
            print "++ Try date %s" % date
            prev = self._dates.get (date._key - 1)
            if date._taken:
                print "+++ is taken...."
            elif prev and date.is_adjacent (prev) and prev._taken :
                print "+++ is next to a taken date %s" % prev
            else :
                date._taken = True
                for director in w._director_list:
                    if director._num_gigs < 2 and \
                        date._key in director._date_set:

                        print "+++ Try director %s" % director

                        director._num_gigs += 1
                        w._choice = [ date, director ] 
                        if len (rest) == 0 or \
                            self._schedule (rest[0], rest[1:]) :
                            return True
                        else:
                            director._num_gigs -= 1
                            w._choice = None
                date._taken = False
        return False

    def output (self):
        print "Schedule ===================================="
        for w in self._writers.values():
            w.output()

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
