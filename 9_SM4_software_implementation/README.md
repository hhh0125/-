# SM4实现
SM4是一种分组密码算法。其分组长度为128bit，密钥长度也为128bit。
加密算法与密钥扩展算法均采用32轮非线性迭代结构，以32bit为单位进行加密运算。

# 具体细节
## 密钥扩展
1）输入128bit主密钥MK=(MK0,MK1,MK2,MK3)

2）定义密钥列表K[36]，密钥与系统参数异或。
![image](https://github.com/hhh0125/-/assets/139990267/0c19eebd-f1fb-48c1-ac47-719b26f3104f)

3）获取子密钥

![image](https://github.com/hhh0125/-/assets/139990267/305585b2-b9b3-48f1-b33b-96e9f12e118b)

## 明文处理
1）将128bit明文X=(X0,X1,X2,X3)	

2）定义明文列表X[36]

3）进行32轮迭代处理
![image](https://github.com/hhh0125/-/assets/139990267/17aaed13-0605-400a-a45e-7d433cbd0df4)

# 运行结果：
![image](https://github.com/hhh0125/-/assets/139990267/8bac5e20-a571-4492-a17e-a5cf5e765445)
