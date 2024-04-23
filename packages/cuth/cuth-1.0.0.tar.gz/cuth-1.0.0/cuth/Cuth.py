import base64
import time
import uuid
import random

from cuth.CuthConfiger import CuthConfiger


def isUuid(s):
    try:
        uuidObj = uuid.UUID(s)
        return str(uuidObj) == s
    except ValueError:
        return False


class Cuth(object):
    def __init__(self, config: CuthConfiger):
        self.config = config

    def issue(self):
        name = "cuth"
        timeStamp = str(int(time.time() * 1000000))  # length = 16
        uid = str(uuid.uuid4())  # length = 36
        b64Data = str(base64.b16encode((name + uid + timeStamp + self.config.passwd).encode("utf-8")).decode("utf-8"))
        data = b64Data + str(uuid.uuid4()) + str(random.randint(1000, 9999)) + "cuth" + self.config.salt
        return data

    def verify(self, data: str) -> bool:
        try:
            timeStamp = time.time()  # length = 16
            timeStart = str(int(timeStamp - 1 * 1000000))
            timeEnd = str(int((timeStamp + self.config.passTime) * 1000000))

            dataT = base64.b16decode(data[:- (44 + len(self.config.salt))].encode("utf-8")).decode("utf-8")
            dataUid = dataT[4:40]
            dataTime = dataT[40: -len(self.config.passwd)]
            dataPasswd = dataT[-len(self.config.passwd):]
            if not isUuid(dataUid):
                return False
            if int(dataTime) < int(timeStart) or int(dataTime) > int(timeEnd):
                return False
            if dataPasswd != self.config.passwd:
                return False
            return True
        except Exception:
            return False

    def verifyOrException(self, data: str):
        if not self.verify(data):
            raise Exception("Incorrect verify")


if __name__ == '__main__':
    a = CuthConfiger()
    a.setPasswd("12345ddwdwedwe6")
    a.setSalt("dweudhiweudhi")
    a.setPassTime(-1)
    print(a.passTime)
    b = Cuth(a)
    i = b.issue()
    print(i)
    b.verifyOrException(i)
