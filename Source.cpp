#pragma warning(disable:4996)
#include <SFML/Graphics.hpp>
#include <Windows.h>
#include <sstream>
#include <fstream>
#include "Button.h"
#include "TextField.h"
using namespace sf;

int main() {
	HDC hDCScreen = GetDC(NULL);
	int refresh = GetDeviceCaps(hDCScreen, VREFRESH);
	ReleaseDC(NULL, hDCScreen);
	ShowWindow(GetConsoleWindow(), SW_HIDE);
	RenderWindow window({ 500, 500 }, "Calcultor", Style::Close);
	window.setFramerateLimit(refresh);
	window.setVerticalSyncEnabled(true);

	

	const unsigned int fsize = 20;
	const unsigned int nchars = 20;
	const Vector2f bar_position = Vector2f(30, 30);
	char buff[nchars];

	TextField tf(nchars);
	tf.setPosition(bar_position.x, bar_position.y);
	RectangleShape shadow_rect(Vector2f(15 * nchars, fsize));
	shadow_rect.setPosition(Vector2f(62, 57));

	
	
	// create a font
	Font font;
	// Load it from a file
	if (!font.loadFromFile("sansation.ttf")) {
		std::cout << "Error loading font\n";
	}

	Cursor cursor;
	Event event;
	while (window.isOpen()) {
		
		
		while (window.pollEvent(event)) {
			switch (event.type) {
			case Event::Closed:
				window.close();
				break;
			case Event::Resized: {
				float w = static_cast<float>(event.size.width);
				float h = static_cast<float>(event.size.height);
				window.setView(View(Vector2f(w / 2.0, h / 2.0), Vector2f(w, h)));
				break;
			}
			case Event::MouseButtonReleased:
				tf.setFocus(false);
				if (cursor.loadFromSystem(sf::Cursor::Arrow))
					window.setMouseCursor(cursor);
				if (shadow_rect.getGlobalBounds().contains(Vector2f(Mouse::getPosition(window)))) {
					tf.setFocus(true);
					if (cursor.loadFromSystem(sf::Cursor::Text))
						window.setMouseCursor(cursor);
				}
				break;
			case Event::KeyPressed:
				if (Keyboard::isKeyPressed(Keyboard::Enter)) {
					tf.setFocus(false);
					std::ofstream fout("input.txt");
					fout << tf.getText();
					fout.close();

					system("calculatorcopy.py");  //calling python script

					std::ifstream fin("output.txt");
					
					fin.getline(buff, nchars);
					fin.close();
					
					std::cout << buff << std::endl;
				}
			default:
				tf.handleInput(event);
				break;
			}
		}

		

		std::ostringstream ss; //string buffer to convert numbers to string
		ss << tf.getText();

		//set up text properties
		Text atext;
		atext.setFont(font);
		atext.setCharacterSize(fsize);
		atext.setStyle(Text::Bold);
		atext.setColor(Color::Red);
		atext.setPosition(Vector2f(62, 57));
		atext.setString(ss.str());

		std::ostringstream ss2; //string buffer to convert numbers to string
		if(buff[0] != (char)-52 and buff[0] != (char)-72) { ss2 << buff; }
		else { ss2 << ""; }
		
		
		//strdup(ss2.str().c_str())
		Text res;
		res.setFont(font);
		res.setCharacterSize(fsize);
		res.setStyle(Text::Bold);
		res.setColor(Color::Red);
		res.setPosition(Vector2f(100, 100));
		res.setString(ss2.str());
		

		window.clear();
	
		window.draw(tf);

		window.draw(atext);
		
		window.draw(res);
		
		window.display();
	}
}
