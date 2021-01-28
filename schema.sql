DROP TABLE IF EXISTS contact;
DROP TABLE IF EXISTS reporter;
DROP TABLE IF EXISTS enroll;
DROP TABLE IF EXISTS admin_reporter;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS constituency;

CREATE TABLE contact(
    ID INTEGER PRIMARY KEY,
	fullname VARCHAR(100) NOT NULL,
	user_location VARCHAR(50) NOT NULL,
	telephone VARCHAR(13) NOT NULL,
	symptoms VARCHAR(250) NOT NULL
);

CREATE TABLE reporter(
    username VARCHAR(200) NOT NULL PRIMARY KEY,
    passwd VARCHAR(50) NOT NULL
);

CREATE TABLE enroll(
    fullname VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    phone_number VARCHAR(13) NOT NULL,
    user_address VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    constituency VARCHAR(100) NOT NULL,
    dob DATE NOT NULL
);

CREATE TABLE admin_reporter(
    ID INTEGER PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    assigned_password VARCHAR(100) NOT NULL,
    starting_date DATE NOT NULL,
    end_date DATE Not NULL,
    constituency VARCHAR(100) NOT NULL
);

CREATE TABLE patient(
    ID INTEGER PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    next_of_kin VARCHAR(100) NOT NULL,
    constituency VARCHAR(100) NOT NULL,
    test_ID VARCHAR(20) NOT NULL,
    test_result VARCHAR(20) NOT NULL,
    quarantine VARCHAR(20) NOT NULL
);

CREATE TABLE constituency(
    constituency_name VARCHAR(100) NOT NULL PRIMARY KEY,
    region VARCHAR(100) NOT NULL
);