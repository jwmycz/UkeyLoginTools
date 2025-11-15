from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
class jm:
    def aes_encrypt(self,plaintext, key):
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return (iv + ciphertext).hex()
    def aes_decrypt(self,ciphertext, key):
        def im(ciphertext, key):
            iv = ciphertext[:16]

            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)
            return plaintext.decode()
        try:
            ciphertext = bytes.fromhex(ciphertext)
            return im(ciphertext, key)
        except Exception as e:
            return im(ciphertext, key)
    def aes_alldata(self,ciphertext,types,bskey='kCsXHMdhQHb1zMVIzqFQQA=='):
        key = base64.b64decode(bskey)
        if types == 1:
            return self.aes_decrypt(ciphertext, key)
        elif types == 2:
            return self.aes_encrypt(ciphertext, key)
    def getkey(self):
        key = get_random_bytes(16)
        key_b64 = base64.b64encode(key).decode()
        return key_b64

    def setkey(self,key):
        newkey = base64.b64decode(key)
        return newkey


    def jiami(self,data):
        getkey = self.getkey()
        newkey = self.setkey(getkey)
        newwkey = self.aes_alldata(getkey, 2)
        newdata = self.aes_encrypt(data, newkey)
        return {'key':newwkey,'data':newdata}
    def jiemi(self,key,data):
        key = self.aes_alldata(key, 1)
        nnew = self.setkey(key)
        data = self.aes_decrypt(data, nnew)
        return data



