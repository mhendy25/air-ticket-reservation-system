create table airline(
    name varchar(25),
    primary key(name)
);
create table airline_staff(
    user_name  varchar(12), 
    first_name varchar(12),
    last_name varchar(12),
    password decimal(12),
    date_of_birth date,
    airline_name    varchar(25),
    primary key (user_name),
    foreign key (airline_name) references airline(name));

create table permission(
    user_name   varchar(12),
    permission_type varchar(8),
    primary key (user_name, permission_type),
    foreign key (user_name) references airline_staff(user_name));

create table airplane(
    id  int,
    airline_name varchar(25),
    primary key(id, airline_name),
    foreign key (airline_name) references airline(name)
);


create table airport(
    name varchar(25),
    city varchar(12),
    primary key (name)
);
create table customer(
    email varchar(24),
    name varchar(12),
    building_number int,
    street varchar(15),
    password varchar(12),
    city varchar(10),
    state varchar(12),
    phone_number decimal(11,0), 
    passport_number varchar(20), -- passport numbers may have letters as well as numbers 
    passport_expiration date,
    passport_country varchar(15),
    date_of_birth date,
    primary key(email)
);

create table booking_agent(
    email varchar(24),
    password varchar(15),
    booking_agent_id int,
    primary key(email)
);

create table works_for(
    booking_agent_email varchar(24),
    airline_name varchar (25),
    primary key(booking_agent_email,airline_name),
    foreign key(booking_agent_email) references booking_agent(email),
    foreign key(airline_name) references airline(name)

);

create table flight(
    flight_number int,
    departure_time datetime,
    arrival_time datetime,
    price decimal(8,2), -- assume USD is the main currency 
    status varchar (11),
    airline_name varchar(25),
    airplane_id int,
    departure_airport_name varchar(20),
    arrival_airport_name varchar(120),
    primary key (flight_number, airline_name),
    foreign key (airline_name) references airline(name),
    foreign key (arrival_airport_name) references airport(name),
    foreign key (departure_airport_name) references airport(name),
    foreign key (airplane_id) references airplane(id)

);



create table ticket(
    ticket_id int,
    flight_number int,
    customer_email varchar(24),
    booking_agent_email varchar(24),
    primary key(ticket_id),
    foreign key (flight_number) references flight(flight_number),
    foreign key (customer_email) references customer(email),
    foreign key (booking_agent_email) references booking_agent(email)
);




