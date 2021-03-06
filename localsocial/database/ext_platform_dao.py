from localsocial.database.db import db_conn, handled_execute

"""
	CREATE TABLE platformLink (
	userId			INTEGER REFERENCES users (userId) NOT NULL,
	loginPlatform	platform NOT NULL,
	externalId		VARCHAR(75) NOT NULL,
"""

def create_external_link(userId, platform, externalId):
	cursor = handled_execute(db_conn, """
		INSERT INTO platformLink (userId, loginPlatform, externalId)
		VALUES (%s, %s, %s);
		""", (userId, platform, externalId))

	return userId

def get_external_link(platform, externalId):
	cursor = handled_execute(db_conn, """
		SELECT userId FROM platformLink
		WHERE loginPlatform=%s AND externalId=%s;
		""", (platform, externalId))

	db_conn.commit()

	row = db_conn.fetchone()

	if row != None:
		return row[0]
	else:
		# Do we want to raise an exception here or do we want to return None?
		# In isolation, returning None makes more sense, but for the sake of
		# consistency, it may make more sense to raise an exception

		return None

