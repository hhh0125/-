SM3的消息填充：
   假设消息m 的长度为l 比特。首先将比特“1”添加到消息的末尾，再添加k 个“0”， k是满足l + 1 + k ≡ 448mod512 的最小的非负整数。然后再添加一个64位比特串，该比特串是长度l的二进制表示。填充后的消息m′ 的比特长度为512的倍数。
哈希长度扩展攻击：
当知道hash(m)的值及m长度的情况下，可以推算出hash(m||padding||m’)。在这里m’是任意数据,padding是m后的填充字节。
实现思路：
1）先定义message，用sm3算出其hash值，记为msg_hash。
2）再定义extend，为扩展的消息。利用长度扩展攻击，把msg_hash作为加密的初始向量，去加密extend，获得extend_hash。
3）作为比较，计算message+padding+extend的hash值，记为new_msg_hash。
如果extend_hash等于new_msg_hash，则长度扩展攻击成功。
运行结果：