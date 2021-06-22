
# python sub-text.py aqua
# python sub-text.py aqua --substitue subst-md.csv

from tabulate import tabulate
from math import *
import argparse
import random
import re

def read_args ():
  parser = argparse.ArgumentParser ()
  parser.add_argument ('title', nargs='*')
  parser.add_argument ("-p", "--partes", type=int)
  parser.add_argument ("-n", "--num", type=int, default=351)
  parser.add_argument ("-s", "--substitue", default="subst-html.csv")
  parser.add_argument ("-o", "--outfile", default="libro-wiki")
  parser.add_argument ("-t", "--topicos", default="topicos-html.csv")
  parser.add_argument("--substable", action="store_true")
  parser.add_argument("--paramlist", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

if args.paramlist:
  for arg in vars (args):
    print (f"{arg}: {getattr (args, arg)}")

replace_x = [
  (" ","_"),
  ("/","_"),
  ("\\","_"),
  (".","_"),
  ("~","_"),
  (":","_"),
]

replace_y = [
  ("_"," "),
]

def canonical (args_title):
  title, full_pg = "",""
  # print (type (args_title))
  if type (args_title) is list:
    title = " ".join (args_title)
  if type (args_title) is str:
    title = args_title
  for a,b in replace_y:
    title = title.replace (a,b)
  pg_file = title
  for a,b in replace_x:
    pg_file = pg_file.replace (a,b)
  full_pg = "html/" + pg_file + ".html"
  return title, full_pg

def add_css(tof):
  text = """
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
"""
  tof.write (text)


def read_topicos():
  d = {}
  f = open (args.topicos)
  for s in f.readlines ():
    item = s.strip("\n").split("\t")
    d [item[0]] = item[1:]
  f.close()
  return d

def imprime (title0,subs,tof): 
  # title = " ".join (args.title)
  # pg_file = "_".join (args.title) + ".txt"
  title, pg_file = canonical (title0)
  title = title[0].upper() + title[1:]
  # print (pg_file)
  f = open (pg_file)
  text = f.read ()
  # text = "<h1> &#11035; " + title + "</h1>\n\n" + text
  text = "<h1 class=\"c\"> <img src=\"w.png\" class=\"c\"> " + title + "</h1>\n\n" + text
  for s1,s2 in subs:
    text = re.sub (s1, s2, text, flags=re.M)

  tof.write (text + "\n\n")

def read_sublist ():
  g = open (args.substitue)
  items = []
  for s in g.readlines ():
    new = s.strip("\n").split("\t")
    if len (s) > 1 and s[0] != "#":
      if len (new) == 2:
        items.append (new)
      if len (new) == 1:
        items.append ((new[0],""))
  if args.substable:
    print (tabulate(items))
  return items

##########
def split (l,num):
  n = ceil (len(l) / num)
  return [l[i:i + n] for i in range(0, len(l), n)]

def chunks_of (l,n):
  return [l[i:i + n] for i in range(0, len(l), n)]

f = open (args.topicos)
lines = f.readlines ()
f.close()

random.shuffle (lines)
subs = read_sublist ()
if args.partes:
  partition = split (lines,args.num)
else:
  partition = chunks_of (lines,args.num)

total_partes = len (partition)
zeros = len (str(total_partes))
for pt,part in enumerate (partition):
  print (f"\nParte {pt+1}\n")
  f = open (args.outfile + "-" + str(pt+1).zfill(zeros) + ".html","w")
  add_css (f)
  for i,s in enumerate (part):
    item = s.strip("\n").split("\t")
    print (f"{i+1}/{len(part)} {item[0]}")
    imprime (item[0],subs,f)
       

