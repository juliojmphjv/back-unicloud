import hashlib
import uuid

class TokenGenerator:
    def __init__(self, email):
        self.email = email.encode('utf-8')
        self.hasing = hashlib.sha256()

    def random_string(self):
        random_string = uuid.uuid4()
        return random_string

    def gettoken(self):
        # self.hasing.update(self.email)
        invitation = f'{self.email}.{self.random_string()}'.encode('utf-8')
        self.hasing.update(invitation)
        return self.hasing.hexdigest()

if __name__ == '__main__':
    gen = TokenGenerator('felipegatefy@gmail.com')
    print(gen.gettoken())