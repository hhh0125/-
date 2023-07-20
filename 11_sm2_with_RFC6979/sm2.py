import hmac
from hashlib import sha256

from gmssl import sm2,func



# 椭圆曲线的相关参数
canshu={
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'q': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
    'g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7'
         'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'x':'00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5',
    'U':'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
}



def _double_point(Point):  # 倍点
    l = len(Point)
    para_len=len(canshu['n'])
    len_2 = 2 * para_len
    if l < para_len * 2:
        return None
    else:
        x1 = int(Point[0:para_len], 16)
        y1 = int(Point[para_len:len_2], 16)
        if l == len_2:
            z1 = 1
        else:
            z1 = int(Point[len_2:], 16)

        T6 = (z1 * z1) % int(canshu['q'], 16)
        T2 = (y1 * y1) % int(canshu['q'], 16)
        T3 = (x1 + T6) % int(canshu['q'], 16)
        T4 = (x1 - T6) % int(canshu['q'], 16)
        T1 = (T3 * T4) % int(canshu['q'], 16)
        T3 = (y1 * z1) % int(canshu['q'], 16)
        T4 = (T2 * 8) % int(canshu['q'], 16)
        T5 = (x1 * T4) % int(canshu['q'], 16)
        T1 = (T1 * 3) % int(canshu['q'], 16)
        T6 = (T6 * T6) % int(canshu['q'], 16)
        ecc_a3 = (int(canshu['a'], 16) + 3) % int(canshu['q'], 16)
        T6 = (ecc_a3 * T6) % int(canshu['q'], 16)
        T1 = (T1 + T6) % int(canshu['q'], 16)
        z3 = (T3 + T3) % int(canshu['q'], 16)
        T3 = (T1 * T1) % int(canshu['q'], 16)
        T2 = (T2 * T4) % int(canshu['q'], 16)
        x3 = (T3 - T5) % int(canshu['q'], 16)

        if (T5 % 2) == 1:
            T4 = (T5 + ((T5 + int(canshu['q'], 16)) >> 1) - T3) % int(canshu['q'], 16)
        else:
            T4 = (T5 + (T5 >> 1) - T3) % int(canshu['q'], 16)

        T1 = (T1 * T4) % int(canshu['q'], 16)
        y3 = (T1 - T2) % int(canshu['q'], 16)

        form = '%%0%dx' % para_len
        form = form * 3
        return form % (x3, y3, z3)

def _add_point(P1, P2):  # 点加函数，P2点为仿射坐标即z=1，P1为Jacobian加重射影坐标
        para_len=len(canshu['n'])
        len_2 = 2 * para_len
        l1 = len(P1)
        l2 = len(P2)
        if (l1 < len_2) or (l2 < len_2):
            return None
        else:
            X1 = int(P1[0:para_len], 16)
            Y1 = int(P1[para_len:len_2], 16)
            if (l1 == len_2):
                Z1 = 1
            else:
                Z1 = int(P1[len_2:], 16)
            x2 = int(P2[0:para_len], 16)
            y2 = int(P2[para_len:len_2], 16)

            T1 = (Z1 * Z1) % int(canshu['q'], 16)
            T2 = (y2 * Z1) % int(canshu['q'], 16)
            T3 = (x2 * T1) % int(canshu['q'], 16)
            T1 = (T1 * T2) % int(canshu['q'], 16)
            T2 = (T3 - X1) % int(canshu['q'], 16)
            T3 = (T3 + X1) % int(canshu['q'], 16)
            T4 = (T2 * T2) % int(canshu['q'], 16)
            T1 = (T1 - Y1) % int(canshu['q'], 16)
            Z3 = (Z1 * T2) % int(canshu['q'], 16)
            T2 = (T2 * T4) % int(canshu['q'], 16)
            T3 = (T3 * T4) % int(canshu['q'], 16)
            T5 = (T1 * T1) % int(canshu['q'], 16)
            T4 = (X1 * T4) % int(canshu['q'], 16)
            X3 = (T5 - T3) % int(canshu['q'], 16)
            T2 = (Y1 * T2) % int(canshu['q'], 16)
            T3 = (T4 - X3) % int(canshu['q'], 16)
            T1 = (T1 * T3) % int(canshu['q'], 16)
            Y3 = (T1 - T2) % int(canshu['q'], 16)

            form = '%%0%dx' % para_len
            form = form * 3
            return form % (X3, Y3, Z3)

def _convert_jacb_to_nor( Point):  # Jacobian加重射影坐标转换成仿射坐标
        para_len=len(canshu['n'])
        len_2 = 2 * para_len
        x = int(Point[0:para_len], 16)
        y = int(Point[para_len:len_2], 16)
        z = int(Point[len_2:], 16)
        z_inv = pow(
            z, int(canshu['q'], 16) - 2, int(canshu['q'], 16))
        z_invSquar = (z_inv * z_inv) % int(canshu['q'], 16)
        z_invQube = (z_invSquar * z_inv) % int(canshu['q'], 16)
        x_new = (x * z_invSquar) % int(canshu['q'], 16)
        y_new = (y * z_invQube) % int(canshu['q'], 16)
        z_new = (z * z_inv) % int(canshu['q'], 16)
        if z_new == 1:
            form = '%%0%dx' % para_len
            form = form * 2
            return form % (x_new, y_new)
        else:
            return None

def _kg(k, Point):  # kP运算
        Point = '%s%s' % (Point, '1')
        mask_str = '8'
        para_len=len(canshu['n'])
        for i in range(para_len - 1):
            mask_str += '0'
        mask = int(mask_str, 16)
        Temp = Point
        flag = False
        for n in range(para_len * 4):
            if (flag):
                Temp = _double_point(Temp)
            if (k & mask) != 0:
                if (flag):
                    Temp = _add_point(Temp, Point)
                else:
                    flag = True
                    Temp = Point
            k = k << 1
        return _convert_jacb_to_nor(Temp)

def gen_k(msg,x):

    h1=sha256(msg.encode()).digest()
    V=b'\x01'*32
    K=b'\x00'*32
    K=hmac.new(K,V+b'\x00'+x.encode()+h1,sha256).digest()
    V=hmac.new(K,V,sha256).digest()
    K=hmac.new(K,V+b'\x01'+x.encode()+h1,sha256).digest()
    V=hmac.new(K,V,sha256).digest()
    T=b''
    while len(T)<len(canshu['q']):
        V = hmac.new(K, V, sha256).digest()
        T+=V
    return hex(int.from_bytes(T, "big") % int(canshu['q'],16))[2:]

# 签名
def sign(msg_hash,K):
    para_len=len(canshu['n'])
    e=int(msg_hash,16)
    d=int(canshu['x'],16)
    k=int(K,16) # 随机数
    P1=_kg(k,canshu['g'])
    x = int(P1[0:para_len], 16)
    R = ((e + x) % int(canshu['n'],16))
    if R == 0 or R + k == int(canshu['n'],16):
        return None
    d_1 = pow(
        d + 1, int(canshu['n'],16) - 2, int(canshu['n'],16))
    S = (d_1 * (k + R) - R) % int(canshu['n'],16)
    if S == 0:
        return None
    else:
        return '%064x%064x' % (R, S)

def verify(Sign, data):
        # 验签函数，sign签名r||s，E消息hash，public_key公钥
        para_len=len(canshu['n'])
        r = int(Sign[0:para_len], 16)
        s = int(Sign[para_len:2*para_len], 16)
        e = int(data, 16)
        t = (r + s) % int(canshu['n'],16)
        if t == 0:
            return 0

        P1 = _kg(s, canshu['g'])
        P2 = _kg(t, canshu['U'])
        # print(P1)
        # print(P2)
        if P1 == P2:
            P1 = '%s%s' % (P1, 1)
            P1 = _double_point(P1)
        else:
            P1 = '%s%s' % (P1, 1)
            P1 = _add_point(P1, P2)
            P1 = _convert_jacb_to_nor(P1)

        x = int(P1[0:para_len], 16)
        return r == ((e + x) % int(canshu['n'], 16))


if __name__=="__main__":
    msg='1234'
    k=gen_k(msg,canshu['x'])


    print("="*5+"自制sm2"+"="*5)
    sign=sign(msg,k)
    print(f"消息:{msg.encode()}\nk is {k}\n签名：{sign}")
    print(f"检验签名与消息是否对应:{verify(sign,msg.encode())}")

    print("="*5+"系统sm2"+"="*5)
    sm2_crypt=sm2.CryptSM2(public_key=canshu['U'],private_key=canshu['x'])
    sign1=sm2_crypt.sign(msg.encode(),k)
    print(f"消息:{msg.encode()}\nk is {k}\n签名：{sign1}")
    print(f"检验签名与消息是否对应:{sm2_crypt.verify(sign1,msg.encode())}")

