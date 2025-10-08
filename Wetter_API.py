import requests
import pygame
import sys
import io
from datetime import datetime

# === API Key ===
api_key = "4bf98e075d88a2d3e40ee0655aa76d74"

# === Pygame Setup ===
pygame.init()
screen = pygame.display.set_mode((650, 450))
pygame.display.set_caption("Wetteranzeige")

font_big = pygame.font.SysFont("Segoe UI Emoji", 60)
font_small = pygame.font.SysFont("Segoe UI Emoji", 24)
font_city = pygame.font.SysFont("Arial", 28, bold=True)
font_input = pygame.font.SysFont("Arial", 22)

# === Farben ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (80, 150, 220)

# === Variablen ===
city_input = ""
current_city = ""  # ← wird nur nach erfolgreicher Eingabe geändert
input_active = True
input_cleared = False
data_loaded = False

# Platzhalter für Wetterdaten
temp = weather = humidity = wind_speed = None
icon_surface = None
forecast_list = []
forecast_surfaces = []

# === Hilfsfunktionen ===
def weather_color(desc):
    desc = desc.lower()
    if "regen" in desc:
        return (100, 149, 237)
    elif "sonnig" in desc or "klar" in desc:
        return (255, 223, 100)
    elif "wolken" in desc:
        return (169, 169, 169)
    else:
        return (200, 200, 200)

def load_weather_data(city):
    global temp, weather, humidity, wind_speed, icon_surface, forecast_list, forecast_surfaces, data_loaded

    try:
        # === Aktuelles Wetter ===
        url_now = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=de"
        response_now = requests.get(url_now)
        data_now = response_now.json()

        if response_now.status_code != 200:
            return False

        temp = data_now["main"]["temp"]
        weather = data_now["weather"][0]["description"]
        humidity = data_now["main"]["humidity"]
        wind_speed = data_now["wind"]["speed"]
        icon_code = data_now["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        icon_surface = pygame.image.load(io.BytesIO(icon_response.content))

        # === 3-Tage-Vorhersage ===
        url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=de"
        response_forecast = requests.get(url_forecast)
        data_forecast = response_forecast.json()

        if response_forecast.status_code != 200:
            return False

        forecast_list = []
        today = datetime.now().date()
        added_days = 0
        for item in data_forecast["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            if dt.date() > today:
                if not any(f['date'] == dt.date().strftime("%a %d.%m") for f in forecast_list):
                    if abs(dt.hour - 12) <= 1:
                        forecast_list.append({
                            "date": dt.strftime("%a %d.%m"),
                            "temp": item["main"]["temp"],
                            "weather": item["weather"][0]["description"],
                            "icon": item["weather"][0]["icon"]
                        })
                        added_days += 1
            if added_days >= 3:
                break

        # Icons laden
        forecast_surfaces = []
        for f in forecast_list:
            icon_url = f"http://openweathermap.org/img/wn/{f['icon']}@2x.png"
            icon_resp = requests.get(icon_url)
            forecast_surfaces.append(pygame.image.load(io.BytesIO(icon_resp.content)))

        data_loaded = True
        return True

    except Exception as e:
        print("Fehler:", e)
        return False

# === Hauptloop ===
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if input_active:
            if event.type == pygame.KEYDOWN:
                # Erste Taste → Eingabe löschen (einmalig)
                if not input_cleared:
                    city_input = ""
                    input_cleared = True

                if event.key == pygame.K_RETURN:
                    if city_input.strip():
                        # Erst prüfen, ob gültig
                        if load_weather_data(city_input.strip()):
                            current_city = city_input.strip()  # ← Ort erst hier aktualisieren
                        else:
                            city_input = "❌ Ungültig!"
                            data_loaded = False
                        input_active = False
                        input_cleared = False
                    else:
                        city_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    city_input = city_input[:-1]
                else:
                    if len(city_input) < 30:
                        city_input += event.unicode

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Klick ins Eingabefeld oben rechts
                if 400 < x < 630 and 20 < y < 50:
                    input_active = True
                    input_cleared = False  # ← Noch nicht löschen!
                    # alter Text bleibt sichtbar

    screen.fill(BLUE)

    # === Eingabefeld (oben rechts) ===
    input_box = pygame.Rect(400, 20, 230, 35)
    pygame.draw.rect(screen, WHITE, input_box, border_radius=6)
    text_surface = font_input.render(city_input or "Ort eingeben...", True, BLACK)
    screen.blit(text_surface, (input_box.x + 8, input_box.y + 6))
    pygame.draw.rect(screen, GRAY, input_box, 2, border_radius=6)

    # === Wetteranzeige ===
    if data_loaded:
        city_text = font_city.render(current_city, True, (255, 255, 255))
        screen.blit(city_text, (90, 20))
        screen.blit(icon_surface, (20, 20))
        temp_text = font_big.render(f"{temp:.0f}°C", True, (255, 255, 255))
        screen.blit(temp_text, (150, 80))
        weather_text = font_small.render(weather.capitalize(), True, (255, 255, 255))
        screen.blit(weather_text, (20, 160))
        humidity_text = font_small.render(f"💧 {humidity}% Luftfeuchtigkeit", True, (255, 255, 255))
        wind_text = font_small.render(f"💨 {wind_speed} m/s Wind", True, (255, 255, 255))
        screen.blit(humidity_text, (20, 200))
        screen.blit(wind_text, (20, 230))

        # 3-Tage-Vorhersage
        x_start = 20
        y_start = 270
        card_width = 180
        card_height = 150
        padding = 20

        for i, f in enumerate(forecast_list):
            card_x = x_start + i * (card_width + padding)
            card_y = y_start
            pygame.draw.rect(screen, weather_color(f['weather']), (card_x, card_y, card_width, card_height), border_radius=12)
            date_text = font_small.render(f['date'], True, (0, 0, 0))
            screen.blit(date_text, (card_x + 10, card_y + 10))
            screen.blit(forecast_surfaces[i], (card_x + 50, card_y + 30))
            temp_text = font_small.render(f"{f['temp']:.0f}°C", True, (0, 0, 0))
            screen.blit(temp_text, (card_x + 10, card_y + 90))
            weather_text = font_small.render(f['weather'].capitalize(), True, (0, 0, 0))
            screen.blit(weather_text, (card_x + 10, card_y + 115))

    pygame.display.flip()

pygame.quit()
