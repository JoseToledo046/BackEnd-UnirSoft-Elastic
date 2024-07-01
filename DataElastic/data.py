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
    query = f"SELECT id, title, backdrop_path, poster_path, budget, original_language, original_title,  release_date, revenue, runtime, tagline, vote_average, overview FROM t_pelicula"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def read_genero(cursor):
    query = f"SELECT id_film, name FROM t_genero"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def read_video(cursor):
    query = f"SELECT id_film, id_video, plataforma, name_video FROM t_video"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def read_produccion(cursor):
    query = f"SELECT id_film, id_prod, logo_path, name FROM t_produccion"
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def read_cast(cursor):
    query = f"SELECT id_film, name, profile_path, character_name FROM t_cast"
    cursor.execute(query)
    results = cursor.fetchall()
    return results
    
def main():
    cPelicula = ""
    cGenero = ""
    cVideo = ""
    cPoduccion = ""
    cCast = ""
    
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
                
        ## Generar produccion
        produccion = read_produccion(cursor)
        if produccion:
            
            for iproduccion in produccion:
                
                produccion_data = {
                    "id_film": iproduccion[0],
                    "logo_path": iproduccion[2],
                    "name": iproduccion[3]
                }
                
                for key, value in produccion_data.items():
                    if isinstance(value, str):
                        produccion_data[key] = value.replace('\r', '')
                
                produccion_json = json.dumps(produccion_data, cls=DecimalEncoder, ensure_ascii=False)
                cPoduccion = cPoduccion + """{"index":{"_index":"produccion"}}""" + "\n" + produccion_json + "\n"
                
            with open('JSON/produccion.json', 'w', encoding='utf-8') as file:
                file.write(cPoduccion)
                
            print("Fin produccion")
        
        ## Generar videos
        video = read_video(cursor)
        if video:
            
            for iVideo in video:
                
                video_data = {
                    "id_film": iVideo[0],
                    "id_video": iVideo[1],
                    "plataforma": iVideo[2],
                    "name_video": iVideo[3]
                }
                
                for key, value in video_data.items():
                    if isinstance(value, str):
                        video_data[key] = value.replace('\r', '')
                
                video_json = json.dumps(video_data, cls=DecimalEncoder, ensure_ascii=False)
                cVideo = cVideo + """{"index":{"_index":"video"}}""" + "\n" + video_json + "\n"
                
            with open('JSON/videos.json', 'w', encoding='utf-8') as file:
                file.write(cVideo)
                
            print("Fin video")
        
        ## Generar generos
        genero = read_genero(cursor)
        if genero:
            
            for iGenero in genero:
                
                genero_data = {
                    "id_film": iGenero[0],
                    "name": iGenero[1]
                }
                
                for key, value in genero_data.items():
                    if isinstance(value, str):
                        genero_data[key] = value.replace('\r', '')
                
                genero_json = json.dumps(genero_data, cls=DecimalEncoder, ensure_ascii=False)
                cGenero = cGenero + """{"index":{"_index":"generos"}}""" + "\n" + genero_json + "\n"
                
            with open('JSON/generos.json', 'w', encoding='utf-8') as file:
                file.write(cGenero)
                
            print("Fin genero")
        
        ## Generar peliculas
        pelicula = read_pelicula(cursor)
        
        if pelicula:
                
            for iPelicula in pelicula:
                    
                pelicula_data = {
                    "id": iPelicula[0],
                    "title": iPelicula[1],
                    "backdrop_path": iPelicula[2],
                    "poster_path": iPelicula[3],
                    "budget": iPelicula[4],
                    "original_language": iPelicula[5],
                    "original_title": iPelicula[6],
                    "release_date": iPelicula[7],
                    "revenue": iPelicula[8],
                    "runtime": iPelicula[9],
                    "tagline": iPelicula[10],
                    "vote_average": iPelicula[11],
                    "overview": iPelicula[12]
                    }
                
                for key, value in pelicula_data.items():
                    if isinstance(value, str):
                        pelicula_data[key] = value.replace('\r', '')

                movie_json = json.dumps(pelicula_data, cls=DecimalEncoder, ensure_ascii=False)
                cPelicula = cPelicula + """{"index":{"_index":"peliculas"}}""" + "\n" + movie_json + "\n" 
                
            with open('JSON/peliculas.json', 'w', encoding='utf-8') as file:
                file.write(cPelicula)
                
            print("Fin pelicula")

        ## Generar cast
        cast = read_cast(cursor)
        if cast:
            
            for icCast in cast:
                
                cast_data = {
                    "id_film": icCast[0],
                    "name": icCast[1],
                    "profile_path": icCast[2],
                    "character_name": icCast[3]
                }
                
                for key, value in cast_data.items():
                    if isinstance(value, str):
                        cast_data[key] = value.replace('\r', '')
                
                cast_json = json.dumps(cast_data, cls=DecimalEncoder, ensure_ascii=False)
                cCast = cCast + """{"index":{"_index":"cast"}}""" + "\n" + cast_json + "\n"
                
            with open('JSON/cast.json', 'w', encoding='utf-8') as file:
                file.write(cCast)
                
            print("Fin cast")
        
    
main()