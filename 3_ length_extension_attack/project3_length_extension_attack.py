from gmssl import sm3


def padding(msg,len1):

    reserve1 = len1 % 64       # 字节数模64，得到分组数后的余数
    msg.append(0x80)           # 消息后加1比特
    reserve1 = reserve1 + 1    # 消息后加1比特

    # 56-64, add 64 byte
    # 8字节存消息长度，不足8字节则重新加个分组
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)      # 填0

    # 将消息长度加入到列表中
    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7-i])

    return msg


def len_extension(msg_hash,extent,msg_len):

    H=[]
    for i in range(8):
        H.append(int(msg_hash[i*8:i*8+8],16))

    extent_list = [i for i in extent]

    extent_list=padding(extent_list,msg_len+len(extent_list))

    group_count=round(len(extent_list)/64)
    B = []
    for i in range(0, group_count):
        B.append(extent_list[i*64:(i+1)*64])

    V = []
    # 将原消息作为iv
    V.append(H)
    for i in range(0, group_count):
        V.append(sm3.sm3_cf(V[i], B[i]))

    y = V[i+1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result

if __name__=='__main__':
    message=b'123'
    extend=b'12'
    msg_list=[i for i in message]
    extend_list=[i for i in extend]
    # 旧消息的hash值
    msg_hash=sm3.sm3_hash(msg_list)
    # 旧消息的填充后列表
    new_msg_list=padding(msg_list[:],len(msg_list))
    # 旧消息加扩展消息后的列表
    new_msg_list.extend(extend_list)
    # 新消息的hash值
    new_hash=sm3.sm3_hash(new_msg_list)
    # 利用长度扩展获得的hash
    extend_hash=len_extension(msg_hash,extend,len(msg_list))

    print("新消息的hash",new_hash)
    print('长度扩展结果',extend_hash)
    if new_hash==extend_hash:
        print("长度扩展攻击成功！")
    else:
        print("失败！")







