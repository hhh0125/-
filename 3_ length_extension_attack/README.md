# SM3的消息填充：
   假设消息m 的长度为l 比特。首先将比特“1”添加到消息的末尾，再添加k 个“0”， k是满足l + 1 + k ≡ 448mod512 的最小的非负整数。然后再添加一个64位比特串，该比特串是长度l的二进制表示。填充后的消息m′ 的比特长度为512的倍数。
## padding函数的实现
```python
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
```
# 哈希长度扩展攻击：
当知道hash(m)的值及m长度的情况下，可以推算出hash(m||padding||m’)。在这里m’是任意数据,padding是m后的填充字节。
## 实现思路：
1）先定义message，用sm3算出其hash值，记为msg_hash。

2）再定义extend，为扩展的消息。利用长度扩展攻击，把msg_hash作为加密的初始向量，去加密extend，获得extend_hash。

3）作为比较，计算message+padding+extend的hash值，记为new_msg_hash。

如果extend_hash等于new_msg_hash，则长度扩展攻击成功。
# 运行结果：
![image](https://github.com/hhh0125/-/assets/139990267/c5ca9762-148b-41cd-8ea8-43dcf0d53daf)
