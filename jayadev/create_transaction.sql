-- from postgres_05june.txt
CREATE OR REPLACE FUNCTION create_transaction()
RETURNS BOOLEAN AS $$
DECLARE passed BOOLEAN;
srec     record;
prec     record;
vtime    time;
vsold    integer;


BEGIN


vsold = 5;
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
				
				 select current_time into vtime;

                                SELECT floor(random()*(500-1)+1) INTO vsold;
  
  	    			   INSERT INTO transaction VALUES (current_date,vtime,srec.sales_rep_id,prec.product_id,vsold);
			--	  PERFORM pg_sleep(1);
			END LOOP;
 		   
		END LOOP;
                                RETURN passed;
                  --PERFORM pg_sleep(1);
	  END LOOP;
        RETURN passed;
END;
$$  LANGUAGE plpgsql;
