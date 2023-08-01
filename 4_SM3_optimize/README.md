# 循环展开
  注意到sm3中有多个循环，将其展开。如将二进制转换为十进制的函数中，将其展开为1x4，减少循环次数；在消息扩展函数中，生成64位W’值时，彼此没有依赖关系，也可将其展开为1x4。
最终通过循环展开，可以由0.149s缩减到0.130s，加速了12.75%，效果并不明显。
# 代码比较：
```c++
	/*
	for (int i = 0; i < 64; i++)	//根据公式生成64位W'值
	{
		res += XOR(res.substr(i * 8, 8), res.substr((i + 4) * 8, 8));
	}
	*/

	//循环展开
	string res1, res2, res3, res4;
	for (int i = 0; i < 64; i+=4)
	{
		res1= XOR(res.substr(i * 8, 8), res.substr((i + 4) * 8, 8));
		res2 = XOR(res.substr((i+1) * 8, 8), res.substr((i+1 + 4) * 8, 8));
		res3= XOR(res.substr((i+2) * 8, 8), res.substr((i+2 + 4) * 8, 8));
		res4= XOR(res.substr((i+3) * 8, 8), res.substr((i+3 + 4) * 8, 8));

		res = res + res1 + res2 + res3 + res4;
	}
```
