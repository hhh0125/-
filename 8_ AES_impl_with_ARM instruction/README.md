本次实验，在vs上使用头文件arm64_neon.h。如下硬件指令供我们使用
单轮加密（包含轮密钥加，字节代换，行移位）、列混合、单轮解密、逆列混合。
对比基本的AES加密流程，基于ARM指令的AES加密改为如下方案：

ARM指令对应的C语言函数如下：
1.// 单轮加密  
2.uint8x16_t vaeseq_u8(uint16x8_t data, uint8x16_t key);  
3.  
4.//单轮解密  
5.uint8x16_t vaesdq_u8(uint8x16_t data, uint8x16_t key);  
6.  
7.//列混合  
8.uint8x16_t vaesmcq_u8(uint8x16_t  data);  
9.  
10.//逆列混合  
11.uint8x16_t vaesimcq_u8(uint8x16_t data); 