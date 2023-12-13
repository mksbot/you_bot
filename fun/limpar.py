import os

def limpar(numlines=100):
  """

  :rtype: object
  """
  if os.name == "posix":
    os.system('clear')
  elif os.name in ("nt", "dos", "ce"):
    os.system('CLS')
  else:
    print('\n' * numlines)
