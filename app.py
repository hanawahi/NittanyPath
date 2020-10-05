from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql

# Author: Hana Wahi
# Email: HQW5245@psu.edu
# See README for further details.

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

host = 'http://127.0.0.1:5000/'


# Main/Index app route:
@app.route('/')
def index():
    return render_template('index.html')


# Student log in ------------------------------------------------->
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message
    msg = ''
    # Do "username" and "password" POST requests exist?
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT * FROM Students WHERE Email = ? AND Password = ?;', (username, password))
        # Fetch one record and return result
        account = cursor.fetchall()
        # If account exists in accounts table in out database
        if account:
            # Information for EMAIL (session ID) only
            cursor2 = connection.execute('SELECT Email FROM Students WHERE Email = ? AND Password = ?;',
                                         (username, password))
            email = cursor2.fetchone()
            # Information for CheckingInfo (Course names, course descriptions, professor contact info, course grades)
            # cursor3
            # checkinginfo
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = email
            session['username'] = account[0]
            session['studentinfo'] = account
            # Redirect to home page
            return redirect(url_for('home'))
            # return render_template('home.html', account=account)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('student.html', msg=msg)
# Student log in ------------------------------------------------->


# Staff log on ------------------------------------------------------->
@app.route('/stafflogin/', methods=['GET', 'POST'])
def loginstaff():
    # Output message
    msg = ''
    # Do "username" and "password" POST requests exist?
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT * FROM Professors WHERE Email = ? AND Password = ?;', (username, password))
        # Fetch one record and return result
        account = cursor.fetchall()
        # If account exists in accounts table in out database
        if account:
            # Information for EMAIL (session ID) only
            cursor2 = connection.execute('SELECT Email FROM Professors WHERE Email = ? AND Password = ?;',
                                         (username, password))
            email = cursor2.fetchone()
            # Information for CheckingInfo (Course names, course descriptions, professor contact info, course grades)
            # cursor3
            # Create session data so that we can access this data in other routes
            session['loggedin'] = True
            session['id'] = email
            session['username'] = account[0]
            # Redirect to home page
            return redirect(url_for('staffhome'))
            # return render_template('home.html', account=account)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('staff.html', msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return render_template('index.html')


# App route for navigating to "student" or "staff" web pages:
@app.route('/select', methods=['POST'])
def select():
    selected = request.form.get('selection')
    connection = sql.connect('database.db')
    if selected == 'Staff':
        return render_template('staff.html')
    if selected == 'Student':
        return render_template('student.html')
    else:
        return render_template('index.html')


# Student Home ------------------------------------------------------------------>
# http://localhost:5000/pythinlogin/home - this will be the student home page, only accessible for logged-in users
@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('student'))
# Student Home ------------------------------------------------------------------>


# Staff Home ------------------------------------------------------------------>
# http://localhost:5000/pythinlogin/home - this will be the student home page, only accessible for logged-in users
@app.route('/stafflogin/staffhome')
def staffhome():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('staffhome.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('staff'))


# Staff Home ------------------------------------------------------------------>


# Change student password -------------------------------------------------------------->
@app.route('/pythonlogin/password')
def password():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the student password change page
        return render_template('password.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# App route for password change:
@app.route('/passwordChange', methods=['POST', 'GET'])
def passwordchange():
    error = None
    if request.method == 'POST':
        result = valid_pass(request.form['newPassword'])
        if result:
            msg = 'Password changed successfully!'
            return render_template('password.html', error=error, result=result, msg=msg)
        else:
            error = 'invalid input name'
    return render_template('student.html', error=error)


# Check for valid password, insert into DB
# Function for SQL commands (new password)
def valid_pass(newPassword):
    connection = sql.connect('database.db')
    connection.execute('UPDATE Students SET Password = ? WHERE Email = ?', (newPassword, session['username'][0]))
    connection.commit()
    cursor = connection.execute('SELECT Password FROM Students;')
    return cursor.fetchall()
# Change student password -------------------------------------------------------------->


# Change staff password -------------------------------------------------------------->
@app.route('/stafflogin/staffpassword')
def staffpassword():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the password change page
        return render_template('staffpassword.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('loginStaff'))


# App route for password change:
@app.route('/passwordChangeStaff', methods=['POST', 'GET'])
def passwordchangestaff():
    error = None
    if request.method == 'POST':
        result = staff_valid_pass(request.form['newPassword'])
        if result:
            msg = 'Password changed successfully!'
            return render_template('staffpassword.html', error=error, result=result, msg=msg)
        else:
            error = 'invalid input name'
    return render_template('staff.html', error=error)


# Check for valid password, insert into DB
# Function for SQL commands (new password
def staff_valid_pass(newPassword):
    connection = sql.connect('database.db')
    connection.execute('UPDATE Professors SET Password = ? WHERE Email = ?', (newPassword, session['username'][0]))
    connection.commit()
    cursor = connection.execute('SELECT Password FROM Password;')
    return cursor.fetchall()
# Change staff password -------------------------------------------------------------->


# Create new post (Student)-------------------------------------------------------------->
@app.route('/pythonlogin/newpost')
def newpostroute():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('newpost.html', username=session['username'])
    # User is not loggedin redirect to logon page
    return redirect(url_for('index'))


# App route for new post:
@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    error = None
    msg = ''
    result = ''
    if request.method == 'POST':
        result = valid_post(request.form['courseid'], request.form['newpost'])
        if result:
            result = posting(request.form['courseid'], request.form['newpost'])
            msg = 'Posted successfully!'
            return render_template('newpost.html', error=error, result=result, msg=msg)
        else:
            msg = 'You are not enrolled in the course you specified. Be sure to provide the exact course ID.'
    return render_template('newpost.html', msg=msg, result=result)


# Check for valid post, insert into DB
# Function for SQL commands (new post validation)
def valid_post(courseid, newpost):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('SELECT * FROM Enrolls WHERE student_email=? AND course_id=?',
                                 (session['username'][0], courseid))
    return cursor1.fetchall()


# Function for SQL commands (past validation, posting)
def posting(courseid, newpost):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Posts (course_id, student_email, post_info) VALUES(?,?,?);',
                       (courseid, session['username'][0], newpost))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM Posts WHERE student_email=? AND course_id=?;',
                                 (session['username'][0], courseid))
    return cursor2.fetchall()
# Create Post (Student) -------------------------------------->


# Create new Comment (Student) --------------------------------------------------->
@app.route('/pythonlogin/newcomment')
def newcommentroute():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('newcomment.html', username=session['username'])
    # User is not loggedin redirect to logon page
    return redirect(url_for('index'))


# App route for new comment:
@app.route('/newcomment', methods=['POST', 'GET'])
def newcomment():
    error = None
    msg = ''
    result = ''
    result2 = ''
    result3 = ''
    if request.method == 'POST':
        result = valid_comment_course(request.form['courseid'], request.form['postid'], request.form['newcomment'])
        result2 = valid_comment_post(request.form['courseid'], request.form['postid'], request.form['newcomment'])
        if result and result2:
            result3 = posting_comment(request.form['courseid'], request.form['postid'], request.form['newcomment'])
            msg = 'Posted successfully!'
            return render_template('newcomment.html', error=error, result=result3, msg=msg)
        else:
            msg = 'Error while posting. Be sure to provide the exact course ID and Post ID.'
    return render_template('newcomment.html', msg=msg, result=result)


# Check for valid comment course, insert into DB
# Function for SQL commands (course validation)
def valid_comment_course(courseid, postid, newpost):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('SELECT * FROM Enrolls WHERE student_email=? AND course_id=?',
                                 (session['username'][0], courseid))
    return cursor1.fetchall()


# Check for valid post, insert into DB
# Function for SQL commands (new post validation)
def valid_comment_post(courseid, postid, newpost):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('SELECT * FROM Posts WHERE post_no=? AND course_id=?', (postid, courseid,))
    return cursor1.fetchall()


# Function for SQL commands (past validation, posting)
def posting_comment(courseid, postid, newpost):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Comments (course_id, post_no, student_email, comment_info) VALUES(?,?,?,?);',
                       (courseid, postid, session['username'][0], newpost))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM Comments WHERE student_email=? AND post_no=? AND course_id=?;',
                                 (session['username'][0], postid, courseid))
    return cursor2.fetchall()
# Create Comment (Student) -------------------------------------------------------------->


# STAFF
# Create new post (Staff) -------------------------------------------------------------->
# App route for new post:
@app.route('/staffnewpost', methods=['POST', 'GET'])
def staffnewpost():
    error = None
    msg = ''
    result = ''
    if request.method == 'POST':
        result = staff_valid_post(request.form['courseid'], request.form['newpost'])
        if result:
            result = staffposting(request.form['courseid'], request.form['newpost'])
            msg = 'Posted successfully!'
            return render_template('staffnewpost.html', error=error, result=result, msg=msg)
        else:
            msg = 'You are not a part of the course you specified. Be sure to provide the exact course ID.'
    return render_template('staffnewpost.html', msg=msg, result=result)


# Check for valid post, insert into DB
# Function for SQL commands (new post validation)
def staff_valid_post(courseid, newpost):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('SELECT * FROM '
                                    'Posts p, Prof_teaching_teams e, Sections s WHERE e.teaching_team_id=s.teaching_'
                                    'team_id AND s.course_id=p.course_id AND e.prof_email=?',
                                 (session['username'][0], courseid))
    return cursor1.fetchall()


# Function for SQL commands (past validation, posting)
def staffposting(courseid, newpost):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Posts (course_id, student_email, post_info) VALUES(?,?,?);',
                       (courseid, session['username'][0], newpost))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM Posts WHERE student_email=? AND course_id=?;',
                                 (session['username'][0], courseid))
    return cursor2.fetchall()
# Create Post (Staff) -------------------------------------->

# Create new comment (Staff)--------------------------------------------------->
@app.route('/stafflogin/newcomment')
def staffnewcommentroute():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('staffnewcomment.html', username=session['username'])
    # User is not loggedin redirect to logon page
    return redirect(url_for('index'))


# App route for new comment:
@app.route('/staffnewcomment', methods=['POST', 'GET'])
def staffnewcomment():
    error = None
    msg = ''
    result = ''
    result2 = ''
    result3 = ''
    if request.method == 'POST':
        result = staff_valid_comment_course(request.form['courseid'], request.form['postid'], request.form['newcomment'])
        result2 = staff_valid_comment_post(request.form['courseid'], request.form['postid'], request.form['newcomment'])
        if result and result2:
            result3 = staff_posting_comment(request.form['courseid'], request.form['postid'], request.form['newcomment'])
            msg = 'Posted successfully!'
            return render_template('staffnewcomment.html', error=error, result=result3, msg=msg)
        else:
            msg = 'Error while posting. Be sure to provide the exact course ID and Post ID.'
    return render_template('staffnewcomment.html', msg=msg, result=result)


# Check for valid comment course, insert into DB
# Function for SQL commands (course validation)
def staff_valid_comment_course(courseid, postid, newpost):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('SELECT * FROM '
                                 'Posts p, Prof_teaching_teams e, Sections s WHERE e.teaching_team_id=s.teaching_'
                                 'team_id AND s.course_id=p.course_id AND e.prof_email=?',
                                 (session['username'][0], courseid))
    return cursor1.fetchall()


# Check for valid post, insert into DB
# Function for SQL commands (new post validation)
def staff_valid_comment_post(courseid, postid, newpost):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('SELECT * FROM Posts WHERE post_no=? AND course_id=?', (postid, courseid,))
    return cursor1.fetchall()


# Function for SQL commands (past validation, posting)
def staff_posting_comment(courseid, postid, newpost):
    connection = sql.connect('database.db')
    connection.execute('INSERT INTO Comments (course_id, post_no, student_email, comment_info) VALUES(?,?,?,?);',
                       (courseid, postid, session['username'][0], newpost))
    connection.commit()
    cursor2 = connection.execute('SELECT * FROM Comments WHERE student_email=? AND post_no=? AND course_id=?;',
                                 (session['username'][0], postid, courseid))
    return cursor2.fetchall()
# Create Comment (Staff)-------------------------------------------------------------->
# STAFF


# Student Information: contains personal info and course info.
# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        email = session['id']
        # Account details: ------------------------------------>
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT * FROM Students WHERE Email = ?', (session['id']))
        # Fetch one record and return result
        result = cursor.fetchall()
        # Course details: ------------------------------------>
        # connection2 = sql.connect('database.db')
        cursor = connection.execute('SELECT DISTINCT e.course_id, e.section_no, c.course_name, c.course_description, '
                                    'p.Email, p.Office, h1.grade, ex.grades FROM Enrolls e, Courses c, Professors p, '
                                    'Homework_grades h1, Exam_grades ex, Students_TA st, Prof_teaching_teams ptt, '
                                    'Sections s WHERE e.student_email=? AND h1.student_email=? AND '
                                    'ex.student_email=? AND st.Course_1=c.course_id AND st.Course_1=e.course_id AND '
                                    'st.Course_1_Section=e.section_no AND st.Course_1=s.course_id AND '
                                    'st.Course_1_Section=s.sec_no AND s.teaching_team_id=ptt.teaching_team_id AND '
                                    'ptt.prof_email=p.Email AND h1.course_id=st.Course_1 AND '
                                    'h1.sec_no=st.Course_1_Section AND ex.course_id=st.Course_1 AND '
                                    'ex.sec_no=st.Course_1_Section;',
                                    (session['username'][0], session['username'][0], session['username'][0]))
        result2 = cursor.fetchall()
        # Show the profile page with info
        return render_template('profile.html', account=result, course=result2)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# Staff Information: contains personal staff information
# http://localhost:5000/pythinlogin/staffprofile - this will be the profile page, only accessible for loggedin users
@app.route('/stafflogin/staffprofile')
def staffprofile():
    # Check if user is loggedin
    if 'loggedin' in session:
        email = session['id']
        # Account details: ------------------------------------>
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT * FROM Professors WHERE Email = ?', (session['id']))
        # Fetch one record and return result
        result = cursor.fetchall()
        # Show the profile page with info
        return render_template('staffprofile.html', account=result)
    # User is not loggedin redirect to login page
    return redirect(url_for('loginstaff'))


# Student Forum View
# http://localhost:5000/pythinlogin/forum - this will be the profile page, only accessible for loggedin  STUDENT users
@app.route('/pythonlogin/forum')
def forum():
    # Check if user is loggedin
    if 'loggedin' in session:
        email = session['id']
        # Posts details: ------------------------------------>
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT DISTINCT p.course_id, p.student_email, p.post_info, p.post_no FROM Posts '
                                    'p, Enrolls e WHERE e.course_id=p.course_id AND e.student_email=?',
                                    (session['username'][0],))
        # Fetch one record and return result
        result = cursor.fetchall()
        # Comments details: --------------------------------->
        cursor = connection.execute('SELECT DISTINCT p.course_id, p.student_email, p.post_info, p.post_no, '
                                    'c.student_email, c.comment_info, c.comment_no FROM Posts p, Enrolls e, '
                                    'Comments c WHERE e.course_id=p.course_id AND e.student_email=? AND '
                                    'p.post_no=c.post_no', (session['username'][0],))
        result2 = cursor.fetchall()
        # Show the forum page with info
        return render_template('forum.html', posts=result, comments=result2)
    # User is not loggedin redirect to login page
    return redirect(url_for('index'))


# Staff Forum View
# http://localhost:5000/pythonlogin/forum - this will be the profile page, only accessible for loggedin STAFF users
@app.route('/stafflogin/staffforum')
def staffforum():
    # Check if user is loggedin
    if 'loggedin' in session:
        email = session['id']
        # Posts details: ------------------------------------>
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT DISTINCT p.course_id, p.student_email, p.post_info, p.post_no FROM '
                                    'Posts p, Prof_teaching_teams e, Sections s WHERE e.teaching_team_id=s.teaching_'
                                    'team_id AND s.course_id=p.course_id AND e.prof_email=?',
                                    (session['username'][0],))
        # Fetch one record and return result
        result = cursor.fetchall()
        # Comments details: --------------------------------->
        cursor = connection.execute(
            'SELECT DISTINCT p.course_id, p.student_email, p.post_info, p.post_no, c.student_email, c.comment_info, '
            'c.comment_no FROM Posts p, Prof_teaching_teams e, Sections s, Comments c WHERE e.teaching_team_'
            'id=s.teaching_team_id AND s.course_id=p.course_id AND e.prof_email=? AND p.post_no=c.post_no',
            (session['username'][0],))
        result2 = cursor.fetchall()
        # Show the forum page with info
        return render_template('staffforum.html', posts=result, comments=result2)
    # User is not loggedin redirect to login page
    return redirect(url_for('index'))


# ASSIGNMENTS STUDENTS
# http://localhost:5000/pythinlogin/assignments - this will be the profile page, only accessible for loggedin  STUDENT users
@app.route('/pythonlogin/assignments')
def assignments():
    # Check if user is loggedin
    if 'loggedin' in session:
        email = session['id']
        # Homeworks details: ------------------------------------>
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT DISTINCT h.course_id, h.sec_no, h.hw_no, h.hw_details, g.grade '
                                    'FROM Homeworks h, Homework_grades g WHERE g.student_email=? AND h.course_'
                                    'id=g.course_id AND h.sec_no=g.sec_no AND h.hw_no=g.hw_no',
                                    (session['username'][0],))
        # Fetch one record and return result
        result = cursor.fetchall()
        # Exams details: --------------------------------->
        cursor = connection.execute('SELECT DISTINCT h.course_id, h.sec_no, h.exam_no, h.exam_details, g.grades '
                                    'FROM Exams h, Exam_grades g WHERE g.student_email=? AND '
                                    'h.course_id=g.course_id AND h.sec_no=g.sec_no AND h.exam_no=g.exam_no',
                                    (session['username'][0],))
        result2 = cursor.fetchall()
        # Show the assignment page with info
        return render_template('assignments.html', homeworks=result, exams=result2)
    # User is not loggedin redirect to login page
    return redirect(url_for('index'))
# ASSIGNMENTS STUDENTS


# ASSIGNMENTS STAFF  ------------------------------------------------------------------>
# http://localhost:5000/stafflogin/assignments - this will be the staff assignments page, only accessible for logged-in users
@app.route('/stafflogin/assignments')
def staffassignments():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the assignments page
        # Homeworks details: ------------------------------------>
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT DISTINCT h.course_id, h.sec_no, h.hw_no, h.hw_details FROM Homeworks '
                                    'h, Sections s, Prof_teaching_teams t WHERE t.prof_email=? AND h.course_'
                                    'id=s.course_id AND h.sec_no=s.sec_no AND t.teaching_team_id=s.teaching_team_id;',
                                    (session['username'][0],))
        # Fetch one record and return result
        result = cursor.fetchall()
        # Exams details: --------------------------------->
        cursor = connection.execute('SELECT DISTINCT h.course_id, h.sec_no, h.exam_no, h.exam_details FROM Exams h, '
                                    ' Sections s, Prof_teaching_teams t WHERE t.prof_email=? AND '
                                    ' h.course_id=s.course_id AND h.sec_no=s.sec_no AND '
                                    't.teaching_team_id=s.teaching_team_id;',
                                    (session['username'][0],))
        result2 = cursor.fetchall()
        return render_template('staffassignments.html', username=session['username'], homeworks=result, exams=result2)
    # User is not loggedin redirect to login page
    return redirect(url_for('index'))


# Staff View Assignment --------------------------------------------------->
@app.route('/stafflogin/staffviewassignment')
def routestaffviewassignment():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        a_type = request.form['a_type']
        a_no = request.form['a_no']
        sec_no = request.form['sec_no']
        return render_template('staffviewassignment.html', username=session['username'], a_type=a_type,
                               a_no=a_no, sec_no=sec_no)
    # User is not loggedin redirect to logon page
    return redirect(url_for('index'))


# App route for viewing assignments:
@app.route('/staffviewassignment', methods=['POST', 'GET'])
def staffviewassignment():
    error = None
    if request.method == 'POST':
        a_type = request.form['a_type']
        a_no = request.form['a_no']
        course_id = request.form['course_id']
        sec_no = request.form['sec_no']
        if a_type == 'homework':
            result = homework_valid_view_query(a_type, a_no, course_id, sec_no)
            return render_template('staffviewassignment.html', result=result, a_type=a_type, a_no=a_no, course_id=course_id, sec_no=sec_no)
        elif a_type == 'exam':
            result = exam_valid_view_query(a_type, a_no, course_id, sec_no)
            return render_template('staffviewassignment.html', result=result, a_type=a_type, a_no=a_no,
                                   course_id=course_id, sec_no=sec_no)
        else:
            msg = 'Error.'
    return render_template('staffviewassignment.html', msg=msg)


def homework_valid_view_query(a_type, a_no, course_id, sec_no):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('SELECT DISTINCT g.student_email, g.grade FROM Homework_grades '
                                 'g WHERE g.course_id=? AND g.sec_no=? AND g.hw_no=?',
                                 (course_id, sec_no, a_no))
    return cursor1.fetchall()


def exam_valid_view_query(a_type, a_no, course_id, sec_no):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('SELECT DISTINCT g.student_email, g.grades FROM Exam_grades '
                                 'g WHERE g.course_id=? AND g.sec_no=? AND g.exam_no=?',
                                 (course_id, sec_no, a_no))
    return cursor1.fetchall()
# Staff View Assignments END ----------->


# Staff ADD Assignments ---------------->
@app.route('/stafflogin/staffaddassignment')
def routestaffaddassignment():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        a_type = request.form['a_type']
        a_no = request.form['a_no']
        sec_no = request.form['sec_no']
        return render_template('staffaddassignment.html', username=session['username'], a_type=a_type,
                               a_no=a_no, sec_no=sec_no)
    # User is not loggedin redirect to logon page
    return redirect(url_for('index'))


# App route for viewing assignments:
@app.route('/staffaddassignment', methods=['POST', 'GET'])
def staffaddassignment():
    error = None
    if request.method == 'POST':
        course_id = request.form['course_id']
        sec_no = request.form['sec_no']
        a_type = request.form['a_type']
        a_no = request.form['a_no']
        a_desc = request.form['a_desc']
        connection = sql.connect('database.db')
        cursor = connection.execute('SELECT DISTINCT h.course_id, h.sec_no, h.hw_no, h.hw_details FROM Homeworks '
                                    'h, Sections s, Prof_teaching_teams t WHERE t.prof_email=? AND h.course_'
                                    'id=s.course_id AND h.sec_no=s.sec_no AND t.teaching_team_id=s.teaching_team_id;',
                                    (session['username'][0],))
        # Fetch one record and return result
        result1 = cursor.fetchall()
        # Exams details: --------------------------------->
        cursor = connection.execute('SELECT DISTINCT h.course_id, h.sec_no, h.exam_no, h.exam_details FROM Exams h, '
                                    ' Sections s, Prof_teaching_teams t WHERE t.prof_email=? AND '
                                    ' h.course_id=s.course_id AND h.sec_no=s.sec_no AND '
                                    't.teaching_team_id=s.teaching_team_id;',
                                    (session['username'][0],))
        result2 = cursor.fetchall()
        if a_type == 'homework':
            result = homework_valid_add_query(course_id, sec_no, a_no, a_desc)
            return render_template('staffaddassignment.html', homeworks=result1, exams=result2, result=result, a_type=a_type, a_no=a_no, course_id=course_id, sec_no=sec_no)
        elif a_type == 'exam':
            result = exam_valid_add_query(course_id, sec_no, a_no, a_desc)
            return render_template('staffaddassignment.html', homeworks=result1, exams=result2, result=result, a_type=a_type, a_no=a_no, course_id=course_id, sec_no=sec_no)
        else:
            msg = 'Error.'
    return render_template('staffaddassignment.html', msg=msg)


def homework_valid_add_query(course_id, sec_no, a_no, a_desc):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('INSERT INTO Homeworks (course_id, sec_no, hw_no, hw_details) VALUES(?,?,?,?);',
                                 (course_id, sec_no, a_no, a_desc))
    connection.commit()
    return cursor1.fetchall()


def exam_valid_add_query(course_id, sec_no, a_no, a_desc):
    connection = sql.connect('database.db')
    cursor1 = connection.execute('INSERT INTO Homeworks (course_id, sec_no, exam_no, exam_details) VALUES(?,?,?,?);',
                                 (course_id, sec_no, a_no, a_desc))
    connection.commit()
    return cursor1.fetchall()
# ASSIGNMENTS STAFF  ------------------------------------------------------------------>


if __name__ == "__main__":
    app.run()
