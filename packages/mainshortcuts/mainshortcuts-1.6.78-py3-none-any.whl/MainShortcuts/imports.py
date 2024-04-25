"""Этот файл просто импортирует части модуля
Он создаётся автоматически"""
import MainShortcuts.main as main
imports_all=[]
imports_import_errors={}
try:
  import MainShortcuts.dict as dict
  imports_all.append('dict')
except Exception as e:
  imports_import_errors['dict']=e
try:
  import MainShortcuts.dir as dir
  imports_all.append('dir')
except Exception as e:
  imports_import_errors['dir']=e
try:
  import MainShortcuts.file as file
  imports_all.append('file')
except Exception as e:
  imports_import_errors['file']=e
try:
  import MainShortcuts.json as json
  imports_all.append('json')
except Exception as e:
  imports_import_errors['json']=e
try:
  import MainShortcuts.list as list
  imports_all.append('list')
except Exception as e:
  imports_import_errors['list']=e
try:
  import MainShortcuts.os as os
  imports_all.append('os')
except Exception as e:
  imports_import_errors['os']=e
try:
  import MainShortcuts.path as path
  imports_all.append('path')
except Exception as e:
  imports_import_errors['path']=e
try:
  import MainShortcuts.proc as proc
  imports_all.append('proc')
except Exception as e:
  imports_import_errors['proc']=e
try:
  import MainShortcuts.str as str
  imports_all.append('str')
except Exception as e:
  imports_import_errors['str']=e
try:
  from MainShortcuts.cfg import cfg
  imports_all.append('cfg')
except Exception as e:
  imports_import_errors['cfg']=e
try:
  from MainShortcuts.dictplus import dictplus
  imports_all.append('dictplus')
except Exception as e:
  imports_import_errors['dictplus']=e
try:
  from MainShortcuts.fileobj import fileobj
  imports_all.append('fileobj')
except Exception as e:
  imports_import_errors['fileobj']=e
try:
  cd=main.cd
  imports_all.append('cd')
except Exception as e:
  imports_import_errors['cd']=e
try:
  clear_ANSI=main.clear_ANSI
  imports_all.append('clear_ANSI')
except Exception as e:
  imports_import_errors['clear_ANSI']=e
try:
  cls_ANSI=main.cls_ANSI
  imports_all.append('cls_ANSI')
except Exception as e:
  imports_import_errors['cls_ANSI']=e
try:
  clear=main.clear
  imports_all.append('clear')
except Exception as e:
  imports_import_errors['clear']=e
try:
  cls=main.cls
  imports_all.append('cls')
except Exception as e:
  imports_import_errors['cls']=e
try:
  exit=main.exit
  imports_all.append('exit')
except Exception as e:
  imports_import_errors['exit']=e
try:
  pwd=main.pwd
  imports_all.append('pwd')
except Exception as e:
  imports_import_errors['pwd']=e
imports_all.sort()