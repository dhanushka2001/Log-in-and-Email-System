import csv

def _csv_reader_with_strip(reader):
  yield from ((item.strip() for item in line) for line in reader)

class LookupSent:

  def __init__(self):
    self.sent = {}
    with open("sent.txt","r") as x:
      reader = _csv_reader_with_strip(
          csv.reader(x, delimiter="|")
      )
      for x in reader:
        ID, From, to, subject, mail = x
        self.sent[ID] = {
              "From": From,
              "To": to,
              "Subject": subject,
              "Message": mail
            }

  def get_all_sent(self):
    """Returns all usernames"""
    return self.sent

  def add_mail(self,From,to,subject,mail):
    """Adds user to users.users.txt"""
    n = len(self.sent)
    self.sent[n+1] = {
            "From": From,
            "To": to,
            "Subject": subject,
            "Message": mail
          }
    with open("sent.txt","w") as x:
      for sent_id,sent_info in self.sent.items():
        x.write(str(sent_id) + "|" + str(sent_info.get("From")) + "|" + str(sent_info.get("To")) + "|" + str(sent_info.get("Subject")) + "|" + str(sent_info.get("Message")) + "\n")