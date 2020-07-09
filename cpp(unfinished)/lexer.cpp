#include<iostream>
#include<string>
#include<map>
#include<ctype.h>
#include<cstdio>
namespace lexer{
	enum Tag{
		NONE=0,AND=256,BASIC,BREAK,DO,ELSE,EQ,FALSE,GE,ID,IF,INDEX,LE,MINUS,NE,NUM,OR,REAL,TEMP,TRUE,WHILE
	};
	class Token;
	class Lexer;
	class Num;
	class Word;
	class Real;
}
namespace symbols{
	
}

using namespace symbols;
using namespace lexer;

namespace lexer{
	class Token{
		public:
			int tag;
			Token():tag(Tag::NONE){
			}
			Token(int t):tag(t){
			}
			std::string toString(){
				std::string s;
				return s+(char)tag;
			}
	};
	class Num:public Token{
		public:
			int val;
			Num():Token(),val(0){
			}
			Num(int v):Token(Tag::NUM),val(v){
			}
			std::string toString()
			{
				std::string s;
				return s+std::to_string(val);
			}
	};
	class Word:public Token{
		public:
			std::string lexeme;
			Word():Token(),lexeme("none"){
			}
			Word(std::string s,int tag):Token(tag),lexeme(s){
			}
			std::string toString()
			{
				return lexeme;
			}
			static const Word And,Or,Eq,Ne,Le,Ge,Minus,True,False,Temp;
	};
	class Real:public Token{
		public:
			double val;
			Real():Token(),val(0.0){
			}
			Real(double v):Token(Tag::REAL),val(v){
			}
			std::string toString()
			{
				std::string s;
				return s+std::to_string(val);
			}
	};
	class Lexer{
		public:
			static int line;
			char peek;
			std::map<std::string,Word> words;
			void reserve(Word w){
				words.insert(std::pair<std::string,Word>(w.lexeme,w));
			}
			Lexer():peek(' '){
				reserve(Word("if",Tag::IF));
				reserve(Word("else",Tag::ELSE));
				reserve(Word("while",Tag::WHILE));
				reserve(Word("do",Tag::DO));
				reserve(Word("break",Tag::BREAK));
				reserve(Word::True);reserve(Word::False);
		//		reserve(Type::Int);reserve(Type::Char);
		//		reserve(Type::Bool);reserve(Type::Float);
			}
			void readch(){
				peek=getchar();
			}
			bool readch(char c){
				readch();
				if(peek!=c)	return false;
				peek=' ';
				return true;
			}
			Token* scan(){
				for(;;readch())
				{
					if(peek==' '||peek=='\t')continue;
					else if(peek=='\n')line++;
					else break;
				}
				switch(peek){
					case '&':{
						if(readch('&'))return new Word(Word::And);
						else return new Token('&');
						break;
					}
					case '|':{
						if(readch('|'))return new Word(Word::Or);
						else return new Token('|');
						break;
					}
					case '=':{
						if(readch('='))return new Word(Word::Eq);
						else return new Token('=');
						break;
					}
					case '!':{
						if(readch('='))return new Word(Word::Ne);
						else return new Token('!');
						break;
					}
					case '<':{
						if(readch('='))return new Word(Word::Le);
						else return new Token('<');
						break;
					}
					case '>':{
						if(readch('='))return new Word(Word::Ge);
						else return new Token('>');
						break;
					}
				}
				if(isdigit(peek)){
					int v=0;
					do{
						v=10*v+peek-'0';
						readch();
					}while(isdigit(peek));
					if(peek!='.') return new Num(v);
					double x=v,d=10.0;
					while(true)
					{
						readch();
						if(!isdigit(peek))
							break;
						x+=(peek-'0')/d;
						d*=10.0;
					}
					return new Real(x);
				}
				if(isalpha(peek))
				{
					std::string b;
					do{
						b+=peek;
						readch();
					}while(isalnum(peek));
					
					Word w=words[b];
					if(w.lexeme!="none")return new Word(w);
					Word *id=new Word(b,Tag::ID);
					words.insert(std::pair<std::string,Word>(b,*id));
					
					return id;
				}
				
				Token* tok=new Token(peek);
				peek=' ';
				return tok;
			}		
	};

	int Lexer::line=1;
	const Word Word::And("&&",Tag::AND),Word::Or("||",Tag::OR),
	           Word::Eq("==",Tag::EQ),Word::Ne("!=",Tag::NE),
			   Word::Le("<=",Tag::LE),Word::Ge(">=",Tag::GE),
			   Word::Minus("minus",Tag::MINUS),
			   Word::True("true",Tag::TRUE),
			   Word::False("false",Tag::FALSE),
			   Word::Temp("t",Tag::TEMP);
}
namespace symbols{
	class Env{
		public:
			
	};
}

int main()
{

	Lexer L;
	while(true)
	{
		Token* tmp=L.scan();
		std::cout<<tmp->tag<<std::endl;
		delete tmp;
	}
}
