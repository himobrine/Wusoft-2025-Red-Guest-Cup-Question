#include <iostream>
using namespace std;

void flag_checker(int v, int w,int x,int y,int z); 

int main(){
	int v,w,x,y,z;
	cout << "Input 5 random number and check your luck ;)" << endl;
	cout << "Num1: ";
	cin >> v;
	cout << "Num2: ";
	cin >> w;
	cout << "Num3: ";
	cin >> x;
	cout << "Num4: ";
	cin >> y;
	cout << "Num5: ";
	cin >> z;
	cout << endl;
	flag_checker(v,w,x,y,z);
}


void flag_checker(int v,int w, int x, int y, int z){
	if ((v * 23 + w * -32 + x * 98 + y * 55 + z * 90 == 333322) &&
		(v * 123 + w * -322 + x * 68 + y * 67 + z * 32 == 707724) &&
		(v * 266 + w * -34 + x * 43 + y * 8 + z * 32 == 1272529) &&
		(v * 343 + w * -352 + x * 58 + y * 65 + z * 5 == 1672457) &&
		(v * 231 + w * -321 + x * 938 + y * 555 + z * 970 == 3372367)){
			cout << "Congratulations, Here is your flag:\n";
			cout << "flag{" << v << "_" << w << "_" << x << "_" << y << "_" << z << "}" << endl;
		}
		else{
			cout << "\nSeems your luck is not in favor right now!\nBetter luck next time!" << endl;
		}

}
