#include <iostream>;
#include<time.h>;
#include"AES.h";
using namespace std;


int main()
{
        string plain = "202100460145";
        string key_s = "202100460145000";
        string m,y;

        cout << "明文：" << plain << endl;
        cout << "密钥：" << key_s << endl;
        m = AES_enc(plain, key_s);
         y= AES_dec(m, key_s);
         cout << "密文：" << m << endl;
         cout<<"解密后的明文：" << y << endl;
        return 0;
}

