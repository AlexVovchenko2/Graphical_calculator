#pragma once
#include <SFML/Graphics.hpp>
#include <string>
#include <iostream>
#include <conio.h>
using namespace sf;


class TextField : public Transformable, public Drawable {
private:
	unsigned int m_size;
	Font m_font;
	std::string m_text;
	RectangleShape m_rect;
	bool m_hasfocus;
public:
	TextField(unsigned int maxChars) :
		m_size(maxChars),
		m_rect(sf::Vector2f(15 * m_size, 20)), // 15 pixels per char, 20 pixels height, you can tweak
		m_hasfocus(false)
	{
		m_font.loadFromFile("sansation.ttf"); // I'm working on Windows, you can put your own font instead
		m_rect.setOutlineThickness(2);
		m_rect.setFillColor(sf::Color::White);
		m_rect.setOutlineColor(sf::Color(127, 127, 127));
		m_rect.setPosition(this->getPosition());
	}
	const std::string getText()const;

	void setPosition(float, float);

	bool contains(Vector2f)const;

	void setFocus(bool);

	void handleInput(Event);

	void draw(RenderTarget& target, RenderStates states)const;
};

const std::string TextField::getText() const {
	return m_text;
}

void TextField::setPosition(float x, float y) {
	Transformable::setPosition(x, y);
	m_rect.setPosition(x, y);
}

bool TextField::contains(sf::Vector2f point) const {
	return m_rect.getGlobalBounds().contains(point);
}

void TextField::setFocus(bool focus) {
	m_hasfocus = focus;
	if (focus) {
		m_rect.setOutlineColor(sf::Color::Blue);
	}
	else {
		m_rect.setOutlineColor(sf::Color(127, 127, 127)); // Gray color
	}
}

void TextField::handleInput(sf::Event e) {				//doesn't work
	if (!m_hasfocus || e.type != sf::Event::TextEntered)
		return;

	if (e.text.unicode == 8) {   // Delete key
		m_text = m_text.substr(0, m_text.size() - 1);
	}
	else if (m_text.size() < m_size) {
		m_text += e.text.unicode;
	}
}

void TextField::draw(RenderTarget& target, RenderStates states)const {
	states.transform *= getTransform();
	target.draw(m_rect, states);
}