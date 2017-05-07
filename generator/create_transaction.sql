CREATE OR REPLACE FUNCTION create_transaction()
RETURNS BOOLEAN AS $$
DECLARE passed BOOLEAN;
srec     record;
prec     record;
vsold    integer;

BEGIN
  FOR i in 1 .. 1
  LOOP
    FOR prec in 
      SELECT * FROM product ORDER BY random()
       LIMIT ceil(random()*3)
    LOOP
      FOR srec in
        SELECT * 
          FROM sales_rep   ORDER BY random()
         LIMIT ceil(random()*3)
      LOOP 
        SELECT floor(random()*(500-1)+1) INTO vsold;
        INSERT INTO transaction VALUES (current_date,current_time,srec.sales_rep_id,prec.product_id,vsold);
      END LOOP;
    END LOOP;
    RETURN passed;
  END LOOP;
END;
$$  LANGUAGE plpgsql;
