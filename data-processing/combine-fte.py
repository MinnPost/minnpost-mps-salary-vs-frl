import csv
import re
import sys
from datetime import date




#remove dollar signs and commas from salary, return an integer
def clean_salary(salary):
  s = re.sub(r'[^\d.]', '', salary)
  return int(s[:-3])

#convert hire date to days elapsed between hire date and 1/14/2013
def convert_hire_date(hire_date):
  months = {
    'Jan' : 1,
    'Feb' : 2,
    'Mar' : 3,
    'Apr' : 4,
    'May' : 5,
    'Jun' : 6,
    'Jul' : 7,
    'Aug' : 8,
    'Sep' : 9,
    'Oct' : 10,
    'Nov' : 11,
    'Dec' : 12
  }

  #Data request dated 1/14/2013 so use that as baseline for days of employ
  school_start_date = date(2013, 1, 14)

  hire_date = hire_date.split("-")

  #start day is first number
  employee_hire_day = int(hire_date[0])

  #lookup 3 letter month digit
  employee_hire_month = months[hire_date[1]]

  #covert hire year to 4 digits
  if int(hire_date[2]) < 13:
    employee_hire_year = int("20" + hire_date[2])
  else:
    employee_hire_year = int("19" + hire_date[2])

  employee_hire_date = date(employee_hire_year, employee_hire_month, employee_hire_day)

  elapsed = school_start_date - employee_hire_date

  return elapsed.days


inputfile = sys.argv[1]
outputfile = sys.argv[2]

holding_row = ['null']

with open(inputfile,'rb') as original_file:
  original_data = csv.reader(original_file, delimiter='|', quotechar='"')
  with open (outputfile,'wb') as cleaned_file:
    cleaned_data = csv.writer(cleaned_file, delimiter='|', quotechar='"')


    #iterate through the rows
    for row in original_data:

      #special exceptions for two rows
      if '-' in row[2]:
        continue
      if row[3] == '0.1':
        continue

      #if the row is 100 FTE just write it to the new spreadsheet
      if int(row[3]) == 100:
        cleaned_data.writerow([row[0], convert_hire_date(row[1]),
        clean_salary(row[2]), row[3], row[4]])

      #else, it is less than 100FTE
      else:
        #if we have held a previous row that was less than 100 check if it's the
        #same peson and that the position is with the same organizational unit

        if holding_row[0] == row[0] and holding_row[4] == row[4]:
          combined_salary = holding_row[2] + clean_salary(row[2])

          #see if total FTEs are 100. if so, write the row
          if int(holding_row[3]) + int(row[3]) == 100:
            cleaned_data.writerow([row[0], convert_hire_date(row[1]),
            combined_salary, int(row[3])+holding_row[3], row[4]])

            holding_row = ['null']

          #if not, combine FTE, days and salary totals and make new holding row
          else:
            holding_row = [row[0], row[1], combined_salary, int(row[3])
            +holding_row[3], row[4]]

        #if it's not the same person or the person is split between programs,
        #discard old holding row and create new one
        else:
          holding_row = [row[0], convert_hire_date(row[1]),
          clean_salary(row[2]), int(row[3]), row[4]]
