insert into airline values ('Egypt Air');
insert into airport values ('CIA', 'Cairo');
insert into airport values ('PVG','Shanghai');
insert into customer values ('mohamedhendy@gmail.com', 'Mohamed','1','tahrir','1234','new cairo','cairo','9876','A2019','2027-08-02','Egypt','2003-08-08');
insert into customer values ('arghyasarkar@gmail.com', 'arghya','2','dokki','1234','dokki','cairo','98765','E209','2026-09-02','Egypt','2003-07-02');
insert into booking_agent values('agent@gmail.com','1234','1');
insert into airplane values ('1','Egypt Air');
insert into airplane values ('2','Egypt Air');
insert into airline_staff values ('travel_managers','Ahmed','Ali','1234','2003-02-07','Egypt Air');
insert into flight values ('1','2023-05-05 04:00:00','05:00:00','200','In Progress','Egypt Air','1','CIA','PVG');
insert into flight values ('2','2023-05-06 06:00:00','07:00:00','300','Up Coming','Egypt Air','2','CIA','PVG');
insert into flight values ('3','2020-05-07 08:00:00','09:00:00','400','Up Coming','Egypt Air','1','PVG','CIA');
insert into ticket values ('1','1','mohamedhendy@gmail.com',null);
insert into ticket values ('2','2','arghyasarkar@gmail.com','agent@gmail.com');

-- assume USD is the main currency 
-- passport numbers may have letters as well as numbers 