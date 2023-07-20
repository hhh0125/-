import sm3

def birth_attack(l):
    # 需要穷举的原像空间
    num=int(2**(l/2))
    # 以hash值为索引
    hash={}
    for i in range(num):
        # hash前l比特
        i_hash = sm3.sm3_hash(i)[2:l]
        index=int(i_hash,2)
        if index not in hash:
            hash[index]=i
        else:
            return i_hash,i,hash[index]
    return None


if __name__=='__main__':

    l=38
    print(f'寻找碰撞的空间大小：{l}bit')
    result=birth_attack(l)
    if result is not None:
        hash,x,y=result
        print(f"找到一组碰撞{x}，{y};hash值为{hash}")
    else:
        print('未发现碰撞')



