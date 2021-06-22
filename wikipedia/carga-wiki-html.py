
import os
import sys
import time
import requests
import datetime
import argparse
from tabulate import tabulate
from collections import OrderedDict

# If you get ModuleNotFoundError: No module named 'requests', 
# try install the module: 
# python -m pip install requests

def read_args ():
  parser = argparse.ArgumentParser ()
  parser.add_argument ('title', nargs='*')
  parser.add_argument ("-l", "--list")
  parser.add_argument ("-s", "--sleep", type=int, default=5)
  parser.add_argument ("-t", "--topicos", default="topicos-html.csv")
  parser.add_argument("--newer", action="store_true",help=
    "Carga plus nove anque si le plus vetere file jam existe.")
  parser.add_argument("--index", action="store_true")
  parser.add_argument("--showtext", action="store_true")
  parser.add_argument("--paramlist", action="store_true")
  args = parser.parse_args ()
  return (args)

dir1 = "html"
replace_x = [
  (" ","_"),
  ("/","_"),
  ("\\","_"),
  (".","_"),
  ("~","_"),
  (":","_"),
]

def canonical (args_title):
  title, full_pg = "",""
  # print (type (args_title))
  if type (args_title) is list:
    title = " ".join (args_title)
  if type (args_title) is str:
    title = args_title
  pg_file = title
  for a,b in replace_x:
    pg_file = pg_file.replace (a,b)
  full_pg = dir1 + "/" + pg_file + ".html"
  return title, full_pg

def carga (title,full_pg):
  # print (title)
  # print (pg_file)
  table = []
  response = requests.get(
      'https://ia.wikipedia.org/w/api.php',
      params={
          'action': 'query',
          'redirects': True,
          'format': 'json',
          'titles': title,
          'prop': 'extracts',
          #'explaintext': True,
      }).json()
  page = next (iter(response['query']['pages'].values()))
  try:
    redirect = next (iter(response['query']['redirects']))
    redir = redirect['to']
    print ("redirect to",redir)
    title,full_pg = canonical ([redir])
  except (KeyError):
    pass
  existe = True
  try:
    extract = page['extract']
  except KeyError:
    print (f'Le pagina "{title}" non existe in Wikipedia.')
    existe = False
  if existe:
    f = open (full_pg,"w")
    f.write (extract)
    if args.showtext:
      print (extract)
    print ("Scribeva",full_pg)
    ln = len (extract)
    now = datetime.datetime.now()
    tm = now.strftime('%Y-%m-%d %H:%M:%S')
    new = [title,tm,str(ln)]
  
    d = {}
    try:
      f = open (args.topicos)
      for s in f.readlines ():
        item = s.strip("\n").split("\t")
        d [item[0]] = item[1:]
      f.close()
    except:
      pass
    d [new[0]] = new [1:]
    table = []
    for k,v in d.items():
      t_flat = [k] + [x for x in v]
      table.append (t_flat)
    table.sort()
    f = open (args.topicos,"w")
    for t in table:
      f.write ("\t".join (t) + "\n")
    f.close()
  return table

args = read_args()
if args.paramlist:
  for arg in vars (args):
    print (f"{arg}: {getattr (args, arg)}")

vetere_paginas = [dir1 + "/" + f for f in os.listdir (dir1)]

table = []

if args.list:
  f = open (args.list)
  for s in f.readlines ():
    sword = s.strip("\n")
    title,pg_file = canonical ([sword])
    if (not args.newer) and pg_file in vetere_paginas:
      print ("Jam existe, non cargate:", title)
    else:
      print ("Cerca", title)
      table = carga (title,pg_file)
      if args.sleep:
        print ("Sleep", args.sleep, "s")
        time.sleep (args.sleep)

if args.title:
  title,pg_file = canonical (args.title)
  table = carga (title,pg_file)

if args.index:
  print (tabulate (table))

