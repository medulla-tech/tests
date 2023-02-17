DROP TRIGGER IF EXISTS machines_before_insert;
DROP TRIGGER IF EXISTS machines_after_insert;
DROP TABLE IF EXISTS registermachines_sendbefore;
DROP TABLE IF EXISTS registermachines_sendafter;

CREATE TABLE registermachines_sendbefore
(time_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
machine_mac VARCHAR(12));

CREATE TABLE registermachines_sendafter
(time_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
machine_mac VARCHAR(12));

DELIMITER //

CREATE TRIGGER machines_before_insert BEFORE INSERT ON machines
FOR EACH ROW BEGIN
INSERT INTO registermachines_sendbefore (machine_mac) VALUES (SUBSTRING_INDEX(NEW.jid, '-', -1));
END;
//

CREATE TRIGGER machines_after_insert AFTER INSERT ON machines
FOR EACH ROW BEGIN
INSERT INTO registermachines_sendafter (machine_mac) VALUES (SUBSTRING_INDEX(NEW.jid, '-', -1));
END;
//

DELIMITER ;

DELETE FROM machines WHERE jid LIKE '%SIVEOTEST-%';
