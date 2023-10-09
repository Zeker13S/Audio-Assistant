from ctypes import cast, POINTER
import webbrowser
import psutil
import pygetwindow as gw
import logging

import math

def traits(response):
    if 'intents' in response:
        for x in response['intents']:
            if x['confidence'] > 0.7:
                if x['name'] == 'open_browser':
                    return abrir_navegador()
                elif x['name'] == 'close_browser':
                    return cerrar_navegador()

def abrir_navegador():
	url = 'https://google.com'
	webbrowser.register('chrome',
		None,
		webbrowser.\
		BackgroundBrowser("C:\Program Files\Google\Chrome\Application//chrome.exe"))
	webbrowser.get('chrome').open(url)
	return "Abrir navegador"

def cerrar_navegador():
    try:
        # Cerrar todas las ventanas de Chrome
        for window in gw.getWindowsWithTitle('Google Chrome'):
            window.close()
        
        # Esperar un momento para que se cierren completamente
        import time
        time.sleep(2)
        
        # Terminar todos los procesos de Chrome
        nombre_proceso = "chrome.exe"
        for proceso in psutil.process_iter(attrs=['pid', 'name']):
            try:
                if nombre_proceso.lower() in proceso.info['name'].lower():
                    proceso.terminate()
            except psutil.NoSuchProcess:
                pass
        
        return "Navegador cerrado"
    except Exception as e:
        return str(e)
