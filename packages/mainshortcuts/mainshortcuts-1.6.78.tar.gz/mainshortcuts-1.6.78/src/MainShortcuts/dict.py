def path(v,path,sep="/"):
  """Пока в разработке, лучше не использовать"""
  for k in path.split(sep):
    if isinstance(v,dict):
      v=v[k]
    else:
      v=v[int(k)]
  return v
def swap(i):
  """Вывернуть словарь
  То есть поставить ключи в значения, а значения в ключи"""
  r={}
  for k,v in i.items():
    r[v]=k
  return r
def sort(d,*args,**kwargs):
  """Сортировать словарь по ключам
  Принимает те же аргументы, что и list.sort"""
  keys=list(d.keys)
  keys.sort(*args,**kwargs)
  r={}
  for k in keys:
    r[k]=d[k]
  return r
def reverse(d):
  """Развернуть словарь
  Начало будет в конце, конец в начале"""
  keys=list(d.keys())[::-1]
  r={}
  for k in keys:
    r[k]=d[k]
  return r
