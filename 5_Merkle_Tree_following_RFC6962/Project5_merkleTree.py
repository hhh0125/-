
from _sha256 import sha256
import random
import string
import math

# 简化sha256
def sha(msg):
    return sha256(msg.encode()).hexdigest()


# 随机生成消息块
def gen_msg(len):
    msg=[]
    for i in range(len):
        # 6个为一组
        block=[random.choice(string.ascii_letters) for i in range(6)]
        msg.append("".join(block))
    return msg

def gen_mrk(msg):

    length = len(msg)
    # merkle tree 深度
    depth=math.ceil(math.log2(length)+1)
    # 生成叶子结点
    mrk=[[sha(i) for i in msg]]

    # 从下往上生成merkle tree
    for i in range(depth-1):
        # 第i层的结点数
        node_count=len(mrk[i])
        # 生成第i+1层的结点
        temp=[sha(mrk[i][j*2]+mrk[i][j*2+1]) for j in range(node_count//2)]
        # 当结点数为奇数时，直接放入上一层
        if node_count%2!=0:
            temp.append(mrk[i][-1])
        mrk.append(temp)
    return mrk

def proof(ele,mrk,root):
    ele_hash=sha(ele)
    if ele_hash in mrk[0]:
        ele_index=mrk[0].index(ele_hash)            # 找到指定元素的索引
    else:
        return "此元素不在消息中！"
    depth=len(mrk)
    audit_path=[]       # 审计路线
    for i in range(depth-1):
        if ele_index%2==0 and len(mrk[i])-1!=ele_index:          # 左节点且不是最后的结点
            # 在审计路线中加入指定元素的右兄弟，并标明指定元素为左结点
            audit_path.append(('l',mrk[i][ele_index+1]))
        else:
            # 在审计路线中加入指定元素的左兄弟，并标记指定元素为右结点
            audit_path.append(('r',mrk[i][ele_index-1]))
        # 更新结点值
        ele_index=int(ele_index/2)
    #print("审计路径：",audit_path)
    for i in audit_path:
        if i[0]=="l":
            ele_hash=sha(ele_hash+i[1])
        else:
            ele_hash=sha(i[1]+ele_hash)
        #print("hash：",ele_hash)
    if ele_hash==root:
        return ("此元素在这颗哈希树中！")
    else:
        return ("此元素存在消息中，但不在这颗哈希树中！")

if __name__=='__main__':

    length=10000
    msg=gen_msg(length)
    # 生成消息块
    ele1="esdfed"
    index=random.randint(0,length)
    msg[index]=ele1   # 插入消息块,用于证明元素在消息中
    print("消息：",msg)
    ele2="sfgheg"   # 用于检验元素不在消息中
    mrk=gen_mrk(msg)
    #print(mrk)
    root=mrk[-1][0]
    print("消息块:", ele1, proof(ele1, mrk,root))
    print("哈希树更新后")
    msg+=gen_msg(10)
    mrk=gen_mrk(msg)
    print("消息块:", ele1, proof(ele1, mrk,root))
    print("消息块:", ele2, proof(ele2, mrk,root))