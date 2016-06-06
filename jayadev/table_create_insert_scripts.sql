CREATE TABLE sales_rep (
    sales_rep_id    char(5) CONSTRAINT firstkey PRIMARY KEY,
    sales_rep_name  varchar(40)    NOT NULL,
    sales_rep_territory varchar(5) NOT NULL,
    daily_gallon_plan  integer     NOT NULL
);

INSERT INTO sales_rep VALUES ('1-001','John Smith','NE',500);
INSERT INTO sales_rep VALUES ('1-002','Linda Errico','SE',1000);
INSERT INTO sales_rep VALUES ('1-003','Ed Smith','NYC',3000);
INSERT INTO sales_rep VALUES ('1-004','Dennis Brunzell','GL',2000);
INSERT INTO sales_rep VALUES ('1-005','Carl Kowaski','WC',1000);
INSERT INTO sales_rep VALUES ('1-006','Jung Lim','NYC',1000);
INSERT INTO sales_rep VALUES ('1-007','Andy Jerkin','NE',500);
INSERT INTO sales_rep VALUES ('1-008','Carla Pollak','WC',2000);
INSERT INTO sales_rep VALUES ('1-009','Samson Smith','TX',4000);
INSERT INTO sales_rep VALUES ('1-010','Lory Ann Curt','SE',3000);

CREATE TABLE territory (
    territory_id    varchar(5) CONSTRAINT tkey PRIMARY KEY,
    territory_name  varchar(40)    NOT NULL
);

INSERT INTO territory VALUES ('NE','North East');
INSERT INTO territory VALUES ('SE','South East');
INSERT INTO territory VALUES ('NYC','New York Metro');
INSERT INTO territory VALUES ('GL','Great Lakes');
INSERT INTO territory VALUES ('WC','West Coast');
INSERT INTO territory VALUES ('TX','Texas');

CREATE TABLE product (
    product_id    varchar(5) CONSTRAINT pkey PRIMARY KEY,
    gallons       decimal(7,2)    NOT NULL
);

INSERT INTO product VALUES ('N001',5);
INSERT INTO product VALUES ('A001',5);
INSERT INTO product VALUES ('C005',.5);
INSERT INTO product VALUES ('M004',.25);
INSERT INTO product VALUES ('N005',.5);

CREATE TABLE transaction
(order_date   date,
 order_time   time with time zone,
 sales_rep_id char(5),
 product_id   varchar(5),
 unit_sold    integer);

INSERT INTO transaction VALUES (current_date,1000,'1-001','N001',25);
INSERT INTO transaction VALUES (current_date,1000,'1-002','A001',15);
INSERT INTO transaction VALUES (current_date,1000,'1-003','M004',20);
INSERT INTO transaction VALUES (current_date,1000,'1-004','N005',11);
INSERT INTO transaction VALUES (current_date,1000,'1-005','C005',30);
