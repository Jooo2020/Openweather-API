import requests
import pygame
import sys
import io

# === API Key und Ort ===
api_key = "4bf98e075d88a2d3e40ee0655aa76d74"
city = input("Welcher Ort: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=de"
response = requests.get(url)
data = response.json()

if response.status_code != 200:
    print("❌ Fehler: Ort nicht gefunden!")
    sys.exit()

# === Wetterdaten extrahieren ===
temp = data["main"]["temp"]
feels_like = data["main"]["feels_like"]
weather = data["weather"][0]["description"]
humidity = data["main"]["humidity"]
wind_speed = data["wind"]["speed"]

# Icon laden (direkt ohne Pillow)
icon_code = data["weather"][0]["icon"]
icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
icon_response = requests.get(icon_url)
icon_surface = pygame.image.load(io.BytesIO(icon_response.content))

# === Pygame Setup ===
pygame.init()
screen = pygame.display.set_mode((420, 300))
pygame.display.set_caption(f"Wetter in {city}")

# Fonts
font_big = pygame.font.SysFont("Segoe UI Emoji", 60)
font_small = pygame.font.SysFont("Segoe UI Emoji", 24)
font_city = pygame.font.SysFont("Arial", 28, bold=True)

# === Hauptanzeige ===
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((100, 150, 200))  # Hintergrundfarbe

    # Ortsname oben links
    city_text = font_city.render(city, True, (255, 255, 255))
    screen.blit(city_text, (90, 20))

    # Icon anzeigen
    screen.blit(icon_surface, (20, 20))

    # Temperatur groß
    temp_text = font_big.render(f"{temp:.0f}°C", True, (255, 255, 255))
    screen.blit(temp_text, (150, 80))

    # Wetterbeschreibung
    weather_text = font_small.render(weather.capitalize(), True, (255, 255, 255))
    screen.blit(weather_text, (20, 160))

    # Luftfeuchtigkeit und Wind
    humidity_text = font_small.render(f"💧 {humidity}% Luftfeuchtigkeit", True, (255, 255, 255))
    wind_text = font_small.render(f"💨 {wind_speed} m/s Wind", True, (255, 255, 255))
    screen.blit(humidity_text, (20, 200))
    screen.blit(wind_text, (20, 230))

    pygame.display.flip()

pygame.quit()
