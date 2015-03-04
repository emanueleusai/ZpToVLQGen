#!/usr/bin/env python

# How-to:
# * copy this script to the MadGraph main directory
# * set directory to the existing (!) directory where the process was set up.
# Then, use the scanpoints to specify which masses to scan as dictionary
# pdgid -> mass in GeV. This script will then run MadGraph for all possible mass
# combinations.

#directory = "/space/ottjoc/code/madgraph5/TTTest"
directory = "/space/ottjoc/code/madgraph5/TTalldec"
#directory = "/space/ottjoc/code/madgraph5/gluino-pair"
scanpoints = {1000006: [600, 700, 800, 900, 1000, 1100], 1000022: [300, 350]}

import sys, os, os.path, shutil

sys.path.append(os.path.join(directory,'bin','internal'))
import madevent_interface as ME

# setup logging:
import logging, logging.config, coloring_logging
logging.config.fileConfig(os.path.join(directory, 'bin', 'internal', 'me5_logging.conf'))
logging.root.setLevel(logging.ERROR)
logging.getLogger('madevent').setLevel(logging.ERROR)
logging.getLogger('madgraph').setLevel(logging.ERROR)

# d is a dict   pdgid (int) -> mass value (float)
def set_masses(d):
   # convert d to int -> float:
   dtmp = {}
   for pdgid in d:
       dtmp[int(pdgid)] = float(d[pdgid])
   d = dtmp
   tmpfile = open(directory + "/Cards/param_card.dat.tmp", 'w')
   replaced_pdgids = set()
   massblock = False
   for l in file(directory + "/Cards/param_card.dat"):
      if 'BLOCK' in l:
          massblock = 'BLOCK MASS' in l
          tmpfile.write(l)
          continue
      if massblock:
          if l.strip().startswith('#'):
              tmpfile.write(l)
              continue
          pdg, mass = l.split(None, 1)
          pdg = int(pdg)
          if pdg in d:
              tmpfile.write('   %d %.3g\n' % (pdg, d[pdg]))
              replaced_pdgids.add(pdg)
          else:
              tmpfile.write(l)
      else:
           tmpfile.write(l)
   tmpfile.close()
   d_pdgids = set(d.keys())
   if d_pdgids != replaced_pdgids:
       raise RuntimeError, "replace not successfull: requested to replace %s, but could only replace %s" % (str(d_pdgids), str(replaced_pdgids))
   os.rename(directory + "/Cards/param_card.dat.tmp", directory + "/Cards/param_card.dat")

def generate_lhe():
   launch = ME.MadEventCmd(me_dir=directory)
   launch.run_cmd('generate_events -f')
   launch.run_cmd('quit')


# rename the run_01/unweighted_events to the naming scheme and delete the Events/run_01 directory.
# newname is the name without extension "lhe.gz"
def process_results(newname):
   os.rename(os.path.join(directory, 'Events', 'run_01', 'unweighted_events.lhe.gz'), os.path.join(directory, 'Events', newname + '.lhe.gz'))
   shutil.rmtree(os.path.join(directory, 'Events', 'run_01'))

def get_name(d):
   result = 'events'
   for pdgid in sorted(list(d.keys())):
      result += '_%d' % int(d[pdgid])
   return result


# givan a map pdgid -> list of mass points, returns a list of
# dictonaries, where each dict corresponds to one mass point.
# example:
# single_dicts({1: [3,4,5], 2: [100, 101]})
# yields a dictionary with 6 entries corresponding to all possible
# mass combinations:
# [{1: 3, 2: 100}, {1: 3, 2: 101}, {1: 4, 2: 100}, {1: 4, 2: 101}, {1: 5, 2: 100}, {1: 5, 2: 101}]
def single_dicts(scanpoints):
   pdgids = sorted(list(scanpoints.keys()))
   def generate(i_id, d):
      id = pdgids[i_id]
      points = scanpoints[id]
      for p in points:
         d = dict(d)
         d[id] = p
         if i_id + 1 == len(pdgids): yield d
         else:
            for d2 in generate(i_id + 1, d): yield d2
      raise StopIteration
   return [x for x in generate(0, {})]

for d in single_dicts(scanpoints):
   print "Starting %s" % str(d)
   set_masses(d)
   generate_lhe()
   process_results(get_name(d))

