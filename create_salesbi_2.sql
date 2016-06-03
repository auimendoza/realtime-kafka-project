CREATE TABLE territory_state
(territory_id varchar(5),
 state varchar(2),
 latitude real,
 longitude real
);

INSERT INTO territory_state (territory_id, state) VALUES ('GL','IL');
INSERT INTO territory_state (territory_id, state) VALUES ('GL','IN');
INSERT INTO territory_state (territory_id, state) VALUES ('GL','MI');
INSERT INTO territory_state (territory_id, state) VALUES ('GL','MN');
INSERT INTO territory_state (territory_id, state) VALUES ('GL','OH');
INSERT INTO territory_state (territory_id, state) VALUES ('GL','WI');

INSERT INTO territory_state (territory_id, state) VALUES ('NE','CT');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','DE');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','MA');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','MD');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','ME');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','NH');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','NJ');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','NY');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','PA');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','RI');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','VA');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','VT');
INSERT INTO territory_state (territory_id, state) VALUES ('NE','WV');

INSERT INTO territory_state (territory_id, state, latitude, longitude) VALUES ('NYC','NY', 40.7773, -73.8727);

INSERT INTO territory_state (territory_id, state) VALUES ('WC','AK');
INSERT INTO territory_state (territory_id, state) VALUES ('WC','CA');
INSERT INTO territory_state (territory_id, state) VALUES ('WC','OR');
INSERT INTO territory_state (territory_id, state) VALUES ('WC','WA');

INSERT INTO territory_state (territory_id, state) VALUES ('TX','TX');

INSERT INTO territory_state (territory_id, state) VALUES ('SE','AL');
INSERT INTO territory_state (territory_id, state) VALUES ('SE','AR');
INSERT INTO territory_state (territory_id, state) VALUES ('SE','FL');
INSERT INTO territory_state (territory_id, state) VALUES ('SE','GA');
INSERT INTO territory_state (territory_id, state) VALUES ('SE','KY');
INSERT INTO territory_state (territory_id, state) VALUES ('SE','LA');
INSERT INTO territory_state (territory_id, state) VALUES ('SE','MS');
INSERT INTO territory_state (territory_id, state) VALUES ('SE','NC');
INSERT INTO territory_state (territory_id, state) VALUES ('SE','SC');
INSERT INTO territory_state (territory_id, state) VALUES ('SE','TN');

COMMIT;

CREATE VIEW gallons_by_territory
AS
WITH sg AS (SELECT sr.sales_rep_id, sum(p.gallons*tr.unit_sold) gallons_sold, sr.daily_gallon_plan
			  FROM transaction tr inner join sales_rep sr on tr.sales_rep_id = sr.sales_rep_id
			                      inner join product p on tr.product_id = p.product_id
			 WHERE tr.order_date = current_date
			 GROUP BY sr.sales_rep_id)
SELECT sr.sales_rep_territory, SUM(sg.gallons_sold) total_gallons_sold, SUM(sr.daily_gallon_plan) total_gallons_plan
  FROM sales_rep sr INNER JOIN sg ON sr.sales_rep_id = sg.sales_rep_id
 GROUP BY sales_rep_territory;
