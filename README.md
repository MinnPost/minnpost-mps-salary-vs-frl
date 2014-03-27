MPS Median Teacher Salary vs. Free/Reduced Lunch
==========================

Is there a relationship between a school's median teacher salary
or median experience level and the school's free-and-reduced-lunch-students
percentage?

Data
----
Data for this project was obtained via a data practices request to
Minneapolis Public Schools by Chris Stewart of the African American
Leadership Forum. The data included teacher name, salary, full time equivalent
percentage, and school It came as an Excel spreadsheet.

Data Processing
---------------
Since this story is not about specific teacher salaries but about school
aggregates, we decided to anonymize the data by running teacher names
through a hash function. After saving the original spreadsheet as a csv which
was then processed with `anonymize-teachers.py` which obscures the teacher names
(while giving a unique identifier) and selects the data columns relevant to
this project: teacher name, hire date, salary, FTE and program (school). Output
of this script can be found in `anonymized-teacher-salaries.csv`.

The next step was to eliminate teachers listed twice on the spreadsheet
(teachers at less than 100 FTE). `combine-fte.py` accomplishes this by either:
dropping teachers who are not full time or who split their time between multiple
schools or programs OR combining a teacher's different salaries at the same
program if they add up to 100FTE. The script also converts hire date to days of
experience by counting elapsed days between hire date and the date of the data
request, 1-14-2013. Results of this script can be found in
`combined-fte-teacher-salaries.csv`.

The final data processing step was to use teacher salaries to determine
aggregate data for each school. `school-aggregates.py` steps through each
teacher in `combined-fte-teacher-salaries.csv` and assigns their salary and
days of experience to their respective schools. It then goes through each school
and calculates mean, median, maximum and minimum of salary and experience for
each school. It also calculates the school's free/reduced lunch percentage
and percentage of white students, based on
`2012-2013-enrollment-special-populations.csv` and
`2012-2013-enrollment-ethnicity.csv`. It also includes the number of teachers
used for the calculation and categorizes schools as racially identifiable or
non-Title I, based on `data/12-13 Racially Identifiable Schools Accessible[2].pdf`
and `data/mmr-fr_designations_10-1-13.pdf`. The output of this script is found
in `school-aggregates.csv`.

Note that the script only includes a subset of schools in its output; it does
not include some specialty schools, like stand-alone special-ed programs as well
as administrative positions.

Visualizations
--------------
The main visualization for this project is a scatterplot comparing each school's
free/reduced price student percentage to its median salary. We use the Highcharts
library to create the plot.

Highcharts takes JSON for data input, so `school-data-json.py` assembles this
from `school-aggregates.csv`, outputting a JSON file with school name, median
salary, and free/reduced lunch percentage, as well as some styling things like
series color and title.

This is then pasted into index.html, which uses the Highcharts scatterplot
example.

We also wanted to create a data table for people to explore the data in more
detail, so `school-data-table.py` selects school name, median salary,
mean salary, free/reduced percentage and category from `school-aggregates.csv`
and writes them to a barebones HTML table, `school-data.html`. We format and
style the table using the Datatables jQuery library. See
`datatables-school-data.html`
