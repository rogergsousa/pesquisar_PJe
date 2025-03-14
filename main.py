''' Automatiza a extração de dados do PJe e a geração de relatórios. '''
# pylint: disable=line-too-long
# pylint: disable=broad-exception-caught
# pylint: disable=too-many-locals

import logging
from pathlib import Path
import sys
import os
import re
import time
import base64
from playwright.sync_api import sync_playwright
import pandas as pd
from twocaptcha import TwoCaptcha

# https://2captcha.com/enterpage
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
api_key = os.getenv('APIKEY_2CAPTCHA', 'sua_chave_api_aqui')

def resolve_captcha():
    ''' Resolve o captcha do PJe utilizando o serviço 2Captcha '''
    solver = TwoCaptcha(api_key)
    try:
        result = solver.normal('captcha.png')
    except Exception as e:
        log_step(e)
        return None
    return result['code']

def log_step(message):
    ''' Exibe mensagens de log formatadas '''
    print(f"[INFO] {message}")
    logging.info(message)

def init():
    # Start chrome in power shell
    # Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList '--remote-debugging-port=9222', '--user-data-dir="C:\Users\<SEU_USUARIO>\AppData\Local\Google\Chrome\User Data"', '--profile-directory="Default"'

    """Função principal do projeto."""
    debugging_url = "http://localhost:9222"  # Connect to the running Chrome instance

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(debugging_url)  # Connect to existing Chrome
        context = browser.contexts[0]  # Use the existing browser context
        page = context.new_page()  # Open a new tab

        try:
            # process number from excel and updade complete field
            excel_process_file = Path('resource', 'pesquisar no PJe.xlsx')
            df = pd.read_excel(excel_process_file, sheet_name='result', dtype={'Valor': str, 'Último Andamento': str})
            vcaptcha = ""
            # Interate over the rows
            index = 0
            for index, row in df.iterrows():
                try:
                    if not pd.isna(row['Valor']):  # Skip if the value is already filled
                        continue

                    process_number = row['Processo']

                    # Navigate to the PJE TRT10 website
                    page.goto("https://pje.trt10.jus.br/consultaprocessual/", timeout=30000)

                    # Fill in the process number
                    process_input = page.locator("#nrProcessoInput")
                    process_input.type(process_number, delay=100)  # Simulates typing with a small delay

                    # Press tab to move focus to the next input
                    process_input.press("Tab")

                    # Click the search button
                    search_button = page.locator("#btnPesquisar")
                    search_button.click()
                    time.sleep(1) 
                    # Wait for the search results to load
                    #page.wait_for_load_state("load")

                    painel_locator = page.locator("#painel-escolha-processo")
                    #painel_locator.wait_for(timeout=5000)

                    # # Verify if #painel-escolha-processo div exists (1a and 2a estancia)
                    if painel_locator.count() > 0:
                        # Click the first button inside the div
                        first_button = painel_locator.locator("button.selecao-processo").first
                        first_button.click()

                    captcha_locator = page.locator("#captchaInput")
                    captcha_locator.wait_for(state="visible", timeout=5000)

                    # Validate if captchaInput is present
                    if captcha_locator.is_visible():
                        # Wait for the captcha image to be visible
                        img_locator = page.locator("#imagemCaptcha")
                        img_locator.wait_for(state="visible", timeout=5000)

                        # Extract the src attribute (Base64 data)
                        img_src = img_locator.get_attribute("src")

                        if img_src and img_src.startswith("data:image"):
                            # Remove "data:image/png;base64," prefix
                            base64_data = img_src.split(",")[1]

                            # Decode the Base64 image
                            img_bytes = base64.b64decode(base64_data)

                            # Save the image to a file
                            with open('captcha.png', "wb") as img_file:
                                img_file.write(img_bytes)
                        else:
                            continue

                        # Wait for captcha to be manually completed
                        vcaptcha = resolve_captcha()

                        # Fill in the CAPTCHA
                        captcha_input = page.locator("#captchaInput")
                        captcha_input.fill(vcaptcha)

                        # Click the CAPTCHA validate button again
                        captcha_button = page.locator("#btnEnviar")
                        captcha_button.click()

                    # Click on the details div
                    details_div = page.locator("#titulo-detalhes")
                    details_div.wait_for(state="visible", timeout=5000)
                    details_div.click()

                    # Extract monetary value from the case details
                    time.sleep(2)  # Give time for content to load
                    details_text = page.locator("#colunas-dados-processo").inner_text()

                    # Regex pattern to find monetary values (e.g., R$ 17.148,23)
                    monetary_pattern = r"R\$[\s ]*([\d\.,]+)"
                    match = re.search(monetary_pattern, details_text)
                    case_value = match.group(1) if match else "0,00"

                    # Retrieve first timeline entry
                    first_timeline_entry = page.locator("ul.pje-timeline li").nth(0).inner_text()

                    # Print extracted information
                    df.at[index, 'Valor'] = case_value
                    df.at[index, 'Último Andamento'] = first_timeline_entry
                    print(f"🔹 Case Number: {process_number} indice {index} captcha {vcaptcha}")

                    # read the control.txt file to check if the process is complete
                    control_file = Path('resource', 'control.txt')
                    with open(control_file, 'r', encoding='utf-8') as file:
                        control = file.read()
                        if control == '1':
                            log_step(f"🔹 Processo {process_number} finalizado")
                            break
                except Exception as e:
                    log_step(f"[ERRO] Erro inesperado: {e} indice {index} captcha {vcaptcha}")
                    continue

        except ValueError as e:
            log_step(f"[ERRO] {e} indice {index}")
        except Exception as e:
            log_step(f"[ERRO] Erro inesperado: {e} indice {index}")
        finally:
            # Save the updated dataframe to a new Excel file
            df.to_excel(excel_process_file, sheet_name='result', index=False)
            input("Pressione Enter para encerrar...")

if __name__ == "__main__":
    init()
