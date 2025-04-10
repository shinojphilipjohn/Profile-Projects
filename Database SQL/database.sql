CREATE TABLE Country(
location VARCHAR(50) NOT NULL PRIMARY KEY
);

CREATE TABLE USState(
state VARCHAR(50) NOT NULL PRIMARY KEY
);

CREATE TABLE Date(
date VARCHAR(50) NOT NULL PRIMARY KEY
);

CREATE TABLE AgeGroup(
location VARCHAR(50) NOT NULL
, date VARCHAR(50) NOT NULL
, age_group VARCHAR(30)
, people_vaccinated_per_hundred NUMERIC
, people_fully_vaccinated_per_hundred NUMERIC
, people_with_booster_per_hundred NUMERIC,
FOREIGN KEY (location) REFERENCES Country(location),
FOREIGN KEY (date) REFERENCES DATE(date),
PRIMARY KEY (location,date)
);

CREATE TABLE USVaccine(
location VARCHAR(50) NOT NULL
, state VARCHAR(50) NOT NULL
, date VARCHAR(50) NOT NULL
, total_vaccinations NUMERIC
, total_distributed NUMERIC
, people_vaccinated NUMERIC
, people_fully_vaccinated_per_hundred NUMERIC
, total_vaccinations_per_hundred NUMERIC
, people_fully_vaccinated NUMERIC
, people_vaccinated_per_hundred NUMERIC
, distributed_per_hundred NUMERIC
, daily_vaccinations_raw NUMERIC
, daily_vaccinations NUMERIC
, daily_vaccinations_per_million NUMERIC
, share_doses_used NUMERIC
, total_boosters NUMERIC
, total_boosters_per_hundred NUMERIC,
FOREIGN KEY (location) REFERENCES Country(location),
FOREIGN KEY (date) REFERENCES DATE(date),
FOREIGN KEY (state) REFERENCES USState(state),
PRIMARY KEY (location,state,date)
);



CREATE TABLE Vaccination(
location VARCHAR(50) NOT NULL
, date VARCHAR(50) NOT NULL
, total_vaccinations NUMERIC
, people_vaccinated NUMERIC
, people_fully_vaccinated NUMERIC
, total_boosters NUMERIC
, daily_vaccinations_raw NUMERIC
, daily_vaccinations NUMERIC
, total_vaccinations_per_hundred NUMERIC
, people_vaccinated_per_hundred NUMERIC
, people_fully_vaccinated_per_hundred NUMERIC
, total_boosters_per_hundred NUMERIC
, daily_vaccinations_per_million NUMERIC
, daily_people_vaccinated NUMERIC
, daily_people_vaccinated_per_hundred NUMERIC,
FOREIGN KEY (location) REFERENCES Country(location),
FOREIGN KEY (date) REFERENCES DATE(date),
PRIMARY KEY (location,date)
);

CREATE TABLE Manufacturer(
location VARCHAR(50) NOT NULL
, vaccines VARCHAR(50) NOT NULL
, date VARCHAR(50) NOT NULL
, total_vaccinations NUMERIC,
FOREIGN KEY (location) REFERENCES Country(location),
FOREIGN KEY (date) REFERENCES DATE(date),
FOREIGN KEY (vaccines) REFERENCES Vaccine(vaccines),
PRIMARY KEY (location,vaccines,date)
);


CREATE TABLE Vaccine(
location VARCHAR(50) NOT NULL
, vaccines VARCHAR(50) NOT NULL,
FOREIGN KEY (location) REFERENCES Country(location),
PRIMARY KEY (location,vaccines)
);

CREATE TABLE VaccineDetail(
location VARCHAR(50) NOT NULL
, vaccines VARCHAR(50) NOT NULL
, source_name VARCHAR(50) NOT NULL
, last_observation_date VARCHAR(50)
, source_website VARCHAR(100),
FOREIGN KEY (location) REFERENCES Country(location),
FOREIGN KEY (vaccines) REFERENCES Vaccine(vaccines),
PRIMARY KEY (location,vaccines,source_name)
);

CREATE TABLE VaccineCountryDetail(
location VARCHAR(50) NOT NULL
, vaccines VARCHAR(50) NOT NULL
, date VARCHAR(50) NOT NULL
, source_url VARCHAR(100)
, total_vaccinations NUMERIC
, people_vaccinated NUMERIC
, people_fully_vaccinated NUMERIC
, total_boosters NUMERIC,
FOREIGN KEY (location) REFERENCES Country(location),
FOREIGN KEY (date) REFERENCES DATE(date),
FOREIGN KEY (vaccines) REFERENCES Vaccine(vaccines),
PRIMARY KEY (location,vaccines,date)
);

