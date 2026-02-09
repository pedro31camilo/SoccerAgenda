from playwright.sync_api import sync_playwright, Playwright
from rich import print
import json
import csv
import os
import re
import unicodedata
from datetime import date as Date, datetime, timedelta

def dateFixing(date_str):
    months = {
        'jan.' : '01',
        'fev.': '02',
        'mar.': '03',
        'abr.': '04',
        'mai.': '05',
        'jun.': '06',
        'jul.': '07',
        'ago.': '08',
        'set.': '09',
        'out.': '10',
        'nov.': '11',
        'dez.': '12'}
    date_parts = date_str.split(', ')
    day = date_parts[1].split(' ')
    day_num = day[0]
    day_mo = months[day[1].lower()]
    return f"{Date.today().year}-{day_mo}-{day_num.zfill(2)}"


def run(playwright: Playwright):
    # garante que a pasta para guardar os CSVs existe
    os.makedirs('teamAgenda', exist_ok=True)
    base_url = 'https://www.espn.com.br'
    start_url = base_url + "/futebol/times"
    chrome = playwright.chromium
    browser = chrome.launch(headless=True)
    page = browser.new_page()
    page.goto(start_url)

    ligas = {}
    times= {}
    calendars = {}

    while True:
        for link in page.locator("select.dropdown__select option.dropdown__option").all():
            data_url = link.get_attribute("data-url")
            if data_url and data_url not in ligas:
                ligas[link.inner_text().strip()] = base_url + data_url
            else:
                break
        for league in ligas.values():
            new_page = browser.new_page()
            new_page.goto(league)
            for team in new_page.locator("div.pl3 div.TeamLinks__Links span.TeamLinks__Link.n9.nowrap a.AnchorLink", has_text="Calendário").all():
                calendar_url = team.get_attribute("href")
                team_name = team.locator("xpath=..").locator("xpath=..").locator("xpath=..").locator("a.AnchorLink").first.inner_text().strip()
                times[team_name] = base_url + calendar_url
        for team_name, calendar_url in times.items():
            team_page = browser.new_page()
            team_page.goto(calendar_url)
            for game in team_page.locator("tr.Table__TR.Table__TR--sm.Table__even").all():
                game_data = game.inner_text().strip().split("\n")
                game_data = [item.strip().replace("\t", " ") for item in game_data if item.strip()]
                game_day = dateFixing(game_data[0])
                print(game_data)
                if game_data[4] == "LIVE": continue
                game_hour_aux = datetime.strptime(game_data[-1].split(" ")[0], "%H:%M") if game_data[-1].split(" ")[0] != "A" else datetime.strptime("00:00", "%H:%M")
                game_end_hour_aux = game_hour_aux + timedelta(hours=2) if game_data[-1].split(" ")[0] != "A" else datetime.strptime("00:00", "%H:%M")
                competition = " ".join(game_data[-1].split(" ")[1: ]) if game_data[-1].split(" ")[0] != "A" else " ".join(game_data[-1].split(" ")[2: ])
                event = f"{game_data[1]} vs {game_data[3]} - {competition}"
                event_dict = {
                    "Subject": event,
                    'Start Date': game_day,
                    'End Date': game_day,
                    'Start Time':game_hour_aux.strftime("%H:%M"),
                    'End Time': game_end_hour_aux.strftime("%H:%M"),
                }
                event_dict['All Day Event'] = 'True' if event_dict['Start Time'] == "00:00" else "False"
                calendars[team_name].append(event_dict) if team_name in calendars else calendars.setdefault(team_name, [event_dict])
            team_page.close()
        new_page.close()
        for team, events in calendars.items():
            if not events:
                continue
            # sanitiza o nome do ficheiro para evitar caracteres inválidos
            def safe_filename(s):
                s = unicodedata.normalize('NFKD', s)
                s = s.encode('ASCII', 'ignore').decode()
                s = re.sub(r"[^\w\s-]", "", s).strip()
                s = re.sub(r"[-\s]+", "_", s)
                return s

            filename = safe_filename(team)
            filepath = os.path.join('teamAgenda', f"{filename}.csv")
            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=events[0].keys())
                writer.writeheader()
                writer.writerows(events)
        break
    browser.close()

with sync_playwright() as playwright:
    run(playwright)