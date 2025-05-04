Analýza projektu – To-Do List aplikácia
1. Popis projektu

Projekt je jednoduchá webová aplikácia typu To-Do list, ktorá umožňuje používateľom:
- vytvárať vlastné úlohy, 
- editovať existujúce úlohy, 
- označovať úlohy ako splnené alebo zrušiť splnenie,
- mazať úlohy,
- filtrovať úlohy podľa prihláseného používateľa.

Aplikácia je rozdelená na dve vrstvy:

Simulačné prostredie (simulator/index.html) – kde úlohy môže používateľ plnohodnotne spravovať.

Prezentačné prostredie (frontend/index.html) – kde sa úlohy iba zobrazujú bez možnosti úprav.

2. Popis funkcionalít

Backend (Python, Flask + SQLite3, WebSocket):
- Uchováva úlohy v databáze (tasks.db).
- Poskytuje REST API pre manipuláciu s úlohami:
        - GET /ulohy – zobrazenie úloh pre daného používateľa,
        - POST /ulohy – pridanie novej úlohy,
        - PUT /ulohy/<id> – úprava existujúcej úlohy (zmena textu, popisu, termínu alebo splnenia),
        - DELETE /ulohy/<id> – vymazanie úlohy.
- Automaticky vysiela zmenu zoznamu úloh cez WebSocket (socketio.emit("update", tasks_json)).

Frontend (HTML, CSS, JavaScript):
- Prihlásenie pomocou mena používateľa.
- Zobrazenie zoznamu úloh aktuálne prihláseného používateľa.
- V simulačnej vrstve (simulator/index.html):
        - možnosť pridávať nové úlohy,
        - upravovať existujúce úlohy,
        - označiť úlohu ako splnenú/zrušiť splnenie,
        - vymazať úlohu.
- V prezentačnej vrstve (frontend/index.html):
        - iba zobrazenie aktuálnych úloh podľa používateľa.

3. Technické riešenie: prepojenie backendu a frontendu

HTTP požiadavky (fetch) sa používajú na komunikáciu s REST API:
- GET – načítanie úloh
- POST – pridanie úlohy
- PUT – aktualizácia úlohy (splnenie, editácia)
- DELETE – odstránenie úlohy

WebSocket pripojenie (socket.io) zabezpečuje:
- okamžitú aktualizáciu úloh na frontende bez manuálneho refreshu stránky,
- real-time synchronizáciu medzi všetkými klientmi (simulátor aj prezentačná vrstva).

Databáza SQLite (tasks.db) obsahuje tabuľku Task s atribútmi:
- id, text, description, due_date, user_name, done, created_at.

Bezpečnostné riešenia:
- povolenie CORS (flask_cors) pre bezpečné volania API z frontendu.