import hashlib

class TokenGenerator:
    def __init__(self, email):
        self.email = email.encode('utf-8')
        self.hasing = hashlib.sha256()

    def gettoken(self):
        self.hasing.update(self.email)
        return self.hasing.hexdigest()

if __name__ == '__main__':
    gen = TokenGenerator('felipegatefy@gmail.com')
    print(gen.gettoken())