import psycopg2
import pandas as pd

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    dbname="SafeLab",
    user="postgres",
    password="Luis*001126",
    host="localhost",
    port="5432"
)

# Crear un cursor
cursor = conn.cursor()

# Leer el archivo CSV
csv_file = 'excel/Scheikunde_Lab_Inventaris (Novenber_2023).csv'
df = pd.read_csv(csv_file)

# Iterar sobre las filas del DataFrame y actualizar la base de datos
for index, row in df.iterrows():
    # Supongamos que tienes una tabla llamada 'mi_tabla' con columnas 'id', 'columna1', 'columna2'
    query = """
    UPDATE CPanel_aparatu
    SET name = %s, mark = %s, range = %s, cant= %s, Observation = %s, date = %s
    WHERE id = %s;
    """
    cursor.execute(query, (row['name'], row['mark'], row['range'], row['cant'], row['Observation'], row['date'], row['id']))

# Confirmar los cambios
conn.commit()

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

print("Base de datos actualizada exitosamente.")