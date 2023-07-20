# 实验思路
PGP使用了公钥加密算法，用于会话密钥的加密；使用对称加密算法，用于消息的加密。

   加密时，使用sm2的公钥对会话密钥key进行加密，使用sm4对消息msg进行加密。
   
   解密时，先利用sm2的私钥求解出会话密钥，再使用sm4解密算法求解出消息msg。
   
## 流程如下：
![image](https://github.com/hhh0125/-/assets/139990267/42735280-df14-4dd0-9acb-d9a104658b0b)

# 运行结果
![image](https://github.com/hhh0125/-/assets/139990267/47761f89-59ab-4370-a5a9-9aebc39f0493)
