# 🌐 **Aplicación Web de Figma Analytics**

## 🎯 **Descripción**

Interfaz web moderna y user-friendly para generar reportes CSV desde la API de Figma Analytics. Esta aplicación te permite configurar parámetros visualmente y descargar archivos CSV directamente desde tu navegador.

## ✨ **Características Principales**

### **🎨 Interfaz Visual Moderna**
- **Diseño responsive** que funciona en todos los dispositivos
- **Formularios intuitivos** con validación en tiempo real
- **Gradientes y animaciones** para una experiencia premium
- **Iconos y elementos visuales** que facilitan la navegación

### **🔌 Funcionalidades de Conexión**
- **Prueba de conexión** antes de generar reportes
- **Validación automática** de tokens y library keys
- **Mensajes de error claros** para troubleshooting
- **Auto-completado** de formularios después de pruebas exitosas

### **📅 Gestión de Fechas Inteligente**
- **Selector de fechas nativo** del navegador
- **Validación automática** de rangos de fechas
- **Fechas por defecto** (últimos 3 meses)
- **Advertencias** para rangos muy amplios

### **📊 Generación de Reportes**
- **Procesamiento en tiempo real** de la API de Figma
- **Manejo automático de paginación** para datasets grandes
- **Métricas en tiempo real** durante la generación
- **Resumen visual** de los resultados

### **💾 Descarga Directa**
- **Archivos CSV optimizados** para Excel/Google Sheets
- **Nombres descriptivos** con timestamps
- **Descarga automática** después de la generación
- **Manejo de archivos temporales** seguro

## 🚀 **Instalación y Configuración**

### **Requisitos Previos**
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno

### **Paso 1: Clonar/Descargar el Proyecto**
```bash
# Si tienes git
git clone <tu-repositorio>
cd figma-analytics-web

# O descarga manual y extrae en una carpeta
```

### **Paso 2: Instalar Dependencias**
```bash
pip install flask pandas requests
```

### **Paso 3: Verificar Estructura de Archivos**
```
figma-analytics-web/
├── app.py                 # Aplicación principal Flask
├── config.py              # Configuración de la aplicación
├── run_web_app.py         # Script de inicio simplificado
├── templates/
│   └── index.html         # Plantilla HTML principal
├── README_WEB_APP.md      # Este archivo
└── requirements.txt        # Dependencias (opcional)
```

### **Paso 4: Ejecutar la Aplicación**

#### **Opción A: Script Simplificado (Recomendado)**
```bash
python run_web_app.py
```

#### **Opción B: Directamente con Flask**
```bash
python app.py
```

#### **Opción C: Con Variables de Entorno**
```bash
set FLASK_ENV=development
set FLASK_DEBUG=true
python app.py
```

## 🌐 **Uso de la Aplicación**

### **1. Acceso a la Interfaz**
- Abre tu navegador en: `http://localhost:5000`
- La aplicación se abrirá automáticamente si usas `run_web_app.py`

### **2. Prueba de Conexión (Opcional pero Recomendado)**
- Ingresa tu **Token de Figma** y **Library Key**
- Haz clic en **"Probar Conexión"**
- Verifica que la conexión sea exitosa antes de continuar

### **3. Configuración del Reporte**
- **Token de Figma**: Tu token de acceso personal
- **Library Key**: Clave de la biblioteca de componentes
- **Fecha de Inicio**: Fecha desde la cual obtener datos
- **Fecha de Fin**: Fecha hasta la cual obtener datos
- **Agrupar Por**: Componente o Equipo

### **4. Generación y Descarga**
- Haz clic en **"Generar y Descargar CSV"**
- Espera a que se procesen los datos
- El archivo CSV se descargará automáticamente

## 🔧 **Configuración Avanzada**

### **Variables de Entorno Disponibles**

```bash
# Configuración del servidor
FLASK_ENV=development          # Entorno (development/production/testing)
FLASK_DEBUG=true              # Modo debug
FLASK_HOST=0.0.0.0           # Host del servidor
FLASK_PORT=5000               # Puerto del servidor

# Configuración de la API
FIGMA_API_TIMEOUT=30          # Timeout de la API en segundos

# Configuración de archivos
TEMP_DIR=/path/to/temp        # Directorio de archivos temporales
MAX_FILE_SIZE=100             # Tamaño máximo de archivo en MB

# Configuración de fechas
MAX_DATE_RANGE_DAYS=1095      # Rango máximo de fechas en días

# Configuración de seguridad
SECRET_KEY=your_secret_key    # Clave secreta para sesiones
MAX_REQUESTS_PER_MINUTE=60    # Límite de requests por minuto
```

### **Configuración de Producción**

```bash
# En producción, usar configuración más estricta
export FLASK_ENV=production
export FLASK_DEBUG=false
export SECRET_KEY=your_very_secure_secret_key
export LOG_LEVEL=WARNING
```

## 📱 **Características de la Interfaz**

### **Sección de Prueba de Conexión**
- **Validación en tiempo real** de credenciales
- **Muestra de datos de ejemplo** para verificar acceso
- **Auto-completado** del formulario principal

### **Formulario Principal**
- **Validación automática** de fechas
- **Advertencias** para rangos muy amplios
- **Campos requeridos** claramente marcados

### **Indicadores de Estado**
- **Spinner de carga** durante el procesamiento
- **Mensajes de progreso** claros
- **Manejo de errores** con mensajes útiles

### **Resumen de Resultados**
- **Métricas clave** del reporte generado
- **Estadísticas visuales** fáciles de entender
- **Botón de descarga** prominente

## 🛠️ **Troubleshooting**

### **Problemas Comunes**

#### **1. Error: "No module named 'flask'**
```bash
# Solución: Instalar dependencias
pip install flask pandas requests
```

#### **2. Error: "Port already in use"**
```bash
# Solución: Cambiar puerto o detener proceso
set FLASK_PORT=5001
python app.py
```

#### **3. Error: "Template not found"**
```bash
# Solución: Verificar estructura de directorios
# Asegúrate de que templates/index.html existe
```

#### **4. Error: "Permission denied"**
```bash
# Solución: Ejecutar como administrador o cambiar permisos
# En Windows: Ejecutar CMD como administrador
# En Linux/Mac: sudo python app.py
```

### **Logs y Debugging**

La aplicación genera logs automáticamente:
- **Archivo de log**: `figma_analytics.log`
- **Consola**: Mensajes en tiempo real
- **Debug mode**: Información detallada de errores

## 🔒 **Seguridad**

### **Medidas Implementadas**
- **Validación de entrada** para todos los parámetros
- **Sanitización** de datos antes de procesar
- **Timeouts** para evitar ataques de denegación de servicio
- **Límites de tamaño** de archivo
- **Manejo seguro** de archivos temporales

### **Recomendaciones**
- **No compartir** tu token de Figma
- **Usar HTTPS** en producción
- **Configurar firewall** para limitar acceso
- **Monitorear logs** regularmente

## 📈 **Escalabilidad y Rendimiento**

### **Optimizaciones Implementadas**
- **Paginación automática** para datasets grandes
- **Procesamiento asíncrono** de requests
- **Manejo eficiente** de memoria
- **Archivos temporales** con limpieza automática

### **Para Uso en Producción**
- **Usar Gunicorn** o similar para WSGI
- **Configurar Nginx** como proxy reverso
- **Implementar cache** para requests frecuentes
- **Monitoreo** con herramientas como Prometheus

## 🤝 **Contribuciones**

### **Cómo Contribuir**
1. **Fork** el proyecto
2. **Crea** una rama para tu feature
3. **Commit** tus cambios
4. **Push** a la rama
5. **Abre** un Pull Request

### **Áreas de Mejora**
- **Tests automatizados** para la API
- **Más opciones de exportación** (Excel, JSON)
- **Dashboard de métricas** en tiempo real
- **Integración** con otras herramientas de análisis

## 📞 **Soporte**

### **Canales de Ayuda**
- **Issues de GitHub**: Para bugs y feature requests
- **Documentación**: Este README y comentarios en el código
- **Comunidad**: Foros y grupos de usuarios de Figma

### **Información de Contacto**
- **Mantenedor**: Tu nombre/organización
- **Email**: tu-email@ejemplo.com
- **Website**: https://tu-sitio.com

## 📄 **Licencia**

Este proyecto está bajo la licencia [MIT](LICENSE) - ver el archivo LICENSE para detalles.

---

## 🎉 **¡Disfruta usando Figma Analytics Web!**

Esta aplicación web transforma la experiencia de generar reportes de Figma Analytics de una tarea técnica a una experiencia visual intuitiva. ¡Esperamos que te sea muy útil!

**¿Tienes preguntas o sugerencias? ¡No dudes en contactarnos!**
