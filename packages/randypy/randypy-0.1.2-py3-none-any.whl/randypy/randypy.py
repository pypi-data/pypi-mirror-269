import random
import string
import uuid
import datetime

def percentage():
  return random.random()

def randyint(min_value, max_value):
  return random.randint(min_value, max_value)

def randyfloat(min_value, max_value):
  return random.uniform(min_value, max_value)

def choice(seq):
  return random.choice(seq)

def shuffle(seq):
  random.shuffle(seq)
  return seq

def str(length):
  characters = string.ascii_letters + string.digits
  str = ''.join(random.choice(characters) for _ in range(length))
  return str

def name():
  first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Daniel", "Olivia", "Christopher", "Sophia",
    "William", "Elizabeth", "Matthew", "Samantha", "Andrew", "Jessica", "Joseph", "Ashley", "Joshua", "Amanda"]
  last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]
  return f"{random.choice(first_names)} {random.choice(last_names)}"

def email(domain="example.com"):
  email = f"{str(8)}@{domain}"
  return email

def password(length=12, include_digits=True, include_special_chars=True):
  if length < 8:
    print("비밀번호는 8자리 이상이어야 합니다.")
    return 
  
  char_num = length
  digit_num = 0
  special_char_num = 0

  if include_digits and include_special_chars:
    char_num = random.randint(1, length-2)
    digit_num = random.randint(1, length-char_num-1)
    special_char_num = length - char_num - digit_num
  elif include_digits:
    char_num = random.randint(1, length-1)
    digit_num = length - char_num
  elif include_special_chars:
    char_num = random.randint(1, length-1)
    special_char_num = length - char_num

  password = list()
  password.extend([random.choice(string.ascii_letters) for i in range(char_num)])
  password.extend([random.choice(string.digits) for i in range(digit_num)])
  password.extend([random.choice(string.punctuation) for i in range(special_char_num)])
  random.shuffle(password)
  return ''.join(password[:])

def UUID():
  return uuid.uuid4()

def date(start_date, end_date):
  try:
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + datetime.timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d')
  except ValueError:
    print('날짜 형식은 "YYYY-mm-dd"으로 지정해야 합니다.')
    return

def color():
  return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))