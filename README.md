# 生日攻击：
如果对l-bit的串进行攻击，根据生日攻击，则进行2^(l/2)次搜索能以较高概率找到碰撞。
# 实现思路：
1）遍历0到2^(l/2)，将其的hash值，以键值对的形式，存在字典中。
2）若找到相同hash值则输出。
3）字符串越大，消耗的时间越久。最多找到48bit。

# 运行结果：
![image](https://github.com/hhh0125/-/assets/139990267/02fb1751-3075-417c-9652-357fb851651e)

