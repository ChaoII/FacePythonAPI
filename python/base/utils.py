import hashlib


def md5value(s):
    md5 = hashlib.md5()
    md5.update(s)
    return md5.hexdigest()
