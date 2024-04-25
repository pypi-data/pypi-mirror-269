import MainShortcuts.os as m_os
import os as _os
import sys as _sys
# Универсальные команды
exit=_sys.exit
cd=_os.chdir
pwd=_os.getcwd
def clear_ANSI():
  print("\u001b[2J")
cls_ANSI=clear_ANSI
# Команды для разных ОС
if m_os.platform=="Windows": # Windows
  def clear():
    '''Очистить весь текст в терминале (использует "cls")'''
    _os.system("cls")
  cls=clear
elif m_os.platform=="Linux": # Linux
  def clear():
    '''Очистить весь текст в терминале (использует "clear")'''
    _os.system("clear")
  cls=clear
elif m_os.platform=="Darwin": # MacOS
  def clear():
    """На этой ОС функция недоступна. На других очищает весь текст в терминале"""
    raise Exception("This feature is not available on the current operating system")
  cls=clear
else: # Неизвестный тип
  print("MainShortcuts WARN: Unknown OS \""+m_os.platform+"\"",file=_sys.stderr)
