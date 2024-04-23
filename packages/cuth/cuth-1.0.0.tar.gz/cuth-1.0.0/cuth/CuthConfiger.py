import random
from ceasylog import *

loggerCfg = LoggerConfiger()
loggerCfg.setName(__name__)
loggerCfg.setMinPrintLevel(LoggerLevel.INFO)
logger = Logger(loggerCfg)


def checkPasswd(passwd: str) -> None:
    if len(passwd) < 6:
        logger.warn("Your password is too short, recommend at least 6 characters.")
    try:
        int(passwd)
        logger.warn("Your password is too simple, recommend to use a string include number and special characters.")
    except ValueError:
        ...
    if passwd.isalpha():
        logger.warn("Your password is too simple, recommend to use a string include number and special characters.")


class CuthConfiger(object):
    def __init__(self):
        self.salt = str(random.randint(32768, 65536))
        self.passwd = "passwd"
        self.passTime = 10  # s

    def setPasswd(self, passwd: str) -> None:
        checkPasswd(passwd)
        self.passwd = passwd

    def setSalt(self, salt: str) -> None:
        logger.warn("We do not recommend set a salt by user.")
        self.salt = salt

    def setPassTime(self, passTime: int) -> None:
        passTime = int(passTime)
        if passTime < 0:
            logger.error("The timeout must be an integer because time will not flow backwards. Used default 10s")
            return
        elif passTime < 1:
            logger.warn("We do not recommend setting a timeout that is too small, as this will allow the time spent "
                        "in data transmission to be accounted for. It is recommended to set it to more than 1s")
        if passTime > 60:
            logger.warn("We do not recommend setting a timeout that is too large, as this will allow the time spent "
                        "in data transmission to be accounted for. It is recommended to set it to less than 60s")
        self.passTime = passTime
