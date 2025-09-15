#!/usr/bin/env python3
"""
Aplicación Web para Figma Analytics
===================================

Interfaz visual para configurar parámetros del endpoint de Figma Analytics
y descargar archivos CSV directamente desde el navegador.
"""

from flask import Flask, render_template, request, jsonify, send_file, flash
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import json
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'figma_analytics_2025'

class FigmaAnalyticsAPI:
    """Clase para interactuar con la API de Figma Analytics"""
    
    def __init__(self, token: str):
        self.token = token
        # CORREGIDO: URL base correcta de la API de Figma
        self.base_url = "https://api.figma.com/v1/analytics/libraries"
        self.headers = {
            'X-FIGMA-TOKEN': token,
            'Content-Type': 'application/json'
        }
    
    def get_library_analytics(self, library_key: str, start_date: str = None, end_date: str = None, group_by: str = 'component'):
        """
        Obtiene datos de analytics de una biblioteca
        
        Args:
            library_key (str): Clave de la biblioteca (library_file_key)
            start_date (str): Fecha de inicio (YYYY-MM-DD)
            end_date (str): Fecha de fin (YYYY-MM-DD)
            group_by (str): Agrupación ('component' o 'team')
        
        Returns:
            dict: Respuesta de la API
        """
        # CORREGIDO: Endpoint correcto según la documentación oficial
        url = f"{self.base_url}/{library_key}/component/actions"
        
        params = {
            'group_by': group_by
        }
        
        if start_date:
            params['start_date'] = start_date
        
        if end_date:
            params['end_date'] = end_date
        
        try:
            print(f"🔍 Llamando a la API CORRECTA: {url}")
            print(f"📋 Parámetros: {params}")
            print(f"🔑 Token: {self.token[:10]}...")
            
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            print(f"📡 Status Code: {response.status_code}")
            print(f"📄 Headers: {dict(response.headers)}")
            
            if response.status_code == 404:
                # Error específico para 404
                error_msg = f"Biblioteca no encontrada. Verifica que el Library Key '{library_key}' sea correcto y que tengas acceso a esta biblioteca."
                raise Exception(error_msg)
            elif response.status_code == 401:
                error_msg = "Token de Figma inválido o expirado. Verifica tu token en la configuración de Figma."
                raise Exception(error_msg)
            elif response.status_code == 403:
                error_msg = "No tienes permisos para acceder a esta biblioteca. Verifica que tu token tenga acceso."
                raise Exception(error_msg)
            elif response.status_code >= 400:
                error_msg = f"Error de la API: {response.status_code} - {response.text}"
                raise Exception(error_msg)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise Exception("Timeout: La API de Figma tardó demasiado en responder. Intenta de nuevo.")
        except requests.exceptions.ConnectionError:
            raise Exception("Error de conexión: No se pudo conectar a la API de Figma. Verifica tu conexión a internet.")
        except requests.exceptions.RequestException as e:
            if "404" in str(e):
                raise Exception(f"Biblioteca no encontrada. Verifica que el Library Key '{library_key}' sea correcto.")
            else:
                raise Exception(f"Error en la API: {str(e)}")
    
    def get_all_pages(self, library_key: str, start_date: str = None, end_date: str = None, group_by: str = 'component'):
        """
        Obtiene todas las páginas de datos usando paginación
        
        Args:
            library_key (str): Clave de la biblioteca
            start_date (str): Fecha de inicio
            end_date (str): Fecha de fin
            group_by (str): Agrupación
        
        Returns:
            list: Lista de todos los registros
        """
        all_data = []
        cursor = None
        page_count = 0
        
        while True:
            page_count += 1
            # CORREGIDO: Endpoint correcto
            url = f"{self.base_url}/{library_key}/component/actions"
            params = {
                'group_by': group_by
            }
            
            if start_date:
                params['start_date'] = start_date
            
            if end_date:
                params['end_date'] = end_date
            
            if cursor:
                params['cursor'] = cursor
            
            try:
                print(f"📄 Página {page_count}: Obteniendo datos...")
                response = requests.get(url, headers=self.headers, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                # CORREGIDO: La API devuelve 'rows' no 'data'
                if 'rows' in data:
                    all_data.extend(data['rows'])
                    print(f"✅ Página {page_count}: {len(data['rows'])} registros obtenidos")
                else:
                    print(f"⚠️ Página {page_count}: No hay datos en la respuesta")
                    print(f"📄 Estructura de respuesta: {list(data.keys())}")
                
                # Verificar si hay más páginas usando cursor
                if 'cursor' in data and data['cursor']:
                    cursor = data['cursor']
                    print(f"🔄 Siguiente página: {cursor}")
                else:
                    print(f"🏁 No hay más páginas. Total: {len(all_data)} registros")
                    break
                    
            except requests.exceptions.RequestException as e:
                raise Exception(f"Error en la página {page_count}: {str(e)}")
        
        return all_data

def process_api_data(data):
    """
    Procesa los datos de la API y los convierte a formato CSV
    
    Args:
        data (list): Lista de registros de la API (rows)
    
    Returns:
        pandas.DataFrame: DataFrame procesado
    """
    if not data:
        return pd.DataFrame()
    
    print(f"🔄 Procesando {len(data)} registros de la API...")
    
    # Convertir a DataFrame
    df = pd.DataFrame(data)
    
    # Mostrar estructura de datos
    print(f"📊 Columnas encontradas: {list(df.columns)}")
    print(f"📈 Primeros registros: {df.head(2).to_dict('records')}")
    
    # CORREGIDO: La API devuelve datos directos en 'rows', no anidados
    # Los datos ya vienen en el formato correcto para CSV
    print("📝 Usando datos directos de la API (formato 'rows')...")
    
    # Renombrar columnas si es necesario para mantener compatibilidad
    column_mapping = {
        'component_name': 'component_name_variante',
        'component_set_name': 'component_set_name_component'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Asegurar que todas las columnas necesarias estén presentes
    required_columns = ['week', 'component_key', 'component_name_variante', 'component_set_key', 'component_set_name_component', 'insertions', 'detachments']
    
    for col in required_columns:
        if col not in df.columns:
            if col == 'component_name_variante':
                df[col] = df.get('component_name', '')
            elif col == 'component_set_name_component':
                df[col] = df.get('component_set_name', '')
            else:
                df[col] = ''
    
    print(f"✅ Datos procesados: {len(df)} registros finales")
    return df

@app.route('/')
def index():
    """Página principal con el formulario"""
    return render_template('index.html')

@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    """Prueba la conexión con la API de Figma"""
    try:
        data = request.get_json()
        token = data.get('token')
        library_key = data.get('library_key')
        
        if not token or not library_key:
            return jsonify({'success': False, 'error': 'Token y Library Key son requeridos'})
        
        print(f"🧪 Probando conexión para Library Key: {library_key}")
        
        # Probar conexión con una llamada simple
        api = FigmaAnalyticsAPI(token)
        result = api.get_library_analytics(library_key, group_by='component')
        
        # CORREGIDO: Verificar 'rows' en lugar de 'data'
        if 'rows' in result:
            return jsonify({
                'success': True, 
                'message': f'Conexión exitosa! Encontrados {len(result["rows"])} registros.',
                'sample_data': result.get('rows', [])[:3]  # Primeros 3 registros como muestra
            })
        else:
            return jsonify({'success': False, 'error': 'Respuesta inesperada de la API'})
            
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error en prueba de conexión: {error_msg}")
        return jsonify({'success': False, 'error': error_msg})

@app.route('/api/generate-csv', methods=['POST'])
def generate_csv():
    """Genera y devuelve el archivo CSV"""
    try:
        data = request.get_json()
        
        # Validar parámetros requeridos
        required_fields = ['token', 'library_key']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'Campo requerido: {field}'})
        
        token = data['token']
        library_key = data['library_key']
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        group_by = data.get('group_by', 'component')
        
        print(f"🚀 Generando CSV para biblioteca: {library_key}")
        print(f"📅 Fechas: {start_date} a {end_date}")
        print(f"🏷️ Agrupación: {group_by}")
        
        # Crear instancia de la API
        api = FigmaAnalyticsAPI(token)
        
        # Obtener datos
        all_data = api.get_all_pages(library_key, start_date, end_date, group_by)
        
        if not all_data:
            return jsonify({'success': False, 'error': 'No se encontraron datos para los parámetros especificados'})
        
        print(f"📊 Datos obtenidos: {len(all_data)} registros")
        
        # Procesar datos
        df = process_api_data(all_data)
        
        if df.empty:
            return jsonify({'success': False, 'error': 'Error al procesar los datos de la API'})
        
        # Crear archivo temporal
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"figma_analytics_{library_key}_{timestamp}.csv"
        
        # Guardar CSV
        csv_path = os.path.join(tempfile.gettempdir(), filename)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        print(f"💾 CSV guardado: {csv_path}")
        
        # Preparar respuesta
        response_data = {
            'success': True,
            'message': f'CSV generado exitosamente con {len(df)} registros',
            'filename': filename,
            'download_url': f'/download/{filename}',
            'summary': {
                'total_records': len(df),
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'components': df['component_key'].nunique() if 'component_key' in df.columns else 0,
                'total_insertions': int(df['insertions'].sum()) if 'insertions' in df.columns else 0,
                'total_detachments': int(df['detachments'].sum()) if 'detachments' in df.columns else 0
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error generando CSV: {error_msg}")
        return jsonify({'success': False, 'error': error_msg})

@app.route('/download/<filename>')
def download_file(filename):
    """Descarga el archivo CSV generado"""
    try:
        file_path = os.path.join(tempfile.gettempdir(), filename)
        
        if os.path.exists(file_path):
            return send_file(
                file_path,
                as_attachment=True,
                download_name=filename,
                mimetype='text/csv'
            )
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate-dates', methods=['POST'])
def validate_dates():
    """Valida las fechas ingresadas"""
    try:
        data = request.get_json()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'valid': False, 'error': 'Ambas fechas son requeridas'})
        
        # Convertir a datetime
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'valid': False, 'error': 'Formato de fecha inválido. Use YYYY-MM-DD'})
        
        # Validar rango
        if start_dt > end_dt:
            return jsonify({'valid': False, 'error': 'La fecha de inicio debe ser anterior a la fecha de fin'})
        
        # Validar que no sea muy antigua
        if start_dt < datetime(2020, 1, 1):
            return jsonify({'valid': False, 'error': 'La fecha de inicio no puede ser anterior a 2020-01-01'})
        
        # Validar que no sea futura
        if end_dt > datetime.now():
            return jsonify({'valid': False, 'error': 'La fecha de fin no puede ser futura'})
        
        # Calcular diferencia
        date_diff = (end_dt - start_dt).days
        
        if date_diff > 1095:  # 3 años
            return jsonify({
                'valid': True, 
                'warning': f'Rango de fechas muy amplio ({date_diff} días). Esto puede tomar mucho tiempo.'
            })
        
        return jsonify({'valid': True, 'message': 'Fechas válidas'})
        
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)})

@app.route('/api/debug-info', methods=['POST'])
def debug_info():
    """Endpoint para obtener información de debug"""
    try:
        data = request.get_json()
        token = data.get('token', '')[:10] + '...' if data.get('token') else 'No proporcionado'
        library_key = data.get('library_key', 'No proporcionado')
        
        debug_info = {
            'token_length': len(data.get('token', '')),
            'token_preview': token,
            'library_key': library_key,
            # CORREGIDO: URL correcta de la API
            'api_url': f"https://api.figma.com/v1/analytics/libraries/{library_key}/component/actions",
            'current_time': datetime.now().isoformat(),
            'python_version': f"{pd.__version__}",
            'requests_version': requests.__version__
        }
        
        return jsonify({'success': True, 'debug_info': debug_info})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🚀 Iniciando aplicación web de Figma Analytics...")
    print("📱 Abre tu navegador en: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
