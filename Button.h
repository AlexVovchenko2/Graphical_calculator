#pragma once
#include <SFML/Graphics.hpp>
#include <string>
#include <iostream>
using namespace sf;

class Button {
private:
	Vector2f size;
	Vector2f coordinates;
	RenderWindow* window;
	Color color;
	Color color2;
public:
	Button(Vector2f size, Vector2f coordinates, RenderWindow* window, Color color, Color color2) {
		this->size = size;
		this->coordinates = coordinates;
		this->window = window;
		this->color = color;
		this->color2 = color2;
	}

	bool draw() {
		RectangleShape button(size);
		button.setPosition(coordinates);

		if (Mouse::isButtonPressed(sf::Mouse::Left) &&
			button.getGlobalBounds().contains(Mouse::getPosition(*window).x, Mouse::getPosition(*window).y)) {
			button.setFillColor(color2);
			(*window).draw(button);
			return true;
		}
		else {
			button.setFillColor(color);
			(*window).draw(button);
			return false;
		}
	}
};