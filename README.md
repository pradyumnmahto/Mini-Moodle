# Welcome to the project: Portal for The Courses

## About the Project:
We developed a learning environment/ Course Management System similar to Moodle.<br/>
Moodle is a free and open-source learning management system written in PHP and distributed under the GNU General Public License. Moodle is used for blended learning, distance education, flipped classroom and other online learning projects in schools, universities, workplaces and other sectors. Moodle is used to create custom websites with online courses and allows for community-sourced plugins.<br/>
What we have implemented could be called something like a 'mini-moodle'. It just serves the purpose of managing the databases of a college with teachers, students, corresponing courses and assignments.

### Stack Used:
* Django for Web Framework
* Html for Web Development
* Bootstrap with CSS for Web Enhancement
* Python for backend programming

## Features Implemented:

### User SignUp and Login-
+ A user can signup using his mail id and by specifying a desired unique username.
+ The user can either signup as a Teacher or as a Student
+ Only a registered user will be able to login and view the website
+ A secure login with a user set-up password and a unique username
+ The users can also change their password using an encrypted link sent on their email
+ Once logged in, the users can view and also edit their profile still under the constraint of unique email and username

### Courses and Assignments:
+ A teacher can create courses that are visible to all the registered users (i.e. registered students)
+ As soon as a teacher creates a course, a randomly generated 6 letter code is associated with the course and an email is sent to all the students, with a link which they can use to register for the course directly
+ The students can also join a specific course by entering the corresponding 6 letter course code on a separate page
+ The teacher can only view his/her created courses and the student can view only courses he/she has registered for
+ Within the course page, the teacher can create assignments that shall be visible to all the students registerd for the course
+ The students can view the assignments posted and can submit files to the corresponding assignment and later view and download their submission
+ Only the latest submission of the student shall be stored
+ The teacher can view all the submissions made by the students to a particular course
+ He/She can download the submissions individually or download all the submissions as a .tgz file

### Grading and Feedback:
+ The teacher can post grades and feedback to any particular assignment submission
+ Or can submit a csv file with the data of all grades and feedback for all the students, and shall be visible to the students immediately

### File Extension Verification:
+ The Teacher when creating an assignment, can specify the type of files expected
+ The student won't be able to submit files other than files of this type

### Autograding and File Directory Verification
+ The teacher can also specify an expected tree directory structure of the submitted archives
+ The students must match the tree structure, else their submission won't be accepted
+ The teacher can also submit an autograder file to evaluate the submissions of the students (Didn't find enough time to implement the autograding part but nevertheless accpeting the autograding script)

### Highlights and Bonuses:
+ Unique username with an encrypted password login
+ Password resetting through an encoded link sent on the user mail
+ View and Edit user profile
+ Creating courses and assignments and Registering to courses via an email invitation or a unique code
+ Able to only view data concerned with the particular user
+ Students can submit files to assignments, which is type and tree restricted
+ Teacher can grade the assignments through a csv file or individually
+ Teacher can download all the assignment submisisons as an archive, with a single click

