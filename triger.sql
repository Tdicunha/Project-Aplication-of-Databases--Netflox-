CREATE OR REPLACE FUNCTION f2() RETURNS trigger AS $$
    BEGIN
        if new.saldo<0 then 
            raise exception 'no money';
        end if; 
        RETURN new;
    END;
    $$ LANGUAGE plpgsql;

CREATE TRIGGER t2 before update ON cliente
FOR EACH ROW

EXECUTE FUNCTION f2();
END;