import random
import sm3

def rho_method(l):

    temp=random.randint(0,2**(l+1)-1)

    a=temp
    a_hash=sm3.sm3_hash(a)

    b=int(a_hash,2)
    b_hash=sm3.sm3_hash(b)

    while a_hash[2:l]!=b_hash[2:l]:

        a=int(a_hash,2)
        a_hash=sm3.sm3_hash(a)

        b=int(b_hash,2)
        b_hash=sm3.sm3_hash(int(sm3.sm3_hash(b),2))

    return a_hash[:l],a,b

if __name__=='__main__':

    l=40
    print(f'寻找碰撞的空间大小：{l}bit')
    hash,x,y=rho_method(l)
    print(f"找到一组碰撞{x}，\n{y};\nhash值为{hash}")

