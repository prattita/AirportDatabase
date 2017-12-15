CREATE TABLE airport(
    IATA char(3) PRIMARY KEY,
    name varchar(50) NOT NULL,
    country varchar(50) NOT NULL, 
	city varchar(50) NOT NULL,
    state varchar(50)
);

CREATE TABLE airline(
    ALCode char(2) PRIMARY KEY,
    name varchar(50) NOT NULL,
    country varchar(50) NOT NULL
);

CREATE TABLE flight(
    flightID int PRIMARY KEY,
    ALCode char(2) REFERENCES airline,
    flightNum varchar(10),
    flightDate date NOT NULL,
    departureTime timestamp NOT NULL,
    arrivalTime timestamp NOT NULL,
    miles int NOT NULL, 
    
    IATAfrom char(3) REFERENCES airport, 
    IATAto char(3) REFERENCES airport
);

CREATE TABLE price(
    flightID int REFERENCES flight,
    classes varchar(20) NOT NULL,
    price NUMERIC NOT NULL,
    capacity int NOT NULL,
    PRIMARY KEY (flightID, classes)
);

CREATE TABLE customer(
    emailAddress varchar(50) PRIMARY KEY,
    name varchar(50) NOT NULL,
    IATA char(3) REFERENCES airport
);

CREATE TABLE addresses(
    emailAddress varchar(50) REFERENCES customer,
    address varchar(50) NOT NULL,
    zipCode int,
    country varchar(50) NOT NULL,
    state varchar(50),
    city varchar(50) NOT NULL,
    PRIMARY KEY (emailAddress, address, zipCode, country, state, city)    
);

CREATE TABLE payment(
    cardNum numeric(16) PRIMARY KEY,
    expDate date NOT NULL,
    cardType varchar(20) NOT NULL,
    address varchar(50) NOT NULL,
    zipCode int,
    country varchar(50),
    state varchar(50),
    city varchar(50),
    emailAddress varchar(50),
    FOREIGN KEY (emailAddress, address, zipCode, country, state, city) REFERENCES addresses
);

CREATE TABLE booking(
    bookingID int PRIMARY KEY,
    cardNum numeric(16) REFERENCES payment
);

CREATE TABLE mileage(
    emailAddress varchar(50) REFERENCES customer,
    ALCode char(2) REFERENCES airline,
    totalMiles int,
    PRIMARY KEY (emailAddress, ALCode)
);

CREATE TABLE include(
    IATA char(3) REFERENCES airport,
    ALCode char (2) REFERENCES airline,
    PRIMARY KEY (IATA, ALCode)
);

CREATE TABLE books(
    flightID int NOT NULL,
    bookingID int NOT NULL,
    PRIMARY KEY (flightID, bookingID),
    FOREIGN KEY (flightID) REFERENCES flight,
    FOREIGN KEY (bookingID) REFERENCES booking
);

CREATE TABLE costs(
    flightID int NOT NULL,
    classes varchar(20) NOT NULL,
    bookingID int NOT NULL, 
    PRIMARY KEY (flightID, classes, bookingID),
    FOREIGN KEY (flightID, classes) REFERENCES price,
    FOREIGN KEY (bookingID) REFERENCES booking
);

CREATE TABLE earnsMileage(
    emailAddress varchar(50),
    ALCode char(2) NOT NULL,
    bookingID int REFERENCES booking, 
    PRIMARY KEY (emailAddress, ALCode, bookingID),
    FOREIGN KEY (emailAddress, ALCode) REFERENCES mileage
);