# Vitability v2

Jednoduchý statický web pre Vitability.

## Technológie

- HTML
- CSS
- minimum vanilla JavaScriptu
- JSON pre aktuálne hodiny
- GitHub Pages

## Aktuálne hodiny

Jana môže meniť súbor:

`data/aktualne.json`

Každá hodina má:

- `day` – deň
- `time` – čas
- `name` – názov hodiny
- `place` – miesto
- `note` – krátka poznámka, môže zostať prázdna

## Lokálne spustenie

Kvôli načítaniu JSON cez `fetch()` nestačí otvoriť `index.html` dvojklikom. Spusti jednoduchý lokálny HTTP server, napríklad:

```bash
python3 -m http.server 8000
```

Potom otvor:

`http://localhost:8000`
