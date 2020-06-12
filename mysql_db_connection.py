# The program will scrape the ads page by page
# The URLs of ads will be written into the MariaDB database
# in the server "jaguar.cs.gsu.edu"

# Run "$ sudo apt-get install sshpass" in Ubuntu terminal if you see relevant errors.

import datetime
import os
import mysql
import mysql.connector

class MySQL_Telegram_DB:
    # remote SQL database server
    m_sServerHost = "jaguar.cs.gsu.edu"
    m_sServerUser = "telegram"
    m_sServerPasswd = "" # Avinash updated the passwd
    m_sServerDatabaseUser = "telegram_admin"
    m_sServerDatabasePasswd = ""
    m_sServerDatabase = "telegram"
    m_sServerPort = "3306"
    m_bServerSQLBuffered = True
    # remote root directory in the file system of the server OS
    m_s_telegram_group_name = ""
    # for each column in the table of the db, we need to create a variable here

    def MySQLQueryBasicInfor(self):
        # query basic information of the mysql database
        aMariaDB_cryptomarkets = mysql.connector.connect(host=self.m_sServerHost, user=self.m_sServerDatabaseUser, passwd=self.m_sServerDatabasePasswd,
                                        database=self.m_sServerDatabase, port=self.m_sServerPort, buffered=self.m_bServerSQLBuffered)
        aCursorDB_cryptomarkets = aMariaDB_cryptomarkets.cursor(dictionary=True)
        # Fetch student information
        aSelectStmt_students_list = "SELECT student_ID FROM students_list WHERE student_name_abbr='" + self.m_sStudentNameAbbr + "';"
        aCursorDB_cryptomarkets.execute(aSelectStmt_students_list)
        if aCursorDB_cryptomarkets.rowcount == 1:
            aOneStudentRecord = aCursorDB_cryptomarkets.fetchone()
            self.m_sStudentIDinDB = aOneStudentRecord["student_ID"]
        # Fetch market information
        aSelectStmt_cryptomarkets_list = "SELECT * FROM cryptomarkets_list WHERE cryptomarket_name_abbr='" + self.m_sMarketNameAbbr + "';"
        aCursorDB_cryptomarkets.execute(aSelectStmt_cryptomarkets_list)
        if aCursorDB_cryptomarkets.rowcount == 1:
            aOneMarketRecord = aCursorDB_cryptomarkets.fetchone()
            self.m_sMarketURL = aOneMarketRecord["cryptomarket_url"]
            self.m_nMarketGlobalID = aOneMarketRecord["cryptomarket_global_ID"]
            self.m_sMarketUserName = aOneMarketRecord["my_username"]
            self.m_sMarketPassword = aOneMarketRecord["my_password"]
            self.m_sRemoteRootDirectoryProductDesc = aOneMarketRecord["product_desc_root_directory"]
            self.m_sRemoteRootDirectoryProductRating = aOneMarketRecord["product_rating_root_directory"]
            self.m_sRemoteRootDirectoryVendorProfile = aOneMarketRecord["vendor_profile_root_directory"]
            self.m_sRemoteRootDirectoryVendorRating = aOneMarketRecord["vendor_rating_root_directory"]
        aMariaDB_cryptomarkets.close()

    def UpdateDatabaseUploadFileProductDescription(self, sLocalOutputFileName, sLocalOutputFileNameFullPath, sProductMarketID):
        # Insert this scraping event to the product_desc_scraping_event table in the SQL database
        aMariaDB_cryptomarkets = mysql.connector.connect(host=self.m_sServerHost, user=self.m_sServerDatabaseUser, passwd=self.m_sServerDatabasePasswd,
                                        database=self.m_sServerDatabase, port=self.m_sServerPort, buffered=self.m_bServerSQLBuffered)
        aCursorDB_cryptomarkets = aMariaDB_cryptomarkets.cursor(dictionary=True)
        aInsertStmt_product_scraping_event = (
            "INSERT INTO product_desc_scraping_event (product_global_ID, scraping_time, product_desc_file_path_in_FS, student_ID) "
            "VALUES (%(product_global_ID)s, %(scraping_time)s, %(product_desc_file_path_in_FS)s, %(student_ID)s)")
        aData_product_scraping_event = {
            'product_global_ID': self.m_nProductGlobalID,
            'scraping_time': self.m_sCurrentUTCTime,
            'product_desc_file_path_in_FS': sLocalOutputFileName,
            'student_ID': self.m_sStudentIDinDB
        }
        aCursorDB_cryptomarkets.execute(aInsertStmt_product_scraping_event, aData_product_scraping_event)
        aMariaDB_cryptomarkets.commit()
        # unlock the my_lock_pd cell of this product record in the product_list table
        aUpdateStmt_product_list = "UPDATE product_list SET my_lock_pd=0, last_scraping_time_pd='" + self.m_sCurrentUTCTime \
                                   + "' WHERE cryptomarket_global_ID='" + str(self.m_nMarketGlobalID) \
                                   + "' AND product_market_ID='" + sProductMarketID + "' AND my_lock_pd=1;"
        aCursorDB_cryptomarkets.execute(aUpdateStmt_product_list)
        aMariaDB_cryptomarkets.commit()
        aMariaDB_cryptomarkets.close()

