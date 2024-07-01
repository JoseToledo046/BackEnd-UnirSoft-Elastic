import csv
import mysql.connector
import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)

def read_pelicula(cursor):
    query = f"SELECT IdFilm, Title, BackdropPath, PosterPath, Budget, OriginalLanguage, OriginalTitle, ReleaseDate, Revenue, RunTime, TagLine, VoteAvarage, OverView, Genero, Video  FROM peliculas"
    cursor.execute(query)
    results = cursor.fetchall()
    return results
    
def main():
    cPelicula = ""
    
    conn = mysql.connector.connect(
            host='monorail.proxy.rlwy.net',  
            port=27601,
            database='buscador', 
            user='root',  
            password='KJCgKEczAzTmbVriQjoqukpDnGLWTtgg'   
        )
    
    if conn.is_connected():
        
        print('Conexion establecida...')
        cursor = conn.cursor()
        print('Cursor OK')

        ## Generar peliculas
        pelicula = read_pelicula(cursor)
        
        if pelicula:
                
            for iPelicula in pelicula:
                    
                pelicula_data = {
                    "IdFilm": iPelicula[0],
                    "Title": iPelicula[1],
                    "BackdropPath": iPelicula[2],
                    "PosterPath": iPelicula[3],
                    "Budget": iPelicula[4],
                    "OriginalLanguage": iPelicula[5],
                    "OriginalTitle": iPelicula[6],
                    "ReleaseDate": iPelicula[7],
                    "Revenue": iPelicula[8],
                    "RunTime": iPelicula[9],
                    "TagLine": iPelicula[10],
                    "VoteAvarage": iPelicula[11],
                    "OverView": iPelicula[12],
                    "Genero": iPelicula[13],
                    "Video": iPelicula[14]
                    }
                
                for key, value in pelicula_data.items():
                    if isinstance(value, str):
                        pelicula_data[key] = value.replace('\r', '')

                movie_json = json.dumps(pelicula_data, cls=DecimalEncoder, ensure_ascii=False)
                cPelicula = cPelicula + """{"index":{"_index":"peliculas"}}""" + "\n" + movie_json + "\n" 
                
            with open('JSON/dato_pelicula.json', 'w', encoding='utf-8') as file:
                file.write(cPelicula)
                
            print("Fin pelicula")
    
main()