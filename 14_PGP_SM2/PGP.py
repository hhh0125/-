from gmssl import sm2,sm4
import random

def PGP_enc(msg,key):


    # 填充
    n=len(msg)
    if n%16!=0:
        num=16-(n%16)
    else:
        num=0
    msg=msg+('\0'*num)
    # 使用sm4对消息进行加密
    sm4_crypt=sm4.CryptSM4()
    sm4_crypt.set_key(key.encode(),1)
    c1=sm4_crypt.crypt_ecb(msg.encode())

    # 使用sm2对密钥进行加密
    c2=sm2_crypt.encrypt(key.encode())

    return c1.hex(),c2.hex()

def PGP_dec(c1,c2):
    key=sm2_crypt.decrypt(c2.encode())

    sm4_crypt=sm4.CryptSM4()
    sm4_crypt.set_key(key,0)
    msg=sm4_crypt.crypt_ecb(c1.encode())
    return msg.hex(),key.hex()

if __name__=='__main__':
    pk='B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    sk='00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    sm2_crypt=sm2.CryptSM2(public_key=pk,private_key=sk)
    print(f'sm2中公钥为：{pk}，私钥为：{sk}')

    msg="202100460145"
    key=hex(random.randint(2 ** 127, 2 ** 128))[2:]
    print(f'消息为：{msg.encode()}，密钥为：{key.encode()}')

    print("----------加密----------")
    c1,c2=PGP_enc(msg,key)
    print(f'消息密文为：{c1}，密钥密文为：{c2}')

    print('----------解密----------')
    msg_n,key_n=PGP_dec(c1,c2)
    print(f'消息为：{msg}，密钥为：{key}')