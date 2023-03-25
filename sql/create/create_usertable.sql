-- username will default to 'guest' in case of no username, unlikely to happen, but covering bases
-- createdAt will default to return from sysdate(), the need to change this is unlikely
-- permRange will have a range from 1 to 5, where 1 is regular user, and 5 is master admin level

CREATE TABLE IF NOT EXISTS Users
(
    username VARCHAR(30)  PRIMARY KEY
                        NOT NULL,
    createdAt TIMESTAMP   NOT NULL
                        DEFAULT current_timestamp,
    permissionLevel INT   NOT NULL
                        DEFAULT 1,
    CONSTRAINT permRange 
	CHECK (permissionLevel >= 1 AND permissionLevel <= 5)
);
