# 哈希树的生成
如下图所示，从下至上，由第i层生成第i+1层的结点；当第i层的结点为奇数时，最后一个结点直接等于第i+1层的某个结点。
![image](https://github.com/hhh0125/-/assets/139990267/be048c6c-36c9-4e23-877a-0956de26b327)
## 函数实现
```python
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
```
# 元素的检验
对于每个元素，要判断它是否属于该哈希树；

1）先判断它是否存在于消息列表中，查看哈希树中的叶子结点是否有该元素的hash值。若存在，进一步判断该元素是否属于该哈希树。

2）生成审计路径 audit path。以目标元素为起点，将生成根值所需的消息块取出，生成审计路径。如下图
![image](https://github.com/hhh0125/-/assets/139990267/f8b3f791-e2b0-42ae-ad0b-0e9af8ff570a)

3）根据审计路径，生成最终的根值，判断与根是否相等。相等，则该元素属于该哈希树。

4）检测函数输出是否正确。生成ele1，插入消息中，运行函数，应该输出“此元素在这颗哈希树中”；之后在哈希树中增添新消息块，运行函数，应该输出“此元素存在消息中，但不在这颗哈希树中！”；随机生成ele2，运行函数，应该输出“此元素不在消息中！”
## 函数实现
```python
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
```
# 运行结果
![image](https://github.com/hhh0125/-/assets/139990267/0496a45f-5296-404c-9b89-d2937dd70143)


