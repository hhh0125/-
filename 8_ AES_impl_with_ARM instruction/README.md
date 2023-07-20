# 实现思路
  本次实验，在vs上使用头文件arm64_neon.h。有如下硬件指令供我们使用
单轮加密（包含轮密钥加，字节代换，行移位）、列混合、单轮解密、逆列混合。
对比基本的AES加密流程，基于ARM指令的AES加密改为如下方案：
![image](https://github.com/hhh0125/-/assets/139990267/89af1f78-ddbe-42d0-9466-486a1fb51e97)

# ARM指令对应的C语言函数如下：
```c++
// 单轮加密
uint8x16_t vaeseq_u8(uint16x8_t data, uint8x16_t key);

//单论解密
uint8x16_t vaesdq_u8(uint8x16_t data, uint8x16_t key);

//列混合
uint8x16_t vaesmcq_u8(uint8x16_t  data);

//逆列混合
uint8x16_t vaesimcq_u8(uint8x16_t data);
```
