import psycopg2


def drop_tables():
    try:
        conn = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
        cur = conn.cursor()
        cur.execute("""DROP TABLE earnsMileage;
                           DROP TABLE costs;
                           DROP TABLE books;
                           DROP TABLE include;
                           DROP TABLE booking;
                           DROP TABLE payment;
                           DROP TABLE addresses;
                           DROP TABLE mileage;
                           DROP TABLE price;
                           DROP TABLE flight;
                           DROP TABLE customer;
                           DROP TABLE airline;
                           DROP TABLE airport;""")
        conn.commit()
    except psycopg2.Error as e:
        print(e.pgcode)

if __name__ == '__main__':
    conn = psycopg2.connect("dbname='AirlineDB' user='postgres' host='localhost' password='Nintendo_20'")
    cur = conn.cursor()

    drop_tables()

    cur.execute("""CREATE TABLE IF NOT EXISTS airport(
                   IATA char(3) PRIMARY KEY,
                   name varchar(50) NOT NULL,
                   country varchar(50) NOT NULL,
                   state varchar(50),
                   city varchar(50) NOT NULL);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS airline(
                   ALCode char(2) PRIMARY KEY,
                   name varchar(50) NOT NULL,
                   country varchar(50) NOT NULL);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS flight(
                    flightID int PRIMARY KEY,
                    ALCode char(2) REFERENCES airline,
                    flightNum varchar(10),
                    flightDate date NOT NULL,
                    departureTime timestamp NOT NULL,
                    arrivalTime timestamp NOT NULL,
                    miles int NOT NULL,
                    IATAfrom char(3) REFERENCES airport,
                    IATAto char(3) REFERENCES airport);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS price(
                    flightID int REFERENCES flight,
                    classes varchar(20) NOT NULL,
                    price NUMERIC NOT NULL,
                    capacity int NOT NULL,
                    PRIMARY KEY (flightID, classes));""")

    cur.execute("""CREATE TABLE IF NOT EXISTS customer(
                    emailAddress varchar(50) PRIMARY KEY,
                    name varchar(50) NOT NULL,
                    IATA char(3) REFERENCES airport);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS addresses(
                    emailAddress varchar(50) REFERENCES customer,
                    address varchar(50) NOT NULL,
                    zipCode int,
                    country varchar(50) NOT NULL,
                    state varchar(50),
                    city varchar(50) NOT NULL,
                    PRIMARY KEY (emailAddress, address, zipCode, country, state, city));""")

    cur.execute("""CREATE TABLE IF NOT EXISTS payment(
                    cardNum numeric(16) PRIMARY KEY,
                    expDate date NOT NULL,
                    cardType varchar(20) NOT NULL,
                    address varchar(50) NOT NULL,
                    zipCode int,
                    country varchar(50),
                    state varchar(50),
                    city varchar(50),
                    emailAddress varchar(50),
                    FOREIGN KEY (emailAddress, address, zipCode, country, state, city) REFERENCES addresses);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS booking(
                    bookingID int PRIMARY KEY,
                    cardNum numeric(16) REFERENCES payment);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS mileage(
                    emailAddress varchar(50) REFERENCES customer,
                    ALCode char(2) REFERENCES airline,
                    totalMiles int,
                    PRIMARY KEY (emailAddress, ALCode));""")

    cur.execute("""CREATE TABLE IF NOT EXISTS include(
                    IATA char(3) REFERENCES airport,
                    ALCode char (2) REFERENCES airline,
                    PRIMARY KEY (IATA, ALCode));""")

    cur.execute("""CREATE TABLE IF NOT EXISTS books(
                    flightID int NOT NULL,
                    bookingID int NOT NULL,
                    PRIMARY KEY (flightID, bookingID),
                    FOREIGN KEY (flightID) REFERENCES flight,
                    FOREIGN KEY (bookingID) REFERENCES booking);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS costs(
                    flightID int NOT NULL,
                    classes varchar(20) NOT NULL,
                    bookingID int NOT NULL,
                    PRIMARY KEY (flightID, classes, bookingID),
                    FOREIGN KEY (flightID, classes) REFERENCES price,
                    FOREIGN KEY (bookingID) REFERENCES booking);""")

    cur.execute("""CREATE TABLE IF NOT EXISTS earnsMileage(
                    emailAddress varchar(50),
                    ALCode char(2) NOT NULL,
                    bookingID int REFERENCES booking,
                    PRIMARY KEY (emailAddress, ALCode, bookingID),
                    FOREIGN KEY (emailAddress, ALCode) REFERENCES mileage);""")

    conn.commit()
