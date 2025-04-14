USE ncat;

CREATE TABLE rosterclass(
	rosterid int,
    userid int,
    FOREIGN KEY (rosterid) REFERENCES roster(id),
    FOREIGN KEY (userid) REFERENCES userid(id)
);