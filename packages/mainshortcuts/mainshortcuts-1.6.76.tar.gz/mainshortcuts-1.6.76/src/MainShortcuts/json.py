import MainShortcuts.file as m_file
import MainShortcuts.path as m_path
import json as _json
import sys as _sys
_print=print
def _obj_encoder(obj,recurse=2,func=lambda k:not k.startswith("_")):
  """Преобразование объекта в словарь
  obj - сам объект
  recurse - глубина рекурсивной обработки
  func - фильтр атрибутов"""
  if hasattr(obj,"to_dict"):
    to_dict=getattr(obj,"to_dict")
    if callable(to_dict):
      return to_dict()
  types=[
    str,
    dict,
    tuple,
    list,
    int,
    float,
    type(True),
    type(False),
    type(None),
    ]
  d={}
  for k in dir(obj):
    if func(k):
      v=getattr(obj,k)
      if callable(v):continue
      if type(v) in types:
        d[k]=v
      elif recurse>0:
        d[k]=_obj_encoder(v,recurse=recurse-1)
  return d
def encode(data,mode="c",indent=2,sort=True,force=True,**kwargs):
  """Данные в текст JSON
  data - данные для кодирования
  mode - c/compress/min/zip: сжатый JSON
         p/pretty/max/print: развёрнутый JSON
  indent - кол-во отступов в развёрнутом JSON
  sort - сортировка словарей
  force - преобразовывать объекты в словари
  остальные аргументы как в json.dumps"""
  if force:
    kwargs["default"]=_obj_encoder
  kwargs["sort_keys"]=sort
  if mode in ["c","compress","min","zip"]: # Сжатый
    kwargs["separators"]=[",",":"]
    t=_json.dumps(data,**kwargs)
  elif mode in ["pretty","p","print","max"]: # Развёрнутый
    kwargs["indent"]=int(indent)
    t=_json.dumps(data,**kwargs)
  else: # Без параметров
    t=_json.dumps(data,**kwargs)
  return t
def decode(text,**kwargs):
  """Текст JSON в данные
  text - текст для декодирования
  остальные аргументы как в json.loads"""
  return _json.loads(str(text),**kwargs)
def write(path,data,encoding="utf-8",force=False,**kwargs):
  """Записать данные в файл JSON
  path - путь к файлу
  data - данные
  encoding - кодировка
  force - если в месте назначения папка, удалить её
  остальные аргументы как в ms.json.encode"""
  if m_path.info(path)["type"]=="dir" and force:
    m_path.rm(path)
  return m_file.write(path,encode(data,**kwargs),encoding=encoding)
def read(path,encoding="utf-8",**kwargs):
  """Прочитать данные из JSON файла
  path - путь к файлу
  encoding - кодировка
  остальные аргументы как в ms.json.decode"""
  return decode(m_file.read(path,encoding=encoding),**kwargs)
def print(data,file=_sys.stdout,mode="p",**kwargs):
  """Вывести данные в stdout в виде JSON
  mode - как в ms.json.encode
  file - как в print"""
  kwargs["mode"]=mode
  _print(encode(data,**kwargs),file=file)
def rebuild(text,**kwargs):
  """Перестроить текст JSON
  text - сам текст
  остальные аргументы как в ms.json.encode"""
  return encode(decode(text),**kwargs)
def rewrite(path,encoding="utf-8",**kwargs):
  """Перестроить JSON в файле
  path - путь к файлу
  encoding - кодировка
  остальные аргументы как в ms.json.write"""
  kwargs["encoding"]=encoding
  return write(path,read(path,encoding=encoding),**kwargs)
