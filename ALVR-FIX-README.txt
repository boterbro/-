ALVR — исправление ошибки порта 8082 (error 10048)
==================================================

ОШИБКА: "error binding to 0.0.0.0:8082" / "Only one usage of each socket address..."

ЧТО ДЕЛАТЬ (один клик):
-----------------------
1. Скачайте оба файла в одну папку:
   - ALVR-FIX.bat
   - alvr-fix-port-8082.ps1

2. Дважды кликните ALVR-FIX.bat
   (Windows спросит права администратора — нажмите «Да»)

3. Скрипт сам:
   - закроет Steam, SteamVR и зависший ALVR
   - освободит порт 8082
   - запустит ALVR Dashboard

4. В ALVR нажмите «Launch SteamVR»
5. На Quest 3 откройте приложение ALVR и подключитесь

Если не помогло — перезагрузите ПК и снова запустите ALVR-FIX.bat

Ссылка на файлы в репозитории:
https://github.com/boterbro/-/tree/cursor/alvr-port-8082-fix-a4d9
