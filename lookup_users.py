import csv

def _csv_reader_with_strip(reader):
  yield from ((item.strip() for item in line) for line in reader)

class LookupUsers:

  def __init__(self):
    self.users = {}
    with open("users.txt","r") as x:
      reader = _csv_reader_with_strip(
          csv.reader(x, delimiter=" ")
      )
      for x in reader:
        user, pas = x
        self.users[user] = pas

  def get_all_users(self):
    """Returns all users (username and password) as a dictionary"""
    return self.users
  
  def get_all_passwords(self):
    """Returns all passwords"""
    return list(self.users.values())

  def add_user(self,username,password):
    """Adds user to users.users.txt"""
    with open("users.txt","w") as x:
      self.users[username]=password
      for key,value in self.users.items():
        x.write(str(key) + " " + str(value) + "\n")

  def change_name(self,oldname,newname):
    with open("users.txt","w") as x:
        self.users[newname] = self.users.pop(oldname)
        for key,value in self.users.items():
          x.write(str(key) + " " + str(value) + "\n")

  def change_pass(self,username,newpass):
    with open("users.txt","w") as x:
        self.users[username] = newpass
        for key,value in self.users.items():
          x.write(str(key) + " " + str(value) + "\n")

  def remove_user(self,username,password):
    """Removes user to users.users.txt"""
    with open("users.txt","w") as x:
        del self.users[username]
        for key,value in self.users.items():
          x.write(str(key) + " " + str(value) + "\n")