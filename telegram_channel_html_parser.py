
from mysql_db_connection import MySQL_Telegram_DB


if __name__ == '__main__':
    # Read the html, parse it using beautiful soup, get the data,

    # query the SQL server to retrieve some basic information
    aMySQL_Telegram_DB = MySQL_Telegram_DB()
    aMySQL_Telegram_DB.m_s_telegram_group_name = "Fullz"
    aMySQL_Telegram_DB.MySQLQueryBasicInfor()