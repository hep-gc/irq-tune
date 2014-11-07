#!/bin/python

# irq-tune
#
# Author: Ian Gable <igable@uvic.ca>
#
# https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Performance_Tuning_Guide/s-cpu-irq.html
#
#

import subprocess
import json
import shlex

def get_mask(selectedcpu):

  cpumask =""
  for cpu in range (0, 48):
    if(cpu == selectedcpu):
      cpumask = "1" + cpumask
    else:
      cpumask = "0" + cpumask
  return cpumask

def add_commas(mask):
  split_mask = [mask[x:x+8] for x in range(0,len(mask),8)]
  comma_sep =""
  for i in range(0,len(split_mask)):
    if (i < 1):
      comma_sep = split_mask[i]
    else:
      comma_sep = comma_sep + "," + split_mask[i]
  return comma_sep
 
def total_mask(cpulist, masktype ):
  masklist = []
  formatted_mask =""
  for cpu in cpulist:
    masklist.append(get_mask(cpu))
  ormask = int(0)
  for mask in masklist:
    ormask = ormask | int(mask,2)
  if masktype == "binary":
    formatted_mask = format(ormask,'048b')
  else:
    formatted_mask = format(ormask,'016x')
  return add_commas(formatted_mask)

def write_proc(irqlist):

  for irq in irqlist:
    irqmask = total_mask(irq['cores'],"hex")
    irqnumber = irq['irq']
    procname = "/proc/irq/%s/smp_affinity" % ( irqnumber )
    procfile = open(procname,'w')
    procfile.write(irqmask)
    procfile.close()

    print "Set IRQ:%s to cores: %s" % ( irqnumber , ', '.join(str(x) for x in irq['cores']) )
    print "mask: %s procfile: %s" % (irqmask, procname)
 

def main():

  # Example irq data structure
  #irqlist = [ { 'irq': '259', 'cores': [32,21] },\
  #            { 'irq': '370', 'cores': [36]      } ]

  json_data = open("irq.json").read()
  irqdict = json.loads(json_data)

  write_proc(irqdict)
 

if __name__ == "__main__":
  main()

# Some debugging junk
#
#  bmask = total_mask(cpulist,"binary")
#  hmask1 = total_mask(cpulist,"hex")
#  hmask2 = total_mask(irqlist[0]['cores'],"hex")
#  hreal = total_mask([36],"hex")
#  print hmask2
#  print hreal


