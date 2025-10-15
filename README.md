# Wetter_API

Dieses Python-Programm zeigt aktuelle Wetterdaten und eine 3-Tage-Vorhersage für eine beliebige Stadt in einer grafischen Oberfläche mit Pygame an. Die Daten werden von der OpenWeatherMap-API bezogen.

## Features

- Eingabefeld für die Stadt (oben rechts)
- Anzeige von Temperatur, Wetterbeschreibung, Luftfeuchtigkeit und Windgeschwindigkeit
- Wetter-Icon und 3-Tage-Vorhersage mit eigenen Karten
- Farbige Darstellung je nach Wetterlage

## Voraussetzungen

- Python 3.x
- [pygame](https://www.pygame.org/)
- [requests](https://docs.python-requests.org/en/latest/)

Installiere die benötigten Pakete mit:

```sh
pip install pygame requests
```

## API-Key
-Ein API-Key von OpenWeatherMap ist erforderlich. Beim ersten Start wird der Key abgefragt und in key.txt gespeichert.