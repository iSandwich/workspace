import datetime

class manager:
  def __init__(self, file_path):
    self.path = file_path

  def __enter__(self):
    self.start_time = datetime.datetime.now()
    self.file = open(self.path)
    return self.file
  
  def __exit__(self, exc_type, exc_val, exc_tb):
    self.file.close()
    self.end_time = datetime.datetime.now()
    self.uptime = self.end_time - self.start_time
    print(f'Program start time: {self.start_time}')
    print(f'Program end time: {self.end_time}')
    print(f'Program work time: {self.uptime}')


with manager('textfile.txt') as text:
  key = input('Do you want to see the textfile.txt contains? Y/N: ')
  while True:
    if key in ['y', 'Y']:
      print(f'\n{text.read()}\n')
      break
    elif key in ['n', 'N']:
      print('Okay then...\n')
      break
    else:
      key = input('Wrong key, eh? Try again: ')
  