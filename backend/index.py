from flask import Flask
from flask import jsonify
from flask import request
from crossdomain import *
import astar

app = Flask(__name__) # tworzenie instancji aplikacji

@app.route('/a-star', methods=['POST', 'OPTIONS', 'GET']) # zdefiniowanie trasy dla aplikacji 
														  # '/a-star' określa końcową część adresu url, w którym ma się uruchamiać aplikacja (http://127.0.0.1:5000/a-star)
														  # methods określa obsługę żądań
														  # POST - obsługa danych przesyłanych przez użytkownika 
														  # GET - obsługa danych wysyłanych przez przeglądarkę
														  # OPTIONS - obsługa danych na temat żądań jakie obsługuje serwer
@crossdomain(origin='*')
def astarRoute():
	if (request.method == 'POST'): # sprawdzenie na bieżąco czy występuje żądanie POST
		print(request.form) # wyświetlenie danych w formie słownika (ImmutableMultiDict) jakie zostały przesłane przez przeglądarkę
		return jsonify(astar.receive(request.form)) # zwraca właśnie wysłane dane z żądania POST z powrotem do pliku js, które najpierw są modyfikowane w pliku astar zaczynając od funkcji receive
	else: # jeśli żądanie to nie POST, to wyświetlane jest "ok", które również daje znak, że program się uruchamia
		return 'ok' 