import psycopg2
import random
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='')
global currentLogin

@app.route('/')
def indexLogin():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/registered', methods=['POST'])
def registered():
    try:
        conn = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        cur = conn.cursor()
        email = request.form['email']
        name = request.form['name']
        cur.execute('INSERT INTO customer (emailAddress, name, IATA) VALUES (%s,%s,NULL)', (email, name))
        conn.commit()
    except:
        print("Cannot register!")
    return render_template("registered.html")

@app.route('/loginFail', methods=['POST'])
def loginFail():
    return render_template('loginFail.html')

@app.route('/LoginSuccess', methods=['POST'])
def loginSuccess():

    global currentLogin
    currentLogin = request.form['email']
    loginDICT = {'key': currentLogin}
    try:
        conn = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        cur = conn.cursor()
        cur.execute('SELECT name FROM customer WHERE emailaddress=%(key)s', loginDICT)

        if cur.rowcount is not 0:
            (name,) = cur.fetchone()
            return render_template('main.html', name=name)

        else:
            return render_template('loginFail.html')

        conn.commit()
    except:
        print("Cannot login!")

@app.route('/home')
def home():
    global currentLogin
    loginDICT = {'key': currentLogin}
    try:
        conn = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        cur = conn.cursor()

        cur.execute('SELECT name FROM customer WHERE emailaddress=%(key)s', loginDICT)
        if cur.rowcount is not 0:
            (name,) = cur.fetchone()
            return render_template('main.html', name=name)
        else:
            return render_template('loginFail.html')
        conn.commit()
    except:
        print("Cannot login!")

@app.route('/user.html')
def user():
    try:
        con = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        global currentLogin
        currentLoginDic = {'key': currentLogin}
        cur = con.cursor()
        cur.execute('SELECT * from payment WHERE emailaddress = %(key)s', currentLoginDic)
        tuple1 = cur.fetchall()

        cur1 = con.cursor()
        cur1.execute('SELECT * from addresses WHERE emailaddress = %(key)s', currentLoginDic)
        tuple2 = cur1.fetchall()
        #print(tuple2)
        con.commit()
        return render_template('user.html', email=currentLogin, tuple=tuple1, tuple2=tuple2)
    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()

        print
        'Error %s' % e
        sys.exit(1)
    finally:
        if con:
            con.close()

@app.route('/userupdate', methods=['POST'])
def userupdate():
    try:
        global currentLogin
        currentLoginDic = {'key': currentLogin}
        con = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")

        cur2 = con.cursor()
        # update
        if request.form['submit'] == 'submit':
            d = {'cardNum': request.form['cardnum'],
                 'zipcode': request.form['zipcode'],
                 'address': request.form['address'],
                 'country': request.form['country'],
                 'state': request.form['state'],
                 'city': request.form['city']}

            cur2.execute(""" UPDATE payment
                SET address = '%(address)s',
                zipcode = %(zipcode)s,
                country = '%(country)s',
                state = '%(state)s',
                city = '%(city)s'
                WHERE cardnum = %(cardNum)s""" % d)
        elif request.form['submit'] == 'delete':
            d = {'cardNum': request.form['cardnum']}
            cur2.execute("""DELETE FROM payment WHERE cardnum = '%(cardNum)s'""" % (d))
        elif request.form['submit'] == 'add':
            d = {'cardNum': request.form['cardnum'],
                 'expdate': request.form['expdate'],
                 'cardtype': request.form['cardtype'],
                 'zipcode': request.form['zipcode'],
                 'address': request.form['address'],
                 'country': request.form['country'],
                 'state': request.form['state'],
                 'city': request.form['city'],
                 'cL': currentLogin}
            cur2.execute("""INSERT INTO payment VALUES('%(cardNum)s',
                                                        '%(expdate)s',
                                                        '%(cardtype)s',
                                                        '%(address)s',
                                                        '%(zipcode)s',
                                                        '%(country)s',
                                                        '%(state)s',
                                                        '%(city)s',
                                                        '%(cL)s'
                                                        )""" % (d))
        #addupdate

        elif request.form['submit'] == 'addsubmit':
            d = {'ozipcode': request.form['oaddzipcode'],
                 'oaddress': request.form['oaddaddress'],
                 'ocountry': request.form['oaddcountry'],
                 'ostate': request.form['oaddstate'],
                 'ocity': request.form['oaddcity'],
                 'zipcode': request.form['oaddzipcode'],
                 'address': request.form['oaddaddress'],
                 'country': request.form['oaddcountry'],
                 'state': request.form['oaddstate'],
                 'city': request.form['oaddcity'],
                 'key': currentLogin}

            cur2.execute(""" UPDATE addresses
                SET address = '%(address)s',
                zipcode = '%(zipcode)s',
                country = '%(country)s',
                state = '%(state)s',
                city = '%(city)s'
                WHERE
                address = '%(oaddress)s' AND
                zipcode = '%(ozipcode)s' AND
                country = '%(ocountry)s' AND
                state = '%(ostate)s' AND
                city = '%(ocity)s' AND
                emailaddress = '%(key)s'""" % d)
        elif request.form['submit'] == 'adddelete':
            d = {'ozipcode': request.form['oaddzipcode'],
                 'oaddress': request.form['oaddaddress'],
                 'ocountry': request.form['oaddcountry'],
                 'ostate': request.form['oaddstate'],
                 'ocity': request.form['oaddcity'],
                 'zipcode': request.form['oaddzipcode'],
                 'address': request.form['oaddaddress'],
                 'country': request.form['oaddcountry'],
                 'state': request.form['oaddstate'],
                 'city': request.form['oaddcity'],
                 'key': currentLogin}

            cur2.execute("""DELETE FROM addresses
                            WHERE
                            emailaddress = '%(key)s' AND
                            address = '%(address)s' AND
                            zipcode = '%(zipcode)s' AND
                            country = '%(country)s' AND
                            state = '%(state)s' AND
                            city = '%(city)s'
                            """ % d)
        elif request.form['submit'] == 'addadd':
            d = {'zipcode': request.form['addzipcode'],
                 'address': request.form['addaddress'],
                 'country': request.form['addcountry'],
                 'state': request.form['addstate'],
                 'city': request.form['addcity'],
                 'cL': currentLogin}
            cur2.execute("""INSERT INTO addresses VALUES('%(cL)s',
                                                        '%(address)s',
                                                        '%(zipcode)s',
                                                        '%(country)s',
                                                        '%(state)s',
                                                        '%(city)s'
                                                        )""" % (d))
        con.commit()

        cur = con.cursor()
        cur.execute('SELECT * from payment WHERE emailaddress = %(key)s', currentLoginDic)
        tuple1 = cur.fetchall()
        cur1 = con.cursor()
        cur1.execute('SELECT * from addresses WHERE emailaddress = %(key)s', currentLoginDic)
        tuple2 = cur1.fetchall()

        return render_template('user.html', email=currentLogin, tuple=tuple1, tuple2=tuple2)
    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()

        print
        'Error %s' % e
        sys.exit(1)
    finally:
        if con:
            con.close()

@app.route('/searchFlights')
def searchFlights():
    IATAs = []
    try:
        conn = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        cur = conn.cursor()
        global currentLogin
        loginDICT = {'key': currentLogin}

        cur.execute('SELECT IATA FROM airport')
        IATAsquery = cur.fetchall()

        for row in IATAsquery:
            (a,) = row
            IATAs.append(a)




        return render_template('searchFlights.html', IATAs = IATAs)
    except:
        print("Can't ")

@app.route('/listOfFlights',methods=['POST'])
def listOfFlights():
    global currentLogin

    fromAir = request.form['fromAir']
    depDate = request.form['depDate']
    toAir = request.form['toAir']
    retDate = request.form['retDate']
    maxCon = request.form['maxCon']
    maxLength = request.form['maxLength']
    userPrice = request.form['userPrice']
    sortBy = request.form['sortBy']
    flightDICT = {'email':currentLogin,
                 'fromAir':fromAir,
                 'depDate':depDate,
                 'toAir':toAir,
                 'retDate':retDate,
                 'maxCon':maxCon,
                 'maxLength':maxLength,
                 'userPrice':userPrice}
    try:
        conn = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        cur = conn.cursor()
        #print(flightDICT['fromAir'])
        #print(flightDICT['toAir'])

        # if maxCon was not specified
        if not flightDICT['maxCon']:
            flightDICT['maxCon'] = 100

        #if userPrice was not specified
        if not flightDICT['userPrice']:
            flightDICT['userPrice'] = 100000

        #if maxLength was not specified
        if not flightDICT['maxLength']:
            flightDICT['maxLength'] = 2400
        else:
            flightDICT['maxLength'] = int(flightDICT['maxLength'])

        #if maxLength was not specified
        if not flightDICT['maxLength']:
            flightDICT['maxLength'] = "\'2400 hour\'::interval"

        #User specified sorting of the data, if none specified, it defaults to "Price (lowest first)"
        #DEPARTURE FLIGHTS
        if sortBy == "Price (lowest first)":
            cur.execute("""WITH RECURSIVE fPrices AS (
                                        SELECT min(price) as price, flightid, sum(capacity) as totalCapacity
                                        FROM flight NATURAL JOIN price
                                        GROUP BY flightId ),
                                    fPriceTable AS (
                                        SELECT *
                                        FROM flight NATURAL JOIN fPrices),
                                    recFlight AS (
                                        SELECT ARRAY[flightid]::text[] AS fids, flightid, alcode, flightnum, flightdate, departuretime, arrivaltime,
                                                miles, IATAFrom, IATATo, price, 1 path_length, (arrivaltime - departuretime) as totalTime,
                                                price as totalPrice, ARRAY[IATAFrom,IATATo]::text[] AS paths
                                        FROM fPriceTable
                                        WHERE IATAFrom = %(fromAir)s
                                              AND flightdate = %(depDate)s
                                              AND totalCapacity > 0
                                            UNION
                                        SELECT fids || ARRAY[two.flightid]::text[] AS fids, recFlight.flightid, recFlight.alcode, recFlight.flightnum,
                                                recFlight.flightdate, recFlight.departuretime, two.arrivaltime, recFlight.miles + two.miles AS miles,
                                                recFlight.IATAFrom, two.IATATo, two.price, path_length + 1 AS path_length,
                                                totalTime + (two.arrivaltime - two.departuretime) as totalTime, recFlight.totalPrice + two.price as totalPrice,
                                                paths || ARRAY[two.IATATo]::text[] AS paths
                                        FROM recFlight, fPriceTable as two
                                        WHERE recFlight.IATATo = two.IATAFrom
                                              AND recFLight.arrivalTime < two.departureTime
                                              AND path_length < %(maxCon)s
                                              AND totalCapacity > 0
                                    )
                                    SELECT fids, miles, path_length, totalTime, totalPrice, paths
                                    FROM recFlight
                                    WHERE IATAFrom = %(fromAir)s
                                          AND IATATo = %(toAir)s
                                          AND totalPrice < %(userPrice)s
                                          AND totalTime < interval \'%(maxLength)s hour\'
                                    ORDER BY totalPrice""", flightDICT)
            print("here")
        if sortBy == "Flight length (lowest first)":
            cur.execute("""WITH RECURSIVE fPrices AS (
                                        SELECT min(price) as price, flightid, sum(capacity) as totalCapacity
                                        FROM flight NATURAL JOIN price
                                        GROUP BY flightId ),
                                    fPriceTable AS (
                                        SELECT *
                                        FROM flight NATURAL JOIN fPrices),
                                    recFlight AS (
                                        SELECT ARRAY[flightid]::text[] AS fids, flightid, alcode, flightnum, flightdate, departuretime, arrivaltime,
                                                miles, IATAFrom, IATATo, price, 1 path_length, (arrivaltime - departuretime) as totalTime,
                                                price as totalPrice, ARRAY[IATAFrom,IATATo]::text[] AS paths
                                        FROM fPriceTable
                                        WHERE IATAFrom = %(fromAir)s AND flightdate = %(depDate)s
                                            UNION
                                        SELECT fids || ARRAY[two.flightid]::text[] AS fids, recFlight.flightid, recFlight.alcode, recFlight.flightnum,
                                                recFlight.flightdate, recFlight.departuretime, two.arrivaltime, recFlight.miles + two.miles AS miles,
                                                recFlight.IATAFrom, two.IATATo, two.price, path_length + 1 AS path_length,
                                                totalTime + (two.arrivaltime - two.departuretime) as totalTime, recFlight.totalPrice + two.price as totalPrice,
                                                paths || ARRAY[two.IATATo]::text[] AS paths
                                        FROM recFlight, fPriceTable as two
                                        WHERE recFlight.IATATo = two.IATAFrom
                                              AND recFLight.arrivalTime < two.departureTime
                                              AND path_length < %(maxCon)s
                                    )
                                    SELECT fids, miles, path_length, totalTime, totalPrice, paths
                                    FROM recFlight
                                    WHERE IATAFrom = %(fromAir)s
                                          AND IATATo = %(toAir)s
                                          AND totalPrice < %(userPrice)s
                                          AND totalTime < interval \'%(maxLength)s hour\'
                                    ORDER BY totalTime""", flightDICT)
        allFlights = cur.fetchall()
        flightIds = []
        for row in allFlights:
            flightIds.append(row[0])
        #print(flightIds)
        numFlights = len(flightIds)


        #RETURN FLIGHTS
        allRetFlights = []
        retFlightIds = []
        numRetFlights = 0
        retFlag = False
        if flightDICT['retDate']:
            retFlag = True
            if sortBy == "Price (lowest first)":
                cur.execute("""WITH RECURSIVE fPrices AS (
                                            SELECT min(price) as price, flightid, sum(capacity) as totalCapacity
                                            FROM flight NATURAL JOIN price
                                            GROUP BY flightId ),
                                        fPriceTable AS (
                                            SELECT *
                                            FROM flight NATURAL JOIN fPrices),
                                        recFlight AS (
                                            SELECT ARRAY[flightid]::text[] AS fids, flightid, alcode, flightnum, flightdate, departuretime, arrivaltime,
                                                    miles, IATAFrom, IATATo, price, 1 path_length, (arrivaltime - departuretime) as totalTime,
                                                    price as totalPrice, ARRAY[IATAFrom,IATATo]::text[] AS paths
                                            FROM fPriceTable
                                            WHERE IATAFrom = %(toAir)s
                                                  AND flightdate = %(retDate)s
                                                  AND totalCapacity > 0
                                                UNION
                                            SELECT fids || ARRAY[two.flightid]::text[] AS fids, recFlight.flightid, recFlight.alcode, recFlight.flightnum,
                                                    recFlight.flightdate, recFlight.departuretime, two.arrivaltime, recFlight.miles + two.miles AS miles,
                                                    recFlight.IATAFrom, two.IATATo, two.price, path_length + 1 AS path_length,
                                                    totalTime + (two.arrivaltime - two.departuretime) as totalTime, recFlight.totalPrice + two.price as totalPrice,
                                                    paths || ARRAY[two.IATATo]::text[] AS paths
                                            FROM recFlight, fPriceTable as two
                                            WHERE recFlight.IATATo = two.IATAFrom
                                                  AND recFLight.arrivalTime < two.departureTime
                                                  AND path_length < %(maxCon)s
                                                  AND totalCapacity > 0
                                        )
                                        SELECT fids, miles, path_length, totalTime, totalPrice, paths
                                        FROM recFlight
                                        WHERE IATAFrom = %(toAir)s
                                              AND IATATo = %(fromAir)s
                                              AND totalPrice < %(userPrice)s
                                              AND totalTime < interval \'%(maxLength)s hour\'
                                        ORDER BY totalPrice""", flightDICT)

            if sortBy == "Flight length (lowest first)":
                cur.execute("""WITH RECURSIVE fPrices AS (
                                            SELECT min(price) as price, flightid, sum(capacity) as totalCapacity
                                            FROM flight NATURAL JOIN price
                                            GROUP BY flightId ),
                                        fPriceTable AS (
                                            SELECT *
                                            FROM flight NATURAL JOIN fPrices),
                                        recFlight AS (
                                            SELECT ARRAY[flightid]::text[] AS fids, flightid, alcode, flightnum, flightdate, departuretime, arrivaltime,
                                                    miles, IATAFrom, IATATo, price, 1 path_length, (arrivaltime - departuretime) as totalTime,
                                                    price as totalPrice, ARRAY[IATAFrom,IATATo]::text[] AS paths
                                            FROM fPriceTable
                                            WHERE IATAFrom = %(toAir)s AND flightdate = %(retDate)s
                                                UNION
                                            SELECT fids || ARRAY[two.flightid]::text[] AS fids, recFlight.flightid, recFlight.alcode, recFlight.flightnum,
                                                    recFlight.flightdate, recFlight.departuretime, two.arrivaltime, recFlight.miles + two.miles AS miles,
                                                    recFlight.IATAFrom, two.IATATo, two.price, path_length + 1 AS path_length,
                                                    totalTime + (two.arrivaltime - two.departuretime) as totalTime, recFlight.totalPrice + two.price as totalPrice,
                                                    paths || ARRAY[two.IATATo]::text[] AS paths
                                            FROM recFlight, fPriceTable as two
                                            WHERE recFlight.IATATo = two.IATAFrom
                                                  AND recFLight.arrivalTime < two.departureTime
                                                  AND path_length < %(maxCon)s
                                        )
                                        SELECT fids, miles, path_length, totalTime, totalPrice, paths
                                        FROM recFlight
                                        WHERE IATAFrom = %(toAir)s
                                              AND IATATo = %(fromAir)s
                                              AND totalPrice < %(userPrice)s
                                              AND totalTime < interval \'%(maxLength)s hour\'
                                        ORDER BY totalTime""", flightDICT)
            #print("REThere")
            allRetFlights = cur.fetchall()
            for row in allRetFlights:
                retFlightIds.append(row[0])
            #print(retFlightIds)
            numRetFlights = len(retFlightIds)


        return render_template('listOfFlights.html', allFlights=allFlights, numFlights = numFlights, flightIds = flightIds,
                               allRetFlights = allRetFlights, numRetFlights = numRetFlights, retFlightIds = retFlightIds,
                               fromAir=fromAir, depDate=depDate, retDate=retDate, toAir=toAir, retFlag = retFlag)
    except psycopg2.Error as e:
        print(e.pgcode)

@app.route('/confirmOrder',methods=['POST'])
def confirmOrder():
    global currentLogin
    flightIdsSTR = request.form['flightId']

    flightIds = flightIdsSTR.split(',')
    t_flightIds = tuple(flightIds)

    loginDict = {"key":currentLogin}

    try:
        conn = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        cur = conn.cursor()



        cur.execute("""SELECT flightId, price, classes, capacity
                        FROM flight NATURAL JOIN price
                        WHERE flightid IN %s
                        ORDER BY flightId ASC""",(t_flightIds,))
        flightPriceList = (cur.fetchall())


        cur.execute("""SELECT cardNum
                        FROM payment
                        WHERE emailAddress = %(key)s""",loginDict)
        cardNums = (cur.fetchall())

        conn.commit()
        return render_template('confirmOrder.html', flightPriceList = flightPriceList, cardNums = cardNums)

    except psycopg2.Error as e:
        print(e.pgcode)


@app.route('/booked',methods=['POST'])
def booked():
    booking = request.form['bookings']
    cardNum = request.form['cardNum']

    bookingList = booking.split(',')
    bookingDict = dict([(k, v) for k,v in zip (bookingList[::2], bookingList[1::2])])

    #bid = ""
    #for key in bookingDict:
    #    bid = bid + key
    #print (bid)
    bid = random.randint(0,10000)
    valuesDict = {'cardNum':cardNum,'bid':bid}
    print(valuesDict)
    try:
        conn = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        cur = conn.cursor()

        cur.execute("""INSERT INTO booking VALUES (%(bid)s, %(cardNum)s)""",valuesDict)
        #print("INSERTED")

        for key in bookingDict:
            newDict = {'key':key, 'classes':bookingDict[key], 'bid':bid}
            cur.execute("""INSERT INTO costs VALUES (%(key)s, %(classes)s, %(bid)s)""",newDict)

        for key in bookingDict:
            newDict = {'key': key, 'classes': bookingDict[key], 'bid': bid}
            cur.execute("""UPDATE price
                            SET capacity = capacity - 1
                            WHERE flightid = %(key)s AND classes = %(classes)s""",newDict)

        conn.commit()
    except psycopg2.Error as e:
        print(e.pgcode)

    return render_template('booked.html')

@app.route('/booking.html')
def booking():
    try:
        con = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")

        global currentLogin
        currentLoginDic = {'key': currentLogin}
        #cardnum
        cur = con.cursor()
        cur.execute('SELECT *'
                    #'FROM flight WHERE flightid IN ( '
                    #'SELECT flightid '
                        'FROM costs NATURAL JOIN flight '
                        'WHERE bookingid IN ( '
                        'SELECT bookingid '
                    'FROM booking '
                    'WHERE cardnum IN ( '
                    'SELECT cardnum '
                    'FROM payment '
                    'WHERE emailaddress = %(key)s))', currentLoginDic)
        bookings = cur.fetchall()
        con.commit()
        return render_template('booking.html', email=currentLogin, bookings = bookings)
    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()

        print
        'Error %s' % e
        sys.exit(1)
    finally:
        if con:
            con.close()

@app.route('/bookingupdate', methods=['POST'])
def bookingupdate():
    try:
        con = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        cur = con.cursor()
        #store current login info
        global currentLogin
        currentLoginDic = {'key': currentLogin}
        bookingDic = {'key': request.form['bookingid']}
        cur.execute('DELETE FROM costs WHERE bookingid = %(key)s', bookingDic)
        cur.execute('DELETE FROM booking WHERE bookingid = %(key)s', bookingDic)

        cur1 = con.cursor()
        cur1.execute('SELECT *'
                    'FROM flight WHERE flightid IN ( '
                    'SELECT flightid '
                    'FROM costs '
                    'WHERE bookingid IN ( '
                    'SELECT bookingid '
                    'FROM booking '
                    'WHERE cardnum IN ( '
                    'SELECT cardnum '
                    'FROM payment '
                    'WHERE emailaddress = %(key)s)))', currentLoginDic)
        bookings = cur1.fetchall()
        con.commit()
        return render_template('booking.html', email=currentLogin, bookings=bookings)

    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()
        print
        'Error %s' % e
        sys.exit(1)
    finally:
        if con:
            con.close()

if __name__ == '__main__':
    app.run(debug=True)