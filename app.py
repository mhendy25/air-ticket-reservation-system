from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password='',
                               database='_final_db')

@app.route('/')
def index():
	# checkout the session first
	if(session):
		print('session is:', )
		if session['type'] == 'Customer':
			return render_template('customerHome.html')
		elif session['type'] == 'Booking Agent':
			return render_template('agentHome.html')
		elif session['type'] == 'Airline Staff':
			return render_template('staffHome.html')
	else:
		print('no session!')
		return render_template('searchPage.html', error = None)


@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	logtype = request.form['logtype']
	username = request.form['username']
	password = request.form['password']
	
	if logtype == 'Customer':
		query = "SELECT * FROM customer WHERE email = '{}' and password = '{}'"
		query1 = "SELECT * FROM customer WHERE email = '{}'"
	elif logtype == 'Agent':
		query = "SELECT * FROM agent WHERE email = '{}' and password = '{}'"
		query1 = "SELECT * FROM agent WHERE email = '{}'"
	elif logtype == 'Airline Staff':
		query = "SELECT * FROM airline_staff WHERE username = '{}' and password = '{}'"
		query1 = "SELECT * FROM airline_staff WHERE username = '{}'"
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	cursor.execute(query.format(username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	cursor1 = conn.cursor()
	cursor1.execute(query1.format(username))
	data1 = cursor1.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	cursor1.close()

	error = None
	if(data1):
		#creates a session for the the user
		#session is a built in
		if(data):
			session['username'] = username
			session['type'] = logtype
			if(logtype == 'Customer'):
				return render_template('customerHome.html')
			elif(logtype == 'Agent'):
				return render_template('agentHome.html')
			elif(logtype == 'Airline Staff'):
				query2 = "SELECT permission_id FROM airline_staff WHERE username = '{}'".format(username)
				query3 = "SELECT name_airline FROM airline_staff WHERE username = '{}'".format(username)
				cursor2 = conn.cursor()
				cursor2.execute(query2)
				data2 = cursor2.fetchone()
				cursor3 = conn.cursor()
				cursor3.execute(query3)
				data3 = cursor3.fetchone()
				cursor2.close()
				cursor3.close()
				session['permission'] = data2[0]
				print(data2[0])
				session['airline'] = data3[0]
				print(data)
				return render_template('staffHome.html')
		else:
			error = "Incorrect password"
			return render_template('login.html', error=error)
	else:
		#returns an error message to the html page
		error = 'No username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	registertype = request.form['user']
	if registertype == 'Customer':
		return render_template('registerCus.html')
	elif registertype == 'Booking Agent':
		return render_template('registerAgt.html')
	elif registertype == 'Airline Staff':
		return render_template('registerStf.html')


@app.route('/registerCus', methods=['GET', 'POST'])
def registerCus():
	username = request.form['username']
	password = request.form['password']
	name = request.form['name']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']

	query = "SELECT * FROM customer WHERE email = '{}'"
	cursor = conn.cursor()
	cursor.execute(query.format(username))
	data = cursor.fetchone()
	error = None

	if(data):
		error = "This user already exists"
		return render_template('registerCus.html', error = error)
	else:
		ins = "INSERT INTO customer VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',\
		 '{}', '{}', '{}', '{}')"

	cursor.execute(ins.format(username, name, password ,building_number, street, city, state, phone_number, passport_number\
		, passport_expiration, passport_country, date_of_birth))
	conn.commit()
	cursor.close()
	return render_template('index.html')

@app.route('/registerAgt', methods=['GET', 'POST'])
def registerAgt():
	username = request.form['username']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

	query = "SELECT * FROM agent WHERE email = '{}'"
	cursor = conn.cursor()
	cursor.execute(query.format(username))
	data = cursor.fetchone()
	error = None

	if(data):
		error = "This user already exists"
		return render_template('registerAgt.html', error = error)
	else:
		ins = "INSERT INTO agent VALUES('{}', '{}', '{}')"

	cursor.execute(ins.format(username, password , booking_agent_id))
	conn.commit()
	cursor.close()
	return render_template('index.html')
	
@app.route('/registerStf', methods=['GET', 'POST'])
def registerStf():
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	#permission_id = request.form['permission_id']
	permission_id = 4
	name_airline = request.form['name_airline']
	
	query = "SELECT * FROM airline_staff WHERE username = '{}'"
	cursor = conn.cursor()
	cursor.execute(query.format(username))
	data = cursor.fetchone()
	error = None

	if(data):
		error = "This user already exists"
		return render_template('registerStf.html', error = error)
	else:
		query = "SELECT * FROM airline WHERE name = '{}'"
		cursor1 = conn.cursor()
		cursor1.execute(query.format(name_airline))
		data1 = cursor1.fetchone()
		
		error = None
		if(data1 == None):
			error = "The airline does not exists"
			return render_template('registerStf.html', error = error)
		ins = "INSERT INTO airline_staff VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')"
		
	cursor.execute(ins.format(username, password ,first_name, last_name, date_of_birth, permission_id, name_airline))
	conn.commit()
	cursor.close()
	return render_template('index.html')

@app.route('/search', methods = ['Get', 'POST'])
def search():
	dep = request.form['dep_city_port']
	des = request.form['des_city_port']
	date = request.form['date']
	query = "SELECT flight_num, depart_time, arrive_time FROM flight f JOIN airport a on f.depart_airport = a.name JOIN\
	 airport b on f.arrive_airport = b.name WHERE (f.depart_airport = '{}' OR a.name = '{}' ) AND\
	 (f.arrive_airport = '{}' OR b.name = '{}') AND depart_time LIKE '{}%' AND status = 'upcoming'"
	cursor = conn.cursor()
	cursor.execute(query.format(dep,dep,des,des,date))
	data = cursor.fetchall()
	error = None
	cursor.close()
	if(data):
		return render_template('searchPage.html', result = data, error = None)
	else:
		error = "No result found."
		return render_template('searchPage.html', error = error)


	
@app.route('/viewCus', methods = ['GET', 'POST'])
def viewCus():
	action = request.form['view_my_flight']
	username = session['username']
	if action == 'View My Flight':
		query = 'SELECT flight_num, depart_time, arrive_time FROM ticket NATURAL JOIN flight WHERE customer_email = "{}"'
		cursor = conn.cursor()
		cursor.execute(query.format(username))
		data = cursor.fetchall()
		cursor.close()
		return render_template('customerHome.html', result = data)
	
@app.route('/searchCus', methods = ['GET', 'POST'])
def searchCus():
	dep = request.form['dep_city_port']
	des = request.form['des_city_port']
	date = request.form['date']
	query = "SELECT flight_num, depart_time, arrive_time FROM flight f JOIN airport a on f.depart_airport = a.name JOIN\
	 airport b on f.arrive_airport = b.name WHERE (f.depart_airport = '{}' OR a.name = '{}' ) AND\
	 (f.arrive_airport = '{}' OR b.name = '{}') AND depart_time LIKE '{}%'" 
	cursor = conn.cursor()
	cursor.execute(query.format(dep,dep,des,des,date))
	data = cursor.fetchall()
	error = None
	cursor.close()
	if(data):
		return render_template('customerHome.html', result1 = data, error = None)
	else:
		error = "No result found."
		return render_template('customerHome.html', error = error)

@app.route('/purticketCus', methods = ['GET', 'POST'])
def purticketCus():
	flight_num = request.form['ticket']
	username = session['username']
	cursor = conn.cursor()
	## for special customers
	query0 = "SELECT name_airline, count(*) from ticket natural join flight where customer_email = '{}' group by name_airline "
	cursor.execute(query0.format(username))
	data0 = cursor.fetchall()
	cursor.close()
	is_special = None 
	if data0:
		print(data0)
		if data0[0][1]>=3:
			is_special = True
	cursor = conn.cursor()
	query = "INSERT INTO ticket(flight_num, customer_email, agent_email) VALUES('{}', '{}', Null)"
	cursor.execute(query.format(flight_num, username))
	conn.commit()
	cursor.close()
	return render_template('customerHome.html', banner = "Purchase Success", is_special = is_special)

@app.route('/chartCus', methods = ['GET', 'POST'])
def chartCus():
	value = request.form['view']
	username = session['username']
	query = "SELECT month(depart_time) AS month, sum(price) AS monthly_spent FROM flight JOIN \
	ticket on ticket.flight_num = flight.flight_num WHERE customer_email = '{}' AND DATE(depart_time) >= '2023-01-01' AND DATE(depart_time) <='2023-12-30' \
	GROUP BY month(depart_time)"
	query1 = "SELECT sum(price) AS spent FROM flight  JOIN \
	ticket on ticket.flight_num = flight.flight_num WHERE customer_email = '{}' AND DATE(depart_time) >= '2023-01-01' AND DATE(depart_time) <= '2023-12-30'"
	cursor = conn.cursor()
	cursor.execute(query.format(username))
	data = cursor.fetchall()
	cursor.close()
	cursor1 = conn.cursor()
	cursor1.execute(query1.format(username))
	data1 = cursor1.fetchone()
	cursor1.close()
	month = [i[0] for i in data]
	spent = [j[1] for j in data]
	height = ["height:" + str(k[1]/10) + "%" for k in data]
	length = len(month)
	allyear = data1[0]
	return render_template('chartCus.html', month = month, spent = spent, height = height, length = length, allyear = allyear, nonemp = 1)

@app.route('/viewTopCus', methods = ['GET', 'POST'])
def viewTopCus():
	username = session['username']
	query1 = "SELECT t.customer_email, c.name, count(t.ticket_id) FROM ticket t JOIN customer c ON c.email = t.customer_email \
	WHERE t.agent_email = '{}' GROUP BY t.customer_email, c.name"
	query2 = "SELECT t.customer_email, c.name, sum(f.price) FROM (flight f NATURAL JOIN ticket t) JOIN customer c ON c.email = t.customer_email \
	WHERE t.agent_email = '{}' GROUP BY t.customer_email, c.name"

	cursor = conn.cursor()
	cursor.execute(query1.format(username))
	data = cursor.fetchall()
	cursor.close()
	cursor1 = conn.cursor()
	cursor1.execute(query2.format(username))
	data1 = cursor1.fetchall()
	cursor1.close()
	return render_template('agentHome.html', result_cus_num = data, result_cus_amt = data1)

@app.route('/chartCusDate', methods = ['GET', 'POST'])
def chartCusDate():
	start = request.form['start']
	end = request.form['end']
	username = session['username']
	query = "SELECT month(depart_time) AS month, sum(price) AS monthly_spent FROM flight NATURAL JOIN \
	ticket WHERE customer_email = '{}' AND DATE(depart_time) >= '{}' AND DATE(depart_time) <= '{}' \
	GROUP BY month(depart_time)"
	cursor = conn.cursor()
	cursor.execute(query.format(username, start, end))
	data = cursor.fetchall()
	cursor.close()
	if(data):
		month = [i[0] for i in data]
		spent = [j[1] for j in data]
		height = ["height:" + str(k[1]/10) + "%" for k in data]
		length = len(month)
		return render_template('chartCus.html', month = month, spent = spent, height = height, length = length, nonemp = 1)
	else:
		return render_template('chartCus.html', error = "You have not spend anything in these days")

@app.route('/logoutCus')
def logoutCus():
	session.clear()
	return redirect('/')

@app.route('/viewAgt', methods = ['GET', 'POST'])
def viewAgt():
	action = request.form['view_my_flight']
	username = session['username']
	if action == 'View My Flight':
		query = 'SELECT flight_num, depart_time, arrive_time FROM ticket NATURAL JOIN flight WHERE agent_email = "{}"'
		cursor = conn.cursor()
		cursor.execute(query.format(username))
		data = cursor.fetchall()
		cursor.close()
		return render_template('agentHome.html', result = data)
	
@app.route('/searchAgt', methods = ['GET', 'POST'])
def searchAgt():
	dep = request.form['dep_city_port']
	des = request.form['des_city_port']
	date = request.form['date']
	username = session['username']
	query = "SELECT flight_num, depart_time, arrive_time, name_airline FROM flight f JOIN airport a on f.depart_airport = a.name JOIN\
	 airport b on f.arrive_airport = b.name WHERE (f.depart_airport = '{}' OR a.name = '{}' ) AND\
	 (f.arrive_airport = '{}' OR b.name = '{}') AND depart_time LIKE '{}%' AND status = 'upcoming'" 
	cursor = conn.cursor()
	cursor.execute(query.format(dep,dep,des,des,date))
	data = cursor.fetchall()
	error = None
	cursor.close()
	query2 = "SELECT name FROM works_for WHERE email = '{}' " 
	cursor = conn.cursor()
	cursor.execute(query2.format(username))
	data2 = cursor.fetchall()
	cursor.close()
	data2 = [i[0] for i in data2]
	if(data):
		# airline = [i[0] for i in data2]
		return render_template('agentHome.html', result1 = data, error = None, airline = data2)
	else:
		error = "No result found."
		return render_template('agentHome.html', error = error)

@app.route('/purticketAgt', methods = ['GET', 'POST'])
def purticketAgt():
	flight_num = request.form['ticket']
	cus_email = request.form['cus_email']
	username = session['username']
	query1 = "SELECT email FROM customer WHERE email = '{}'"
	cursor = conn.cursor()
	cursor.execute(query1.format(cus_email))
	data = cursor.fetchone()
	if (data):
		query2 = "INSERT INTO ticket(flight_num, customer_email, agent_email) VALUES('{}', '{}', '{}')"
		cursor = conn.cursor()
		cursor.execute(query2.format(flight_num, cus_email, username))
		conn.commit()
		cursor.close()
		return render_template('agentHome.html', banner = "Purchase Success")
	else:
		banner = 'Customer email does not exist.'
		cursor.close()
		return render_template('agentHome.html', banner = banner)

@app.route('/view_comm', methods = ['GET', 'POST'])
def view_comm():
	start = request.form['start_date']
	end = request.form['end_date']
	username = session['username']
	if len(start)==0:
		query = "SELECT ifnull(sum(price), 0), ifnull(avg(price), 0), count(*) FROM ticket left outer JOIN flight on flight.flight_num = ticket.flight_num  where\
		date(depart_time)<='2023-05-07' AND date(depart_time)>='2023-04-06' and agent_email = '{}' " 
		cursor = conn.cursor()
		cursor.execute(query.format(username))
		data = cursor.fetchall()
		error = None
		cursor.close()
	else:
		query = "SELECT ifnull(sum(price), 0), ifnull(avg(price), 0), count(*) FROM ticket left outer JOIN flight on flight.flight_num = ticket.flight_num  where\
		date(depart_time) >='{}' and date(arrive_time)<='{}' and agent_email = '{}' " 
		cursor = conn.cursor()
		cursor.execute(query.format(start, end, username))
		data = cursor.fetchall()
		print(data)
		error = None
		cursor.close()
	if(data):
		
		return render_template('agentHome.html', result1 = data, error = None)
	else:
		error = "No result found."
		return render_template('agentHome.html', error = error)
	

@app.route('/logoutAgt')
def logoutAgt():
	session.clear()
	return redirect('/')

@app.route('/viewStf', methods = ['GET', 'POST'])
def viewStf():
	action = request.form['view_my_flight']
	username = session['username']
	airline = session['airline']
	if action == 'View My Flight':
		query = 'SELECT flight_num, depart_time, arrive_time FROM flight WHERE name_airline = "{}"'
		cursor = conn.cursor()
		cursor.execute(query.format(airline))
		data = cursor.fetchall()
		cursor.close()
		return render_template('staffHome.html', result = data)

@app.route('/viewFlight', methods = ['GET', 'POST'])
def viewFlight():
	flight_num = request.form['ticket']
	confirm = request.form['confirm']
	query = "SELECT customer_email, name FROM ticket join customer ON customer_email = email WHERE flight_num = '{}'"
	cursor = conn.cursor()
	cursor.execute(query.format(flight_num))
	result = cursor.fetchall()
	conn.commit()
	cursor.close()
	return render_template('staffHome.html', result1 = result)

@app.route('/tocreate', methods = ['GET', 'POST'])
def tocreate():
	permission = session['permission']
	if(permission == 1 or permission == 3):
		return redirect(url_for('showTable'))
	else:
		return render_template('staffHome.html', error = "You are not Admin")

@app.route('/showTable', methods = ['GET', 'POST'])
def showTable():
	username = session['username']
	name_airline = session['airline']
	query = "SELECT flight_num, depart_time, arrive_time FROM flight WHERE name_airline = '{}' AND\
	 DATE(depart_time) >= '2023-01-01' "
	cursor = conn.cursor()
	cursor.execute(query.format(name_airline))
	data = cursor.fetchall()
	cursor.close()
	
	query_plane = "SELECT id FROM airplane WHERE name_airline = '{}'"
	cursor1 = conn.cursor()
	cursor1.execute(query_plane.format(name_airline))
	data1 = cursor1.fetchall()
	cursor1.close()

	query_airport = "SELECT name FROM airport"
	cursor2 = conn.cursor()
	cursor2.execute(query_airport)
	data2 = cursor2.fetchall()
	cursor2.close()
	return render_template('addFlightAdmin.html', result = data, result_plane = data1, result_port = data2)


@app.route('/addFlightAdmin', methods = ['Get', 'POST'])
def addFlightAdmin():
	username = session['username']
	name_airline = session['airline']
	depart_time = request.form['depart_time']
	arrive_time = request.form['arrive_time']
	price = request.form['price']
	status = request.form['status']
	plane_id = request.form['plane_id']
	depart_airport = request.form['depart_airport']
	arrive_airport = request.form['arrive_airport']

	query0 = "SELECT flight_num FROM flight ORDER BY flight_num DESC"
	cursor0 = conn.cursor(buffered=True)
	cursor0.execute(query0)
	flight_num = cursor0.fetchone()[0]
	cursor0.close()
	flight_num = str(int(flight_num) + 1)

	query = "INSERT INTO flight VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
	cursor = conn.cursor()
	cursor.execute(query.format(flight_num, depart_time, arrive_time, price, status, name_airline, plane_id, depart_airport, arrive_airport))
	conn.commit()
	cursor.close()

	return render_template('addFlightAdmin.html', banner = 'Success')



@app.route('/toupdate', methods = ['GET', 'POST'])
def toupdate():
	permission = session['permission']
	if permission == 2: #only allow "operators"
		return redirect(url_for('showFlight'))
	else:
		return render_template('staffHome.html', error = "You are not Operator")

@app.route('/showFlight', methods = ['GET', 'POST'])
def showFlight():
	username = session['username']
	name_airline = session['airline']
	query = "SELECT * FROM flight WHERE name_airline = '{}'"
	cursor = conn.cursor()
	cursor.execute(query.format(name_airline))
	data = cursor.fetchall()
	cursor.close()
	return render_template('updateFlight.html', result = data)

@app.route('/updateFlight', methods = ['GET', 'POST'])
def updateFlight():
	flight_num = request.form['change']
	new_status = request.form['status']
	query = "UPDATE flight SET status = '{}' WHERE flight_num = '{}'"
	cursor = conn.cursor()
	cursor.execute(query.format(new_status, flight_num))
	conn.commit()
	cursor.close()
	return render_template('updateFlight.html', banner = 'Success')

@app.route('/toAddPlane', methods = ['GET', 'POST'])
def toAddPlane():
	permission = session['permission']
	if(permission == 1 or permission == 3):
		return render_template('addPlane.html')
	else:
		return render_template('staffHome.html', error = "You are not Admin")

@app.route('/addPlaneAdmin', methods = ['Get', 'POST'])
def addPlaneAdmin():
	username = session['username']
	name_airline = session['airline']
	plane_id = request.form['plane_id']
	query0 = "SELECT id FROM airplane WHERE id = '{}' AND name_airline = '{}'"
	cursor0 = conn.cursor()
	cursor0.execute(query0.format(plane_id, name_airline))
	data0 = cursor0.fetchone()
	cursor0.close()
	if (data0):
		return render_template('addPlane.html', banner = 'Plane ID already exists!')
	query = "INSERT INTO airplane VALUES('{}', '{}')"
	cursor = conn.cursor()
	cursor.execute(query.format(plane_id, name_airline))
	conn.commit()
	cursor.close()

	query1 = "SELECT * FROM airplane WHERE name_airline = '{}'"
	cursor1 = conn.cursor()
	cursor1.execute(query1.format(name_airline))
	data1 = cursor1.fetchall()
	cursor.close()

	return render_template('addPlane.html', result = data1, banner = 'Success')

@app.route('/toAddAirport', methods = ['GET', 'POST'])
def toAddAirport():
	permission = session['permission']
	if(permission == 1 or permission == 3):
		return render_template('addAirport.html')
	else:
		return render_template('staffHome.html', error = "You are not Admin")

@app.route('/addAirportAdmin', methods = ['GET', 'POST'])
def addAirportAdmin():
	username = session['username']
	airport = request.form['airport']
	city = request.form['city']
	query0 = "SELECT name FROM airport WHERE name = '{}' AND city = '{}'"
	cursor0 = conn.cursor()
	cursor0.execute(query0.format(airport, city))
	data0 = cursor0.fetchone()
	cursor0.close()
	if (data0):
		return render_template('addAirport.html', banner = 'Airport already exists!')
	query = "INSERT INTO airport VALUES('{}', '{}')"
	cursor = conn.cursor()
	cursor.execute(query.format(airport, city))
	conn.commit()
	cursor.close()

	query1 = "SELECT * FROM airport"
	cursor1 = conn.cursor()
	cursor1.execute(query1)
	data1 = cursor1.fetchall()
	cursor.close()

	return render_template('addAirport.html', result = data1, banner = 'Success')

@app.route('/viewAgents', methods = ['GET', 'POST'])
def viewAgents():
	username = session['username']
	name_airline = session['airline']
	query1 = "SELECT t.agent_email, a.booking_agent_id FROM (ticket t JOIN agent a ON t.agent_email = a.email) \
	JOIN flight f USING(flight_num) WHERE f.name_airline = '{}'  \
	GROUP BY t.agent_email ORDER BY count(t.ticket_id) DESC LIMIT 5"
	query2 = "SELECT t.agent_email, a.booking_agent_id FROM (ticket t JOIN agent a ON t.agent_email = a.email) \
	JOIN flight f USING(flight_num) WHERE f.name_airline = '{}'  \
	GROUP BY t.agent_email ORDER BY count(t.ticket_id) DESC LIMIT 5"
	query3 = "SELECT t.agent_email, a.booking_agent_id FROM (ticket t JOIN agent a ON t.agent_email = a.email) \
	JOIN flight f USING(flight_num) WHERE f.name_airline = '{}'  \
	GROUP BY t.agent_email ORDER BY sum(f.price) DESC LIMIT 5"
	cursor1 = conn.cursor()
	cursor1.execute(query1.format(name_airline))
	data1 = cursor1.fetchall()
	cursor1.close()
	cursor2 = conn.cursor()
	cursor2.execute(query2.format(name_airline))
	data2 = cursor2.fetchall()
	cursor2.close()
	cursor3 = conn.cursor()
	cursor3.execute(query3.format(name_airline))
	data3 = cursor3.fetchall()
	cursor3.close()
	return render_template('staffHome.html', result1 = data1, result2 = data2, result3 = data3)

	
@app.route('/viewFreqCus', methods = ['GET', 'POST'])
def viewFreqCus():
	name_airline = session['airline']
	query1 = "SELECT c.email, c.name FROM flight f JOIN ticket t using(flight_num) join customer c on c.email = t.customer_email\
			  WHERE f.name_airline = '{}'  GROUP BY t.customer_email ORDER BY count(t.ticket_id) DESC LIMIT 1 "
	cursor1 = conn.cursor()
	cursor1.execute(query1.format(name_airline))
	data1 = cursor1.fetchone()
	cursor1.close()
	query2 = "SELECT f.flight_num, f.depart_time, f.arrive_time, f.price, f.plane_id, f.depart_airport, f.arrive_airport \
	FROM flight f JOIN ticket t using(flight_num) WHERE t.customer_email = '{}' AND f.name_airline = '{}'"
	cursor2 = conn.cursor()
	cursor2.execute(query2.format(data1[0], name_airline))
	data2 = cursor2.fetchall()
	cursor2.close()
	return render_template('staffHome.html', result_cus = data1, result_fli = data2)

@app.route('/toReport', methods = ['GET', 'POST'])
def toReport():
	return render_template('ticketReports.html')

@app.route('/ticketReports', methods = ['GET', 'POST'])
def ticketReports():
	start = request.form['start']
	end = request.form['end']
	airline = session['airline']
	query = "SELECT month(depart_time) AS month, count(ticket_id) AS monthly_sold FROM flight right outer JOIN \
	ticket on flight.flight_num = ticket.flight_num WHERE name_airline = '{}' AND DATE(depart_time) >= '{}' AND DATE(arrive_time) <= '{}' \
	GROUP BY month(depart_time)"
	cursor = conn.cursor()
	cursor.execute(query.format(airline, start, end))
	data = cursor.fetchall()
	cursor.close()
	if(data):
		month = [i[0] for i in data]
		spent = [j[1] for j in data]
		height = ["height:" + str(k[1]*10) + "%" for k in data]
		length = len(month)
		return render_template('ticketReports.html', month = month, spent = spent, height = height, length = length, nonemp = 1)
	else:
		return render_template('ticketReports.html', error = "No ticket sold in these days")

@app.route('/toRevenueMonth', methods = ['GET', 'POST'])
def toRevenueMonth():
	return redirect(url_for('revenueComparisonMonth'))

@app.route('/revenueComparisonMonth')
def revenueComparisonMonth():
	name_airline = session['airline']
	query1 = "SELECT ifnull(sum(price), 0) FROM ticket left outer JOIN flight on ticket.flight_num = flight.flight_num WHERE agent_email is not NULL AND\
	DATE(depart_time) >= '2023-01-01' AND DATE(depart_time) <= '2023-06-01' "

	query2 = "SELECT ifnull(sum(price), 0) FROM ticket left outer JOIN flight on ticket.flight_num = flight.flight_num WHERE agent_email is  NULL AND\
	DATE(depart_time) >= '2023-01-01' AND DATE(depart_time) <= '2023-06-01' "
	cursor1 = conn.cursor()
	cursor1.execute(query1.format(name_airline))
	data1 = cursor1.fetchone()[0]
	cursor1.close()
	cursor2 = conn.cursor()
	cursor2.execute(query2.format(name_airline))
	data2 = cursor2.fetchone()[0]
	cursor2.close()
	print(data1)
	print(data2)
	if data1 + data2 != 0:
		indirect1 = data1/(data1+data2) * 100
		print(indirect1)
		direct1 = 100 - indirect1
	else:
		indirect1 = 0
		direct1 = 0
	

	return render_template('revenueComparisonMonth.html', indirect1 = indirect1, direct1 = direct1, \
	data1 = data1, data2 = data2, error = str(data1)+','+str(data2))

@app.route('/toRevenueYear', methods = ['GET', 'POST'])
def toRevenueYear():
	return redirect(url_for('revenueComparisonYear'))

@app.route('/revenueComparisonYear')
def revenueComparisonYear():
	name_airline = session['airline']
	query3 = "SELECT ifnull(sum(price), 0) FROM ticket left outer JOIN flight on ticket.flight_num = flight.flight_num WHERE agent_email is not NULL AND\
	DATE(depart_time) >= '2023-01-01' AND DATE(depart_time) <= '2023-06-01' "

	query4 = "SELECT ifnull(sum(price), 0) FROM ticket left outer JOIN flight on ticket.flight_num = flight.flight_num WHERE agent_email is  NULL AND\
	DATE(depart_time) >= '2023-01-01' AND DATE(depart_time) <= '2023-06-01' "
	cursor3 = conn.cursor()
	cursor3.execute(query3.format(name_airline))
	data3 = cursor3.fetchone()[0]
	cursor3.close()
	cursor4 = conn.cursor()
	cursor4.execute(query4.format(name_airline))
	data4 = cursor4.fetchone()[0]
	cursor4.close()
	if data3 + data4 != 0:
		indirect2 = data3/(data3+data4) * 100
		direct2 = 100 - indirect2
	else:
		indirect2 = 0
		direct2 = 0
	return render_template('revenueComparisonYear.html', indirect2 = indirect2, direct2 = direct2, data3 = data3, data4 = data4, \
	error = str(data3)+',' + str(data4))


@app.route('/viewReports', methods = ['GET', 'POST'])
def viewReports():
	username = session['username']
	name_airline = session['airline']
	query1 = "SELECT a.city, count(t.ticket_id) FROM (airport a JOIN flight f ON f.arrive_airport = a.name) RIGHT JOIN ticket t \
	ON f.flight_num = t.flight_num WHERE f.name_airline = '{}' AND DATE(f.depart_time) >= '2023-01-01' AND DATE(f.arrive_time) \
	< '2023-06-01' GROUP BY a.city ORDER BY count(t.ticket_id) DESC LIMIT 3"
	query2 = "SELECT a.city, count(t.ticket_id) FROM (airport a JOIN flight f ON f.arrive_airport = a.name) RIGHT JOIN ticket t \
	ON f.flight_num = t.flight_num WHERE f.name_airline = '{}' AND DATE(f.depart_time) >= '2023-01-01' AND DATE(f.arrive_time) \
	< '2023-06-01'  GROUP BY a.city ORDER BY count(t.ticket_id) DESC LIMIT 3"
	cursor1 = conn.cursor()
	cursor1.execute(query1.format(name_airline))
	data1 = cursor1.fetchall()
	cursor1.close()
	cursor2 = conn.cursor()
	cursor2.execute(query2.format(name_airline))
	data2 = cursor2.fetchall()
	cursor2.close()
	return render_template('staffHome.html', result_des_3 = data1, result_des_y = data2)

@app.route('/toGrant', methods = ['GET', 'POST'])
def toGrant():
	permission = session['permission']
	if(permission == 1 or permission == 3):
		# return render_template('updateFlight.html')
		return redirect(url_for('showStf'))
	else:
		return render_template('staffHome.html', error = "You are not Admin")

@app.route('/showStf', methods = ['GET', 'POST'])
def showStf():
	username = session['username']
	name_airline = session['airline']
	query = "SELECT username, first_name, last_name FROM airline_staff WHERE name_airline = '{}'"
	cursor = conn.cursor()
	cursor.execute(query.format(name_airline))
	data = cursor.fetchall()
	cursor.close()
	return render_template('grantPermission.html', result = data)

@app.route('/grantPermission', methods = ['GET', 'POST'])
def grantPermission():
	staff_user = request.form['grant']
	new_status = request.form['status']
	query = "UPDATE airline_staff SET permission_id = '{}' WHERE username = '{}'"
	cursor = conn.cursor()
	cursor.execute(query.format(new_status, staff_user))
	conn.commit()
	cursor.close()
	return render_template('grantPermission.html', banner = 'Success')

@app.route('/toAddAgents', methods = ['GET', 'POST'])
def toAddAgents():
	permission = session['permission']
	if(permission == 1 or permission == 3):
		
		return render_template('addAgent.html')
	else:
		return render_template('staffHome.html', error = "You are not Admin")

@app.route('/addAgents', methods = ['Get', 'POST'])
def addAgents():
	username = session['username']
	name_airline = session['airline']
	a_email = request.form['a_email']

	query0 = "SELECT * FROM agent WHERE email = '{}'"
	cursor0 = conn.cursor()
	cursor0.execute(query0.format(a_email))
	data = cursor0.fetchone()
	cursor0.close()

	if(data):
		query1 = "SELECT * FROM works_for WHERE email = '{}' and name = '{}'"
		cursor1 = conn.cursor()
		cursor1.execute(query1.format(a_email,name_airline))
		data1 = cursor1.fetchone()
		cursor1.close()
		if(data1):
			return render_template('addAgent.html', banner = "Agent already in this airline")
		query = "INSERT INTO works_for VALUES('{}', '{}')"
		cursor = conn.cursor()
		cursor.execute(query.format(name_airline, a_email))
		conn.commit()
		cursor.close()
		return render_template('addAgent.html', banner = "Success")
	else:
		return render_template('addAgent.html', banner = "Agent does not exists")

@app.route('/logoutStf')
def logoutStf():
	session.clear()
	return redirect('/')
	
app.secret_key = 'some key that you will never guess'

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
