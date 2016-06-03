CREATE OR REPLACE FUNCTION create_transaction()
RETURNS BOOLEAN AS $$
DECLARE passed BOOLEAN;
srec     record;
prec     record;
vtime    integer;
vsold    integer;


BEGIN


vtime =1000;
vsold = 5;
    FOR i in 1 .. 10
      LOOP
          FOR prec in 
		SELECT * FROM product
		
		LOOP
		    FOR srec in
        		SELECT * 
        		FROM sales_rep  
    			LOOP 
				
				vtime = vtime + 10;

                                SELECT floor(random()*(500-1)+1) * prec.gallons INTO vsold;
  
  	    			   INSERT INTO transaction VALUES (current_date,vtime,srec.sales_rep_id,prec.product_id,vsold);
			END LOOP;
		END LOOP;
	  END LOOP;
        RETURN passed;
END;
$$  LANGUAGE plpgsql;
