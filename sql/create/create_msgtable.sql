-- Messages records use userID for foreign key in case of username collisions
-- sentAt will default to return of sysdate() function
-- userID will reference the Users table

CREATE TABLE IF NOT EXISTS Messages
(
    messageID SERIAL PRIMARY KEY,
    userID BIGINT UNSIGNED NOT NULL,
    content VARCHAR(1024)   NOT NULL,
    sentAt TIMESTAMP        NOT NULL
                            DEFAULT current_timestamp,
    CONSTRAINT fk_userID
    FOREIGN KEY(userID) 
	REFERENCES Users(userID)
);
