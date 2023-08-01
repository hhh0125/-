# 创新创业实践作业
* 姓名：谭羽彤
* 学号：202100460145
## 项目完成情况
### project1
* 实现方式：python
* 运行环境：pycharm
* 实现思路：
    
  1）遍历0到2^(l/2)，将其的hash值，以键值对的形式，存在字典中。
  
  2）若找到相同hash值则输出。
  
  3）字符串越大，消耗的时间越久。我最多找到48bit。
### project2
* 实现方式：python
* 运行环境：pycharm
*  实现思路：
  
  1）随机生成l比特的字符串，生成其hash值，记为temp。
  
  2）定义a=temp，b=hash(hash(a))。
  
  3）计算a_hash是否等于b_hash。不等，则计算a=hash(a),b=hash(hash(b))。
  
  最多找到32bit
### project3
* 实现方式：python
* 运行环境：pycharm
* 实现思路：
  
  1）先定义message，用sm3算出其hash值，记为msg_hash。
  
  2）再定义extend，为扩展的消息。利用长度扩展攻击，把msg_hash作为加密的初始向量，去加密extend，获得extend_hash。
  
  3）作为比较，计算message+padding+extend的hash值，记为new_msg_hash。
  
  如果extend_hash等于new_msg_hash，则长度扩展攻击成功。

### project4
* 实现方式：c++
* 运行环境：vs
* 实现效果：
  
  通过循环展开，可以由0.149s缩减到0.130s，加速了12.75%，效果并不明显。
### project5
* 实现方式：python
* 运行环境：pycharm
* 实现思路：
  
   参考RFC6962中的审计路径，以检验某元素是否属于该哈希树
### project8
* 实现方式：c++
* 运行环境：vs
* 实现思路：

  在vs上使用头文件arm64_neon.h。头文件中有相应的硬件指令可以使用，如单轮加密（包含轮密钥加，字节代换，行移位）、列混合、单轮解密、逆列混合。只需将基本的AES加密流程，换成相应的ARM指令函数即可。

### project9
* 实现方式：c++和python
* 运行环境：vs和pycharm
* 实现思路：

  AES采用CBC加密模式，利用c++实现；SM4则是使用python实现。  
### project11
* 实现方式：python
* 运行环境：pycharm
* 实现思路：
  
  在RFC6979中主要讲解如何选取随机数k，因此本次实验的重点在随机数k上的选取。
### project14
* 实现方式：python
* 运行环境：pycharm
* 实现思路：
  
  PGP使用了公钥加密算法，用于会话密钥的加密；使用对称加密算法，用于消息的加密。

   加密时，使用sm2的公钥对会话密钥key进行加密，使用sm4对消息msg进行加密。
  
   解密时，先利用sm2的私钥求解出会话密钥，再使用sm4解密算法求解出消息msg。
  
### project17
