import MainShortcuts.path as m_path
import os as _os
import shutil as _shutil
_open=open
def read(path,encoding="utf-8"):
  """Прочитать файл как текст
  encoding - кодировка
  Если файла нет, возвращает пустую строку"""
  if _os.path.isfile(path):
    with _open(path,"rb") as f:
      text=f.read().decode(encoding)
  else:
    text=""
  return text
def write(path,text="",encoding="utf-8",force=False):
  """Записать текст в файл
  text - текст для записи
  encoding - кодировка
  force - принудительно создать файл"""
  if _os.path.isdir(path) and force:
    m_path.rm(path)
  with _open(path,"wb") as f:
    f.write(str(text).encode(encoding))
  return True
def open(path):
  """Прочитать файл как байты
  Если файла нет, возвращает пустые байты"""
  if _os.path.isfile(path):
    with _open(path,"rb") as f:
      content=f.read()
  else:
    content=b""
  return content
load=open
def save(path,content=b"",force=False):
  """Записать байты в файл
  content - байты для записи
  force - принудительно создать файл"""
  if _os.path.isdir(path) and force:
    m_path.rm(path)
  with _open(path,"wb") as f:
    f.write(content)
  return True
def delete(path):
  """Удалить файл
  Если он не существует, ничего не изменится
  Если на месте папка, выдаст ошибку"""
  type=m_path.info(path)["type"]
  if type=="file":
    m_path.rm(path)
  elif not _os.path.exists(path):
    pass
  else:
    raise Exception("Unknown type: "+type)
def copy(fr,to,force=False):
  """Копировать файл
  force - если в месте назначения папка, удалить её"""
  type=m_path.info(fr)["type"]
  if type=="file":
    if m_path.exists(to) and force:
      m_path.delete(to)
    _shutil.copy(fr,to)
  else:
    raise Exception("Unknown type: "+type)
def move(fr,to,force=False):
  """Переместить файл
  force - если в месте назначения папка, удалить её"""
  type=m_path.info(fr)["type"]
  if type=="file":
    if m_path.exists(to) and force:
      m_path.delete(to)
    _shutil.move(fr,to)
  else:
    raise Exception("Unknown type: "+type)
def rename(fr,to,force=False):
  """Переименовать файл
  force - если в месте назначения папка, удалить её"""
  type=m_path.info(fr)["type"]
  if type=="file":
    if m_path.exists(to) and force:
      m_path.delete(to)
    _os.rename(fr,to)
  else:
    raise Exception("Unknown type: "+type)
