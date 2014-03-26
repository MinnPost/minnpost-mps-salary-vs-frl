import csv
import sys
import numpy

#a dict to match school names in original data request with school names in
#Free/Reduced Price Lunch and Ethnicity data
school_convert = {"Academic Superintendent Office":"Academic Superintendent Office","Adaptive Phys Ed":"Adaptive Phys Ed","After School & Summer School":"After School & Summer School","Andersen Open":"ANDERSEN COMMUNITY                 ","Andersen United Community":"ANDERSEN COMMUNITY                 ","Andersen United":"ANDERSEN COMMUNITY                 ","Anishinabe Academy":"ANISHINABE ACADEMY                 ","Anne Sullivan":"SULLIVAN ELEMENTARY                ","Anthony":"ANTHONY MIDDLE SCHOOL              ","Anwatin IB World School & Spanish Dual":"ANWATIN MIDDLE COM & SPANISH D I   ","Armatage":"ARMATAGE ELEMENTARY                ","Bancroft Elementary":"BANCROFT ELEMENTARY                ","Barton Open":"BARTON OPEN ELEMENTARY             ","Bethune":"BETHUNE ELEMENTARY                 ","Broadway Art & Technology":"BROADWAY ARTS & TECHNOLOGY         ","Bryn Mawr Primary":"BRYN MAWR ELEMENTARY               ","Burroughs":"BURROUGHS ELEMENTARY               ","Career & Technical Education":"Career & Technical Education","Cityview Performing Arts Magnet":"CITYVIEW PAM MAGNET                ","Contract Alternatives":"Contract Alternatives","Curriculum &  Instruction":"Curriculum &  Instruction","Dowling Elementary":"DOWLING ELEMENTARY                 ","Early Childhood Family Education":"Early Childhood Family Education","Early Childhood Special Education":"ECSE                               ","Edison High":"EDISON SENIOR HIGH                 ","Elementary Assistant Principals":"Elementary Assistant Principals","Emerson Spanish Immersion":"EMERSON ELEMENTARY                 ","English Language Learners-ESL":"English Language Learners-ESL","Field":"FIELD ELEMENTARY                   ","Folwell Performing Arts":"FOLWELL ARTS MAGNET                ","Guidance & Counseling":"Guidance & Counseling","Hale Elementary":"HALE ELEMENTARY                    ","Hall International":"HALL INTERNATIONAL                 ","Harrison Education Center":"HARRISON EDUCATION CENTER          ","Health Services":"Health Services","Hearing Impaired":"Hearing Impaired","Hennepin Cty Juv Just Ctr":"Hennepin Cty Juv Just Ctr","Henry High":"HENRY SENIOR HIGH                  ","Hiawatha Elementary":"HIAWATHA ELEMENTARY                ","Hmong International Academy":"HMONG INTERNATIONAL ACADEMY        ","Hospital Agency":"Hospital Agency","Indian Education":"Indian Education","Information Technology":"Information Technology","Jefferson Elementary":"JEFFERSON ELEMENTARY               ","Jenny Lind":"JENNY LIND ELEMENTARY              ","Jenny Lind Elementary":"JENNY LIND ELEMENTARY              ","Kenny Elementary":"KENNY ELEMENTARY                   ","Kenwood Elementary":"KENWOOD ELEMENTARY                 ","Labor Relations/Employee Relations":"Labor Relations/Employee Relations","Lake Harriet Lower (Audubon)":"LAKE HARRIET LOWER ELEMENTARY      ","Lake Harriet Upper (Fulton)":"LAKE HARRIET UPPER SCHOOL          ","Lake Nokomis Keewaydin":"LK NOKOMIS COMM-KEEWAYDIN CAMPUS   ","Lake Nokomis Wenonah":"LK NOKOMIS COMM-WENONAH CAMPUS     ","Loring Elementary":"LORING ELEMENTARY                  ","Lucy Laney Elementary":"LUCY LANEY @ CLEVELAND PARK ELEM.  ","Lyndale Elementary":"LYNDALE ELEMENTARY                 ","Marcy Open School":"MARCY OPEN ELEMENTARY              ","Minneapolis Kids":"Minneapolis Kids","MPS  Deaf/Hard of Hearing":"MPS D/HH                           ","MPS Metro HA":"MPS METRO HA                       ","MPS Metro SJ (St. Joe's Home Children)":"MPS METRO SJ                       ","Nellie Stone Johnson":"NELLIE STONE JOHNSON ELEMENTARY    ","North (ISA)":"NORTH ACADEMY ARTS/COMMUNICATION   ","North High":"NORTH SENIOR HIGH                  ","Northeast Middle School":"NORTHEAST MIDDLE                   ","Northrop Elementary":"NORTHROP ELEMENTARY                ","Occupational, Physical Therapists":"Occupational, Physical Therapists","Office of the Chief Academic Officer":"Office of the Chief Academic Officer","Olson Middle School":"OLSON MIDDLE                       ","Olson/Lind Lower":"Olson/Lind Lower","Olson/Lind Upper":"Olson/Lind Lower","Online Learning":"Online Learning","Organizational & Professional Develop.":"Organizational & Professional Develop.","Pierre Bottineau French Immersion":"PIERRE BOTTINEAU                   ","Pillsbury Math/Science/Technology":"PILLSBURY ELEMENTARY               ","Pratt Elementary":"PRATT ELEMENTARY                   ","Psychology Services":"Psychology Services","Ramsey Middle School":"RAMSEY MIDDLE                      ","Reserve Teachers":"Reserve Teachers","Richard Green Central":"Richard Green Central","River Bend":"RIVER BEND EDUCATIONAL CENTER      ","Roosevelt High":"ROOSEVELT SENIOR HIGH              ","Sanford Middle School":"SANFORD MIDDLE                     ","School Readiness":"School Readiness","Secondary Programs":"Secondary Programs","Seward Montessori School":"SEWARD ELEMENTARY                  ","Sheridan International Fine Arts":"SHERIDAN ELEMENTARY                ","South High":"SOUTH SENIOR HIGH                  ","Southwest High":"SOUTHWEST SENIOR HIGH              ","Span Central Middle Schools":"SPAN                               ","Span High School":"SPAN HIGH                          ","Special Ed 023":"SPECIAL ED - SPEECH ONLY           ","Speech Language Clinicians":"Speech Language Clinicians","St. Joseph's Home for Children":"St. Joseph's Home for Children","Stadium View":"STADIUM VIEW                       ","Strategic Workforce Management":"Strategic Workforce Management","Student Placement":"Student Placement","Student Services":"Student Services","TAPPPOffice":"TAPPPOffice","Teaching & Learning":"Teaching & Learning","Transition Plus":"TRANSITION PLUS SERVICES           ","Waite Park Elementary":"WAITE PARK ELEMENTARY              ","Washburn High":"WASHBURN SENIOR HIGH               ","Wellstone Intl High School":"WELLSTONE INTERNATIONAL HIGH       ","Wenonah Elementary":"Wenonah Elementary","Whittier Community School":"WHITTIER INTERNATIONAL             ","Windom Elementary":"WINDOM SCHOOL                      ","Richard Green Central":"GREEN CENTRAL PARK ELEMENTARY      "}

#we'll only keep schools on this list (eliminates some nontraditional programs)
keep_schools = ['Transition Plus','River Bend','North (ISA)','Pratt Elementary','Lake Nokomis Wenonah','Seward Montessori School','Folwell Performing Arts','Kenwood Elementary','Lake Harriet Upper (Fulton)','Armatage','Hale Elementary','South High','Edison High','Henry High','Nellie Stone Johnson','Bryn Mawr Primary','Hmong International Academy','Whittier Community School','Northrop Elementary','Emerson Spanish Immersion','Hiawatha Elementary','Jenny Lind','Lake Nokomis Keewaydin','Sanford Middle School','Anne Sullivan','Jefferson Elementary','Anishinabe Academy','Harrison Education Center','Burroughs','Bancroft Elementary','Jenny Lind Elementary','Pillsbury Math/Science/Technology','Andersen Open','Northeast Middle School','Dowling Elementary','Anthony','Ramsey Middle School','Olson Middle School','Wellstone Intl High School','Loring Elementary','Sheridan International Fine Arts','Anwatin IB World School & Spanish','Dual','Roosevelt High','North High','Kenny Elementary','Andersen United','Bethune','Lake Harriet Lower (Audubon)','Southwest High','Field','Barton Open','Hall International','Lyndale Elementary','Washburn High','Lucy Laney Elementary','Waite Park Elementary','Windom Elementary','Stadium View','Marcy Open School','Pierre Bottineau French Immersion','Richard Green Central']

#Schools that don't accept Title I funding
nontitleone = ['Armatage','Barton Open','Burroughs','Field','Hale Elementary','Kenwood Elementary','Lake Harriet Upper (Fulton)','Lake Harriet Lower (Audubon)']

#Racially-identifiable schools
ri = ['Andersen Open','Anne Sullivan','Andersen United','Bethune','Bryn Mawr Primary','Hall International','Henry High','Hmong International Academy','Jenny Lind','Lucy Laney Elementary','Nellie Stone Johnson','North (ISA)','North High','Olson Middle School','Richard Green Central','Sheridan International Fine Arts']

#create some dicts with free-reduced price percentages and pct of white students for schools in the state
frp = {}
whtpct = {}

with open('2012-2013-enrollment-special-populations.csv','rb') as f:
  specpop = csv.reader(f,delimiter='|',quotechar='"')

  #skip header
  specpop.next()

  for row in specpop:
    if row[10] == "All Grades" and row[11] != '' and row[5] == "MINNEAPOLIS PUBLIC SCHOOL DIST.    ":
      school = row[7]

      total_students = float(row[11])

      if row[12] == '':
        free_students = 0
      else:
        free_students = float(row[12])

      if row[13] == '':
        reduced_students = 0
      else:
        reduced_students = float(row[13])

      frp[school] = (free_students + reduced_students) / total_students

with open('2012-2013-enrollment-ethnicity.csv','rb') as f:
  ethn = csv.reader(f,delimiter='|',quotechar='"')

  #skipheader
  ethn.next()

  for row in ethn:
    if row[10] == "All Grades" and row[24] != '' and row[5] == "MINNEAPOLIS PUBLIC SCHOOL DIST.    ":
      school = row[7]

      total_students = float(row[24])

      if row[23] == '':
        minority_students = 0
      else:
        minority_students = float(row[23])

      whtpct[school] = (total_students-minority_students) / total_students


#create dict with school name as key and
""""
school_data {school_name: {'salaries':[], 'experience':[]}}
"""

school_data = {}

#creating two lists to track district-wide medians
all_exp = []
all_sal = []

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file,"rb") as f1:
  teacher_data = csv.reader(f1,delimiter='|',quotechar='"')
  with open(output_file,"wb") as f2:
    school_averages = csv.writer(f2,delimiter='|',quotechar='"')

    #write a header row
    school_averages.writerow(['school','school2','meansal','mediansal','minsal','maxsal','meanexp','medianexp','minexp','maxexp','schoolfrp','schoolpctwht','nteachers','category'])

    #first add all teachers' salaries and experience levels to lists based on their schools
    for row in teacher_data:

      #data has two names for Jenny Lind, so we combine them here
      if row[4] == 'Jenny Lind Elementary':
        school = 'Jenny Lind'

      #there are also two Andersen schools in the data, but it's the same school
      elif row[4] == 'Andersen Open' or row[4] == 'Andersen United':
        school = 'Andersen United Community'
      else:
        school = row[4]

      if school in school_data:
        school_data[school]['salaries'].append(int(row[2]))
        school_data[school]['experience'].append(int(row[1]))

      else:
        school_data[school] = {'salaries': [int(row[2])],
                               'experience': [int(row[1])]}

      #also add each experience and salary to respective district-wide lists
      all_exp.append(int(row[1]))
      all_sal.append(int(row[2]))

    #now iterate through all the schools and write rows to output csv with data
    for school in school_data:

      school_data[school]['salaries'].sort()

      mean_salary = numpy.mean(school_data[school]['salaries'])
      median_salary = numpy.median(school_data[school]['salaries'])
      min_salary = school_data[school]['salaries'][0]
      max_salary = school_data[school]['salaries'][-1]

      school_data[school]['experience'].sort()

      mean_experience = numpy.mean(school_data[school]['experience'])
      median_experience = numpy.median(school_data[school]['experience'])
      min_experience = school_data[school]['experience'][0]
      max_experience = school_data[school]['experience'][-1]

      if school_convert[school] in frp:
        school_frp = frp[school_convert[school]]
      else:
        school_frp = "N/A"

      if school_convert[school] in whtpct:
        school_pctwhite = whtpct[school_convert[school]]
      else:
        school_pctwhite = "N/A"

      n_teachers = len(school_data[school]['salaries'])

      #test for a couple of categories
      if school in nontitleone:
        category = 'notitle1'
      elif school in ri:
        category = 'ri'
      else:
        category = 'none'

      #only record output data for the programs we're interested in
      if school in keep_schools:
        school_averages.writerow([school,
                                  school_convert[school],
                                  mean_salary,
                                  median_salary,
                                  min_salary,
                                  max_salary,
                                  mean_experience,
                                  median_experience,
                                  min_experience,
                                  max_experience,
                                  school_frp,
                                  school_pctwhite,
                                  n_teachers,
                                  category
                                ])

print ("District median experience: %s" % numpy.median(all_exp))
print ("District median salary: %s" % numpy.median(all_sal))
