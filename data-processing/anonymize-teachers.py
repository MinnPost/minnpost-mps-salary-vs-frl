import sys
import hashlib
import csv

input_file = sys.argv[1]
output_file = sys.argv[2]
salt = sys.argv[3]

with open(input_file,"rb") as input_f:
  salary_data = csv.reader(input_f, delimiter='|', quotechar='"')


  with open(output_file,"wb") as output_f:
    results_file = csv.writer(output_f, delimiter='|', quotechar='"')

    #skip header
    salary_data.next()

    for row in salary_data:
      teacher_name = row[0]
      h = hashlib.md5(teacher_name+salt)

      #Hash teacher name
      r = [h.hexdigest()]

      #Select data rows relevant to this project
      r.append(row[1]) #hire date
      r.append(row[3]) #salary
      r.append(row[4]) #fte
      r.append(row[5]) #organizational unit

      results_file.writerow(r)
