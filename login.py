from lookup_users import LookupUsers
from lookup_sent import LookupSent

class Login:
  user = None
  pas = None

  def __init__(self):
    self.lookup_users = LookupUsers()
    self.lookup_sent = LookupSent()

  def current_users(self):
    self.lookup_users = LookupUsers()
    users = self.lookup_users.get_all_users()
    #returns a dictionary {"username": "password"}
    return users

  def current_sent(self):
    self.lookup_sent = LookupSent()
    sent = self.lookup_sent.get_all_sent()
    #sent is a dictionary of dictionaries, where the primary dictionaries
    #are the messages (to, from, subject,message), and the keys are the ID.
    return sent
    

  def login(self):
    while True:
      ans = input("| 1 = Log-in | 2 = Sign-up |\n")
      if ans == "1":
        self.user = input("Please enter your username: ")
        while True:
          #infinite if loop, check if there is a username that matches in list
          #keep asking till they give a registered username

          if self.user not in self.current_users().keys():
            print("{} is not a registered username".format(self.user))
            self.user = input("Please enter your username: ")
            #they get username correct
          else:
            #3 tries allowed to get password correct
            tries = 3
            print("Hello {}.".format(self.user))
            self.pas = input("Please enter your password: ")
            while tries > -1:
              #if they get the password correct success message and kill while loop
              #self.lookup = Lookup()
              if self.current_users()[self.user] == self.pas:
                print("Successfully logged in to {}'s account.".format(self.user))
                self.menu()
              else:
                if tries > 1:
                  print("Invalid password, {} more attempts.".format(tries))
                  tries -= 1
                  self.pas = input("Please enter your password: ")
                  #add elif statement to fix "1 more attempts" grammar error
                elif tries == 1:
                  print("Invalid password, {} more attempt.".format(tries))
                  tries -= 1
                  self.pas = input("Please enter your password: ")
                #if no attempts left show error message and kill while loop
                else:
                  print("No more attempts! Try again later.")
                  #return
                  self.login()
          
      elif ans == "2":
        print("Add a new account")
        self.user = input("Username: ")
        while True:
          if self.user in self.current_users().keys():
            print("{} is already taken, try another username".format(self.user))
            self.user = input("Username: ")
          elif " " in self.user:
            print("Username cannot contain any spaces!")
            self.user = input("Username: ")
          else:
            self.pas = input("Password: ")
            while True:
              if len(self.pas) < 4:
                print("Password must be greater than 3 characters! Try another password.")
                self.pas = input("Password: ")
              elif " " in self.pas:
                print("Password cannot contain any spaces!")
                self.pas = input("Password: ")
              elif sum(x.isdigit() for x in self.pas) == 0:
                print("Password must contain at least 1 number! Try another password.")
                self.pas = input("Password: ")
              elif sum(x.isalpha() for x in self.pas) < 3:
                print("Password must contain at least 3 letters! Try another password.")
                self.pas = input("Password: ")
              else:
                self.lookup_users.add_user(self.user,self.pas)
                print("Successfully created new account.")
                self.login()
      else:
        print("{} is not a valid option.".format(ans))
        self.login()

  def menu(self):
    main = input("| 1 = Email | 2 = Manage account | 3 = Sign out |\n")
    if main == "1":
      self.email()

    elif main == "2":
      self.manage()
    
    elif main == "3":
      print("Signing out...")
      #print(sent)
      #for a,b in sent.items():
      #  print(b)
      self.login()
    
    else:
      print("{} is not a valid option.".format(main))
      self.menu()

  def email(self):
    emailer = input("| 1 = Compose | 2 = Inbox | 3 = Sent | 4 = Go back |\n")
    if emailer == "1":
      to = input("To: ")
      while True:
        if to not in self.current_users().keys():
          print("{} is not a registered username.".format(to))
          to = input("To: ")
        else:
          subject = input("Subject: ")
          mail = input("Compose: ")
          if len(mail) == 0:
            print("Error! Email must contain a message.")
            mail = input("Compose: ")
          else:
            self.lookup_sent.add_mail(self.user,to,subject,mail)
            print("Message sent!")
            self.email()
    elif emailer == "2":
      print("Loading your inbox...")
      c = list(self.current_sent().values())
      #c is a list of dictionaries, the dictionaries are the messages
      d = [x["To"] for x in c]
      #d is just a list of all the people all the messages were sent to
      if any(value == self.user for value in d):
      #checking if any of the values in d are to the user  
        for sent_id, sent_info in sorted(self.current_sent().items(), reverse = True):
          if sent_info.get("To") == self.user:
            print("\n  ID: {}".format(sent_id))
            for key in sent_info:
              if key == "To":
                continue
              print("  {}: {}".format(key, sent_info[key]))
        self.email()
        #email() is back under for loop since you want to get all messages sent to user
      else:
        print("Inbox empty!")
        #if no values in d are to the user then imbox is empty
      self.email()
    elif emailer == "3":
      print("Loading sent mail...")
      c = list(self.current_sent().values())
      d = [x["From"] for x in c]
      if any(value == self.user for value in d):
        for sent_id, sent_info in sorted(self.current_sent().items(), reverse = True):
          if sent_info.get("From") == self.user:
            print("\n  ID: {}".format(sent_id))
            for key in sent_info:
              if key == "From":
                continue
              print("  {}: {}".format(key, sent_info[key]))
        self.email()
      else:
        print("Empty!")
      self.email()
    elif emailer == "4":
      print("Back to main menu...")
      self.menu()
    else:
      print("{} is not a valid option.".format(emailer))
      self.email()

  def manage(self):
    manager = input("| 1 = Change username | 2 = Change password | 3 = Delete account | 4 = Go back |\n")
    if manager == "1":
      newuser = input("Please enter a new username: ")
      if newuser in self.current_users().keys():
        if self.user == newuser:
          print("{} is your current username!".format(newuser))
          self.manage()
        else:
          print("{} is already taken, try another username.".format(newuser))
          self.manage()
      else:
        self.lookup_users.change_name(self.user,newuser)
        for sent_id, sent_info in self.current_sent().items():
          if sent_info.get("From") == self.current_sent() and sent_info.get("To") == self.current_sent():
            sent_info.update(From = newuser)
            sent_info.update(To = newuser)
          elif sent_info.get("To") == self.user:
            sent_info.update(To = newuser)
          elif sent_info.get("From") == self.user:
            sent_info.update(From = newuser)
          #finally fixed the issue where when u change username it causes havoc, celebrated a bit too early but the fix was still fairly easy, only took a year to bother to fix -_-
          #old comment ^ 
              
        self.user = newuser
        print("Successfully changed your username to {}.".format(newuser))
        self.manage()
    elif manager == "2":
      tries = 3
      trypass = input("Please enter your current password: ")
      while tries > -1:
        if trypass == self.pas:
          newpass = input("Please enter your new password: ")
          while True:
            if len(newpass) < 4:
              print("Password must be greater than 3 characters! Try another password.")
              newpass = input("Password: ")
            elif sum(x.isdigit() for x in newpass) == 0:
              print("Password must contain at least 1 number! Try another password.")
              newpass = input("Password: ")
            elif sum(x.isalpha() for x in newpass) < 3:
              print("Password must contain at least 3 letters! Try another password.")
              newpass = input("Password: ")
            else:
              self.lookup_users.change_pass(self.user,newpass)
              self.pas = newpass
              print("Successfully changed your password to {}.".format(newpass))
              self.manage()
          
        else:
          if tries > 1:
            print("Invalid password, {} more attempts.".format(tries))
            tries -= 1
            trypass = input("Please enter your current password: ")
            #add if statement to fix "1 more attempts" grammar error
          elif tries == 1:
            print("Invalid password, {} more attempt.".format(tries))
            tries -= 1
            trypass = input("Please enter your current password: ")
            #if no attempts left show error message and kill while loop
          else:
            print("No more attempts! Try again later.")
            self.login()

      self.manage()
    elif manager == "3":
      trypass = input("Please enter your password: ")
      tries = 3
      while tries > -1:
        if trypass == self.pas:
          print("This is irreversible.")
          print("Are you sure you want to delete your account?")
          choice = input("| 1 = YES | 2 = NO |\n")
          if choice == "1":
            self.lookup_user.remove_user(self.user,self.pas)
            print("Successfully deleted your account!")
            self.login()
          elif choice == "2":
            self.manage()
          else:
            print("{} is not a valid option.".format(choice))
            self.manage()
        else:
          if tries > 1:
            print("Invalid password, {} more attempts.".format(tries))
            tries -= 1
            trypass = input("Please enter your password: ")
            #add if statement to fix "1 more attempts" grammar error
          elif tries == 1:
            print("Invalid password, {} more attempt.".format(tries))
            tries -= 1
            trypass = input("Please enter your password: ")
            #if no attempts left show error message and kill while loop
          else:
            print("No more attempts! Try again later.")
            self.login()
      self.manage()
    elif manager == "4":
      print("Back to main menu...")
      self.menu()
    else:
      print("{} is not a valid option.".format(manager))
      self.manage()
