import csv

with open('../data-processing/school-aggregates.csv','rU') as src:
  schooldata = csv.reader(src, delimiter='|', quotechar='"')

  #skip header
  schooldata.next()

  with open ('school-data.html',"wb") as out:
    out.write("""
    <table>
      <thead>
        <tr>
          <th>School</th>
          <th>Median salary</th>
          <th>Mean salary</th>
          <th>Free/reduced lunch %</th>
          <th>Category</th>
        </tr>
      </thead>
      <tbody>
    """)

    for row in schooldata:
      school = row[0]
      medisal = round(float(row[3]),0)
      medisal = int(medisal)
      medisal = str(medisal)
      medisal = medisal[0:2] + "," + medisal[2:]

      meansal = round(float(row[2]),0)
      meansal = int(meansal)
      meansal = str(meansal)
      meansal = meansal[0:2] + "," + meansal[2:]


      frp = round(float(row[10])*100,0)
      frp = int(frp)

      categorytitles = {'ri':'Racially identifiable',
                        'notitle1':'Non-Title I',
                        'none':'Other'}
      category = categorytitles[row[13]]

      out.write("""
        <tr>
          <td>%s</td>
          <td style="text-align:right;">%s</td>
          <td style="text-align:right;">%s</td>
          <td style="text-align:right;">%s</td>
          <td>%s</td>
        </tr>

      """%(school, medisal, meansal, frp, category))

    out.write("""
      </tbody>
    </table>
    """)
