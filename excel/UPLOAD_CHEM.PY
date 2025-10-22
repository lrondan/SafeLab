import csv
import psycopg2
from psycopg2 import Error, sql

def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Crear conexión a PostgreSQL"""
    conn = None
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("✅ Conexión a PostgreSQL exitosa")
        return conn
    except Error as e:
        print(f"❌ Error al conectar a PostgreSQL: {e}")
        return None

def get_table_columns(conn, table_name):
    """Obtener los nombres de las columnas de la tabla"""
    try:
        cursor = conn.cursor()
        cursor.execute(
            sql.SQL("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = {}
                ORDER BY ordinal_position
            """).format(sql.Literal(table_name))
        )
        columns = cursor.fetchall()
        print("\n🔍 Columnas en la tabla PostgreSQL:")
        for col in columns:
            print(f"- {col[0]} ({col[1]})")
        return [col[0] for col in columns]
    except Error as e:
        print(f"❌ Error al obtener columnas de la tabla: {e}")
        return None

def show_csv_columns(csv_file, delimiter=','):
    """Mostrar las columnas del archivo CSV"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=delimiter)
            print("\n📋 Columnas en el archivo CSV:")
            for col in csv_reader.fieldnames:
                print(f"- {col}")
            return csv_reader.fieldnames
    except Exception as e:
        print(f"❌ Error al leer el CSV: {e}")
        return None

def insert_data_from_csv(conn, csv_file, table_name, delimiter=';'):
    """Insertar datos desde un archivo CSV a la tabla especificada"""
    try:
        cursor = conn.cursor()
        
        # Obtener columnas de ambas fuentes
        table_columns = get_table_columns(conn, table_name)
        csv_columns = show_csv_columns(csv_file, delimiter)
        
        if not table_columns or not csv_columns:
            raise ValueError("No se pudieron obtener las columnas necesarias")
        
        # Encontrar columnas comunes
        common_columns = sorted(list(set(table_columns) & set(csv_columns)))
        
        if not common_columns:
            print("\n🔴 No hay coincidencia entre las columnas del CSV y la tabla")
            print("💡 Posibles soluciones:")
            print("1. Renombra las columnas del CSV para que coincidan")
            print("2. Crea una tabla temporal o nueva con la estructura del CSV")
            print("3. Usa una herramienta ETL para mapear columnas diferentes")
            return False
        
        print("\n🟢 Columnas comunes encontradas:")
        for col in common_columns:
            print(f"- {col}")
        
        # Leer y procesar el CSV
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=delimiter)
            
            # Crear la sentencia SQL de inserción
            insert_query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(table_name),
                sql.SQL(', ').join(map(sql.Identifier, common_columns)),
                sql.SQL(', ').join(sql.Placeholder() * len(common_columns))
            )
            
            # Contador para mostrar progreso
            total_rows = 0
            batch_size = 100
            
            for row in csv_reader:
                # Preparar los valores en el orden correcto
                values = [row[col] if row[col] != '' else None for col in common_columns]
                cursor.execute(insert_query, values)
                total_rows += 1
                
                # Mostrar progreso cada batch_size
                if total_rows % batch_size == 0:
                    print(f"📦 Procesadas {total_rows} filas...")
            
        conn.commit()
        print(f"\n✅ Datos insertados exitosamente: {total_rows} filas desde {csv_file}")
        return True
        
    except Error as e:
        conn.rollback()
        print(f"\n❌ Error de PostgreSQL: {e}")
        return False
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error inesperado: {type(e).__name__} - {str(e)}")
        return False

def main():
    # Configuración de PostgreSQL - MODIFICA ESTOS VALORES
    db_config = {
        'db_name': 'SafeLab',
        'db_user': 'postgres',
        'db_password': 'Luis*001126',
        'db_host': 'localhost',
        'db_port': '5432'
    }
    
    # Archivo CSV y tabla - MODIFICA ESTOS VALORES
    csv_file = 'C:/Users/user/Desktop/SafeLab/excel/CHEMICALS.csv'  # Ruta a tu archivo CSV
    table_name = 'CPanel_chemsub'  # Nombre de tu tabla existente
    
    print("\n" + "="*50)
    print("  SISTEMA DE CARGA DE DATOS CSV A POSTGRESQL")
    print("="*50 + "\n")
    
    # Crear conexión
    conn = create_connection(**db_config)
    
    if conn is not None:
        try:
            # Insertar datos
            success = insert_data_from_csv(conn, csv_file, table_name)
            
            if not success:
                print("\n✋ Ejecución terminada con problemas")
                print("💡 Revisa los mensajes anteriores para solucionarlos")
        finally:
            conn.close()
            print("\n🔌 Conexión a PostgreSQL cerrada")

if __name__ == '__main__':
    main()