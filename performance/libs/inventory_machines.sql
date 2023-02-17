DROP TRIGGER IF EXISTS glpi_computers_before_insert;
DROP TRIGGER IF EXISTS glpi_computers_after_insert;
DROP TABLE IF EXISTS inventorymachines_sendbefore;
DROP TABLE IF EXISTS inventorymachines_sendafter;

CREATE TABLE inventorymachines_sendbefore
(time_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
name VARCHAR(255));

CREATE TABLE inventorymachines_sendafter
(time_insert TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
name VARCHAR(255));

DELIMITER //

CREATE TRIGGER glpi_computers_before_insert BEFORE INSERT ON glpi_computers
FOR EACH ROW BEGIN
INSERT INTO inventorymachines_sendbefore SET inventorymachines_sendbefore.name = NEW.name;
END;
//

CREATE TRIGGER glpi_computers_after_insert AFTER INSERT ON glpi_computers
FOR EACH ROW BEGIN
INSERT INTO inventorymachines_sendafter SET inventorymachines_sendafter.name = NEW.name;
END;
//

DELIMITER ;
