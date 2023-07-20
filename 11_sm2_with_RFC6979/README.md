# 实验思路
在RFC6979中主要讲解如何选取随机数k，因此本次实验的重点在随机数k上的选取。
## 参数说明
1）n  g的阶

2）q  一个素数，至少160bit

3）g  E上一个点，生成元

4）x  私钥

5）U  公钥 xG

## 生成签名
记qlen=H(m);

1）将H(m)转变为整数模q，记为h。

2）生成一个随机数k ([1,q-1])

3）计算r，把kG的x坐标数转变为整数，模q，记为r。

4）计算s，
![image](https://github.com/hhh0125/-/assets/139990267/ea5add81-a7d4-4c46-aaab-c55516e59604)


(r,s)即为签名。
### 签名函数实现
```python
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
```
##  生成随机数k
1）HMAC

HMAC是使用哈希函数和密钥的消息认证码结构。这里我们使用的HMAC哈希函数与签名生成之前用于处理输入消息的哈希函数相同。本次实验中HMAC采用sha256，记hlen为输出的比特长。

2）生成随机数k

对于给定消息m，采取以下步骤：

a.h1=H(m)   h1是hlen长的序列

b.定义V=0x01 0x01......0x01；V的长度等于8*ceil(hlen/8)，为32。

c.定义K=0x00 0x00......0x00；K的长度等于8*ceil(hlen/8)，为32。

d.定义K=HMAC_K(V|| 0x00|| x || h1)

e.记V=HMAC_K(V)

f.K=HMAC_K(V|| 0x01|| x || h1)

g.V=HMAC_K(V)

h.用以下算法找到合适的k值：

	1.设T是一个空序列，长度记作tlen。
 
	2.当tlen<qlen，做以下循环：
 
		V=HMAC_K(V)
  
		T=T||V
  
	3.k=bits2int(T)；如果k不属于[1,q-1]，则：
 
		K=HMAC_K(V||0x00)
 
		V=HMAC_K(V)
 
直到找到合适的k值。
### 随机数函数实现
```python
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
```
# 运行结果

 作为对比，我调用了gmssl库中的sm2，进行检验自己编写的函数是否正确。


![image](https://github.com/hhh0125/-/assets/139990267/208f2b03-398b-4225-b52b-4829db03d040)




































