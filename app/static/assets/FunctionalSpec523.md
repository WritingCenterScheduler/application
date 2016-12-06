
**Primary functions**

- The main goal of our website is to provide our client with an optimal, automated way to schedule undergraduate work study hours in the five locations available.
- Due to the multiple, variable constraints of the problem, and the multiple locations and employees a fast, optimal scheduling algorithm will be needed.
- In addition, the project will need an intuitive user interface so that both work-study employees and administrators can access and easily use the scheduler.

**Use Cases**

Work-study employees

1. Login with SSO authentication
    * Employees will use their ONYEN and password in order to access their personal page.
2. Specify Availability
    * Employee clicks availability tab and a schedule is brought up where they can fill out their availability
    * Employee can select for each 30- minute time slot on the calendar either &quot;Good to work&quot;, &quot;Okay to work&quot; or &quot;Cannot work&quot; based on their individual preferences.
      * As the employee fills out their availability the sections of time they are filling out change color accordingly; red to indicate cannot work, yellow to indicate okay to work, and green to indicate good to work.
      *  Once the employee has completed their availability the schedule, the employee must hit Submit to send the information to the database where the data will be saved so that employees may update or change their availability at later dates.
3. View Schedule
    * Employee can click &quot;schedule&quot; tab in order to view the final approved schedule set by the administrator including their hours.
4. Logout
    *  User can hit the logout tab in order to logout from service

Administrator

1. Login with SSO authentication
    * Administrators will use their ONYEN and password in order to access their personal page which will have administrative capabilities.
2. Generate Schedule/modify schedule
    * The home page will consist of a calendar with the days of the week listed on the top and the times of day listed on the right. Along the bottom of the calendar will be a list of tabs to switch between the schedules for each of the buildings.
    * The times that each of the building will be greyed out and will not have employee scheduled to these times.
    * Each employee will be displayed in their scheduled time slots on the calendar; in addition, below the calendar each of the employees will have a drag-able bubble which will display the employees name as well as the number of hours they are currently working per week versus the number of hours they need to work per week in order to meet the amount allocated in their work-study grant.
    * The user can drag and drop these bubbles from underneath the schedule onto the actual calendar in order to modify the generated schedule. If employees need to be removed from the schedule they can be removed from the schedule by drag and dropping their names off the calendar.
    * When the user is done editing the schedule they will click to submit the edited version to the database which will update the schedule on the employee view of the website as well.
3. View and modify employee and potential employee info
    * The user can click on an employee&#39;s tab at the top of the page in order to get information about the potential and rehired employees.
    * This information will include a section to enter the total amount they are receiving for their grant, the number of hours needed to work per week based on that total, as well as identifying information about the employee such as PID, university email, and full name.
4. Logout
    * User can hit the logout tab in order to logout from service

**Requirements (in order of importance)**

1. Provide a robust and reasonable speed scheduling algorithm under the constraints listed below.
    * Only return hires are allowed to be scheduled to peer tutoring at Greenlaw
    * Two employees must be scheduled to peer tutoring at Greenlaw during the hours that it is available
  2. An employee must be scheduled for at least an hour at a time; not allowed to make employees come in for a single 30 minute period.
  3. A single multiple hour block in a day is preferable to multiple single hour blocks in a day for a tutor.
  4. All times during which centers are open must be filled with at least one tutor where possible; some may be left for her to manually fill.
  5. All return hires should be scheduled before exploring options for potential hires that would help to fill out the gaps in the schedule
  6. Employees should be scheduled to as close to their desired amount of hours as possible
  7. Employees should not change tutoring location mid-shift with the exception of being able to move from learning center upstairs to learning center downstairs
8. Provide employees with a way to specify availability information and access the finalized schedule
    *  Employees will login to the site using their ONYEN and password
    *  Employees will view a calendar on which they can select for each 30- minute time slot on the calendar either &quot;Good to work&quot;, &quot;Okay to work&quot; or &quot;Cannot work&quot; based on their individual preferences.
9.  Employees can access but will not be able to edit the master calendar through a separate tab at the top of the page.
10.  Provide an interface from which the schedule can be manually changed by the administrator if need be.
     *  Administrator should be able to see how many hours an employee is scheduled for in relation to the number of hours they need to be scheduled for in order to get the full sum of their grant.
     *  Administrator should be able to remove people and add people to the calendar as they see fit.
     *  Administrator should be able to see the availability of  an employee when they go to add them to the calendar so that they avoid adding them into a spot they cannot work
     *  Provide an interface through which to access employee and potential employee information
11. The administrator should be able to fill in the amount of money awarded to each employee through their work study grant, their hourly pay and their start date. From this the system should calculate the number of hours needed each week in order for the employee to meet their goal.
12. The administrator should be provided with each potential employee and return employees personal information such as PID, university email and full name.
13. The administrator should be able to see each individual person&#39;s availability that they entered in their page.

 