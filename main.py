import discord
from discord.ext import commands
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import asyncio
import os
import webserver
from dotenv import load_dotenv, dotenv_values
import json

# Carga el archivo .env
load_dotenv()

# Reemplaza "YOUR TOKEN HERE" con tu token real.
TOKEN = os.getenv("DISCORD")

# IDs del servidor y canal específicos
GUILD_ID = 891766531699118131
CHANNEL_ID = 891766531699118134
MESSAGE_CHANNEL_ID = 1280769149982740533

# URLs según el autor del mensaje
urls = {
    "matimcs": "https://csstats.gg/player/76561198257828663#/matches",
    "oscar7839": "https://csstats.gg/player/76561198096731508#/matches",
    "nicomichea": "https://csstats.gg/player/76561198046820470#/matches",
    "crisz1010": "https://csstats.gg/player/76561199011433275#/matches",
    "cristobalmoya": "https://csstats.gg/player/76561198119174556#/matches",
    "lul_luqui": "https://csstats.gg/player/76561198869951186#/matches"
}

# IDs de Discord para las menciones
discord_ids = {
    "matimcs": 376174160457760768,
    "oscar7839": 321076949260959746,
    "nicomichea": 301892603736096769,
    "crisz1010": 656972976117252102,
    "cristobalmoya": 598332763040383007,
    "lul_luqui": 654129835786108936
}

# Configura los intents
intents = discord.Intents.default()
intents.message_content = True

# Inicializa el bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Carga las credenciales de Google Sheets desde la variable de entorno
creds_json = os.getenv("GOOGLE_SHEETS")
print(creds_json)
creds_dict = json.loads(creds_json)

# Configura las credenciales de Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Abre el archivo de Google Sheets
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/17X_ksb3J1wL6vVLQhjGJRb8zjuohcvC-1I3fnrO2YLM/edit')

# ID de la hoja
sheet = spreadsheet.get_worksheet_by_id(0)

def check_and_update_sheet(url):
    # Obtiene todas las celdas en la columna A
    cell_values = sheet.col_values(1)
    
    # Verifica si el enlace ya está en la columna A
    if url not in cell_values:
        # Encuentra la primera celda vacía en la columna A
        next_empty_row = len(cell_values) + 1
        sheet.update_cell(next_empty_row, 1, url)
        #print(f"Enlace agregado en la fila {next_empty_row}.")
        return next_empty_row
    else:
        #print("El enlace ya está en la columna A.")
        return None

def update_sheet_values(row_to_update, values, kda, hs, kast, rating, ef):
    # Actualiza las celdas correspondientes en la fila especificada
    col_map = {
        "cristobalmoya": 2,
        "nicomichea": 8,
        "oscar7839": 14,
        "matimcs": 20,
        "lul_luqui": 26,
        "crisz1010": 32
    }
    kda_map = {
        "cristobalmoya": 3,
        "nicomichea": 9,
        "oscar7839": 15,
        "matimcs": 21,
        "lul_luqui": 27,
        "crisz1010": 33
    }
    hs_map = {
        "cristobalmoya": 4,
        "nicomichea": 10,
        "oscar7839": 16,
        "matimcs": 22,
        "lul_luqui": 28,
        "crisz1010": 34
    }
    kast_map = {
        "cristobalmoya": 5,
        "nicomichea": 11,
        "oscar7839": 17,
        "matimcs": 23,
        "lul_luqui": 29,
        "crisz1010": 35
    }
    rating_map = {
        "cristobalmoya": 6,
        "nicomichea": 12,
        "oscar7839": 18,
        "matimcs": 24,
        "lul_luqui": 30,
        "crisz1010": 36
    }
    ef_map = {
        "cristobalmoya": 7,
        "nicomichea": 13,
        "oscar7839": 19,
        "matimcs": 25,
        "lul_luqui": 31,
        "crisz1010": 37
    }
    messages = []

    for player, value in values.items():
        if value:
            col = col_map[player]
            sheet.update_cell(row_to_update, col, value)
            #print(f"Actualizado {player} en la columna {col} con el valor {value}")

            # Lógica para evaluar el valor y preparar el mensaje correspondiente
            value_float = float(value)
            if 30 <= value_float <= 55:
                messages.append(f"<@{discord_ids[player]}> agrega $1.000 al pozo")
                deudas = spreadsheet.get_worksheet_by_id('881293869')
                if player == "cristobalmoya":
                    actual = int(deudas.acell('B1').value)
                    deudas.update('B1',actual-1000)
                elif player == "nicomichea":
                    actual = int(deudas.acell('B2').value)
                    deudas.update('B2',actual-1000)
                elif player == "oscar7839":
                    actual = int(deudas.acell('B3').value)
                    deudas.update('B3',actual-1000)
                elif player == "matimcs":
                    actual = int(deudas.acell('B4').value)
                    deudas.update('B4',actual-1000)
                elif player == "lul_luqui":
                    actual = int(deudas.acell('B5').value)
                    deudas.update('B5',actual-1000)
                elif player == "crisz1010":
                    actual = int(deudas.acell('B6').value)
                    deudas.update('B6',actual-1000)
            elif value_float < 30:
                messages.append(f"<@{discord_ids[player]}> agrega $3.000 al pozo")
                deudas = spreadsheet.get_worksheet_by_id('881293869')
                if player == "cristobalmoya":
                    actual = int(deudas.acell('B1').value)
                    deudas.update('B1',actual-3000)
                elif player == "nicomichea":
                    actual = int(deudas.acell('B2').value)
                    deudas.update('B2',actual-3000)
                elif player == "oscar7839":
                    actual = int(deudas.acell('B3').value)
                    deudas.update('B3',actual-3000)
                elif player == "matimcs":
                    actual = int(deudas.acell('B4').value)
                    deudas.update('B4',actual-3000)
                elif player == "lul_luqui":
                    actual = int(deudas.acell('B5').value)
                    deudas.update('B5',actual-3000)
                elif player == "crisz1010":
                    actual = int(deudas.acell('B6').value)
                    deudas.update('B6',actual-3000)
            elif value_float >= 120:
                if player == "cristobalmoya":
                    actual = int(deudas.acell('B1').value)
                    if actual != 0:
                        deudas.update('B1',actual+1000)
                elif player == "nicomichea":
                    actual = int(deudas.acell('B2').value)
                    if actual != 0:
                        deudas.update('B2',actual+1000)
                elif player == "oscar7839":
                    actual = int(deudas.acell('B3').value)
                    if actual != 0:
                        deudas.update('B3',actual+1000)
                elif player == "matimcs":
                    actual = int(deudas.acell('B4').value)
                    if actual != 0:
                        deudas.update('B4',actual+1000)
                elif player == "lul_luqui":
                    actual = int(deudas.acell('B5').value)
                    if actual != 0:
                        deudas.update('B5',actual+1000)
                elif player == "crisz1010":
                    actual = int(deudas.acell('B6').value)
                    if actual != 0:
                        deudas.update('B6',actual+1000)
                messages.append(f"<@{discord_ids[player]}> descuenta $1.000 del pozo")
                deudas = spreadsheet.get_worksheet_by_id('881293869')

    for player, i in kda.items():
        if i:
            col = kda_map[player]
            sheet.update_cell(row_to_update, col, i)
    for player, i in hs.items():
        if i:
            col = hs_map[player]
            sheet.update_cell(row_to_update, col, i)
    for player, i in kast.items():
        if i:
            col = kast_map[player]
            sheet.update_cell(row_to_update, col, i)
    for player, i in rating.items():
        if i:
            col = rating_map[player]
            sheet.update_cell(row_to_update, col, i)
    for player, i in ef.items():
        if i:
            col = ef_map[player]
            sheet.update_cell(row_to_update, col, i)
    return messages

@bot.command(name='agregar', aliases=['a'])
async def agregar(ctx):
    if ctx.guild and ctx.guild.id == GUILD_ID:
        if ctx.channel.id == CHANNEL_ID:
            author = ctx.author.name.lower()
            if author in urls:
                processing_message = await ctx.send(":timer: ***Procesando partida...***")
                url = urls[author]

                # Configura el perfil de Firefox
                firefox_profile_path = r'C:\Users\Matias\AppData\Roaming\Mozilla\Firefox\Profiles\zoikq2v8.default-release'
                firefox_profile = webdriver.FirefoxProfile()
                firefox_options = webdriver.FirefoxOptions()
                firefox_options.add_argument(f'--profile={firefox_profile_path}')
                firefox_options.set_preference("media.navigator.permission.disabled", False)
                firefox_options.add_argument("--headless")  # Agrega esta línea para ejecutar en modo headless

                # Crear perfil de Firefox en el directorio temporal
                firefox_options.profile = "/tmp/firefox_profile"

                # Crear una instancia del navegador (en este ejemplo, usaremos Firefox)
                driver = webdriver.Firefox(options=firefox_options)
                driver.get(url)

                try:
                    # Espera a que la tabla esté presente en el DOM y selecciona la primera fila
                    table = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="match-list-outer"]/table'))
                    )

                    first_row_link = table.find_element(By.XPATH, './/tr[1]/td/a')
                    
                    # Obtén el enlace de la primera fila en la tabla
                    link_url = first_row_link.get_attribute("href")
                    #print(f"Enlace de la primera fila: {link_url}")

                    # Verifica y actualiza Google Sheets
                    row_to_update = check_and_update_sheet(link_url)
                    
                    if row_to_update:
                        # Abre el enlace en la misma pestaña del navegador existente
                        driver.get(link_url)

                        # Espera a que la tabla esté presente en el DOM y selecciona la tabla de puntajes
                        scoreboard = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="match-scoreboard"]'))
                        )
                        
                        # Inicializa los valores a agregar
                        values = {
                            "lul_luqui": None,
                            "oscar7839": None,
                            "nicomichea": None,
                            "crisz1010": None,
                            "cristobalmoya": None,
                            "matimcs": None
                        }
                        
                        # KDA
                        kda = {
                            "lul_luqui": None,
                            "oscar7839": None,
                            "nicomichea": None,
                            "crisz1010": None,
                            "cristobalmoya": None,
                            "matimcs": None
                        }
                    
                        # HS
                        hs = {
                            "lul_luqui": None,
                            "oscar7839": None,
                            "nicomichea": None,
                            "crisz1010": None,
                            "cristobalmoya": None,
                            "matimcs": None
                        }
                        # Kast
                        kast = {
                            "lul_luqui": None,
                            "oscar7839": None,
                            "nicomichea": None,
                            "crisz1010": None,
                            "cristobalmoya": None,
                            "matimcs": None
                        }
                        # rating
                        rating = {
                            "lul_luqui": None,
                            "oscar7839": None,
                            "nicomichea": None,
                            "crisz1010": None,
                            "cristobalmoya": None,
                            "matimcs": None
                        }
                        # EF
                        ef = {
                            "lul_luqui": None,
                            "oscar7839": None,
                            "nicomichea": None,
                            "crisz1010": None,
                            "cristobalmoya": None,
                            "matimcs": None
                        }
                        # Inicializa los nombres y los valores de resultados
                        names = {}
                        resultados = {}

                        # Itera sobre los índices especificados
                        for x in [1, 3]:
                            for z in range(2, 7):
                                xpath = f"//*[@id='match-scoreboard']/tbody[{x}]/tr[{z}]/td[2]/a"
                                try:
                                    element = WebDriverWait(driver, 5).until(
                                        EC.presence_of_element_located((By.XPATH, xpath))
                                    )
                                    link = element.get_attribute("href")
                                    #print(f"Valor en XPath '{xpath}': {link}")

                                    # Compara el enlace y guarda el valor de la columna 11 y el nombre correspondiente
                                    if link == "https://csstats.gg/player/76561198257828663":
                                        column_11_value = element.find_element(By.XPATH, "./../../td[11]").text
                                        column_10_value = element.find_element(By.XPATH, "./../../td[10]").text
                                        column_12_value = element.find_element(By.XPATH, "./../../td[12]").text
                                        column_13_value = element.find_element(By.XPATH, "./../../td[13]").text
                                        column_14_value = element.find_element(By.XPATH, "./../../td[14]").text
                                        column_15_value = element.find_element(By.XPATH, "./../../td[15]").text
                                        values["matimcs"] = column_11_value
                                        kda["matimcs"] = column_10_value
                                        hs["matimcs"] = column_12_value
                                        kast["matimcs"] = column_13_value
                                        rating["matimcs"] = column_14_value
                                        ef["matimcs"] = column_15_value
                                        
                                except Exception as e:
                                    print(f"No se pudo encontrar el elemento en XPath '{xpath}': {e}")

                        # Captura y print valores adicionales como mapa, resultado1 y resultado2
                        try:
                            mapa = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, '//*[@id="match-info-inner"]/div/div[3]'))
                            ).text
                            #print(f"Mapa: {mapa}")
                        except Exception as e:
                            print(f"No se pudo obtener el mapa: {e}")
                            mapa = "No se pudo obtener el mapa"

                        try:
                            resultado1 = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/span'))
                            ).text
                            #print(f"Resultado 1: {resultado1}")
                        except Exception as e:
                            print(f"No se pudo obtener el resultado 1: {e}")
                            resultado1 = "No se pudo obtener el resultado 1"

                        try:
                            resultado2 = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, '//*[@id="match-details"]/div[2]/div/span'))
                            ).text
                            print(f"Resultado 2: {resultado2}")
                        except Exception as e:
                            print(f"No se pudo obtener el resultado 2: {e}")
                            resultado2 = "No se pudo obtener el resultado 2"

                        # Actualiza Google Sheets con los valores capturados
                        print(hs)
                        messages = update_sheet_values(row_to_update, values, kda, hs, kast, rating, ef)

                        # Cierra Firefox si es necesario
                        driver.quit()

                        # Envía el mensaje formateado al canal de resultados
                        result_message = f"# Partida {row_to_update - 1}\n### {mapa}\n\n### **{resultado1} - {resultado2}**\n"
                        for player, value in values.items():
                            if value:
                                result_message += f"- <@{discord_ids[player]}>: {value}\n"

                        result_message += "\n" + "\n".join(messages)
                        await processing_message.delete()
                    
                        # Envía el mensaje de confirmación al usuario
                        confirmation_message = f"¡Hola <@{ctx.author.id}>, tu partida [{link_url}] ha sido registrada!"
                        await ctx.send(confirmation_message)

                        # Envía el mensaje formateado al canal de resultados
                        channel = bot.get_channel(MESSAGE_CHANNEL_ID)
                        await channel.send(result_message)

                    else:
                        await processing_message.delete()
                        message = await ctx.send(f"¡Hola <@{ctx.author.id}>, la última partida ya había sido agregada anteriormente, ¿Desea reintentar en 5 minutos más?.")
                        
                        # Añadir las reacciones :white_check_mark: y :x:
                        await message.add_reaction("✅")
                        await message.add_reaction("❌")
                        
                        def check(reaction, user):
                            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

                        try:
                            # Esperar hasta 10 segundos para una reacción
                            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=check)

                            if str(reaction.emoji) == "✅":
                                await ctx.send("Reintentando en 5 minutos...")
                                await asyncio.sleep(300)  # Espera 5 minutos
                                driver.quit()
                                await agregar(ctx)  # Reintentar la función
                            elif str(reaction.emoji) == "❌":
                                await ctx.send("Cancelado. Cerrando navegador.")
                                driver.quit()

                        except asyncio.TimeoutError:
                            await ctx.send("No se recibió una respuesta. Cerrando navegador.")
                            driver.quit()
                except Exception as e:
                    print(f"Ocurrió un error: {e}")
                    driver.quit()
            else:
                await ctx.send("No tienes una URL asociada.")
        else:
            await ctx.send("Este comando solo puede ser usado en el canal autorizado.")
    else:
        await ctx.send("Este comando solo puede ser usado en el servidor autorizado.")


# Ejecuta el bot
webserver.keep_alive()
bot.run(TOKEN)
