import csv
import json

with open('../data-processing/school-aggregates.csv','rU') as f:
  schooldata = csv.reader(f,delimiter='|',quotechar='"')

  #skip header
  schooldata.next()

  alldata = {'ri':[],'notitle1':[],'none':[]}


  for row in schooldata:
    category = row[13]
    name = row[0]
    frp = float(row[10])
    frp = round(frp*100,1)

    medsal = float(row[3])

    alldata[category].append({'x':frp, 'y':medsal, 'schoolname':name})

with open('frp-v-medsal.json','wb') as schooljson:

  colors = {'ri': '#af8dc3', 'notitle1':'#7fbf7b', 'none':'#a0a0a0'}

  categorytitles = {'ri':'Racially identifiable schools',
                    'notitle1':'Non-Title I schools',
                    'none':'Other schools'}

  jsondata = []

  for cat in alldata:
    jsondata.append({
      'name': categorytitles[cat],
      'color': colors[cat],
      'data': alldata[cat]
    })

  schooljson.write(json.dumps(jsondata))
