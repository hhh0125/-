#include <iostream>;
#include<time.h>;
#include"AES.h";
using namespace std;


int main()
{
        string plain = "202100460145";
        string key_s = "202100460145000";
        string m,y;

        cout << "���ģ�" << plain << endl;
        cout << "��Կ��" << key_s << endl;
        m = AES_enc(plain, key_s);
         y= AES_dec(m, key_s);
         cout << "���ģ�" << m << endl;
         cout<<"���ܺ�����ģ�" << y << endl;
        return 0;
}

