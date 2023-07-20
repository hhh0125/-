Rho算法：
改进的生日攻击，改进生日攻击空间存储占用过多的缺点，边寻找碰撞边存储。
实现思路：
1）随机生成l比特的字符串，生成其hash值，记为temp。
2）定义a=temp，b=hash(hash(a))。
3）计算a_hash是否等于b_hash。不等，则计算a=hash(a),b=hash(hash(b))。
最多找到32bit

运行结果：
