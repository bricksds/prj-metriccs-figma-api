# Figma Analytics - GitHub Pages

## 🚀 Despliegue en GitHub Pages

Esta es la versión estática de la aplicación Figma Analytics, optimizada para funcionar directamente en GitHub Pages.

### 📁 Estructura del Proyecto

```
prj-metriccs-figma-api/
├── index.html          # Aplicación principal (estática)
├── README_GH_PAGES.md  # Este archivo
└── .github/
    └── workflows/
        └── deploy.yml  # GitHub Actions para despliegue automático
```

### ⚠️ Limitaciones de la Versión Estática

Debido a las políticas CORS de los navegadores, esta versión tiene limitaciones:

- **❌ No puede llamar directamente a la API de Figma** desde el navegador
- **✅ Interfaz visual completa** para configuración
- **✅ Validación de fechas** en tiempo real
- **✅ Generación de CSV** (requiere datos de prueba)

### 🔧 Configuración de GitHub Actions

Crea el archivo `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./
```

### 📋 Pasos para Desplegar

1. **Sube los archivos** a tu repositorio de GitHub
2. **Habilita GitHub Pages** en Settings → Pages
3. **Selecciona la fuente** como "GitHub Actions"
4. **El despliegue será automático** en cada push

### 🌐 URL de Acceso

Tu aplicación estará disponible en:
```
https://tu-usuario.github.io/prj-metriccs-figma-api/
```

### 💡 Soluciones para CORS

#### Opción 1: Proxy CORS (Recomendada)
Usa un servicio como `cors-anywhere` o `allorigins`:

```javascript
// En el código JavaScript, cambia:
const response = await fetch(`https://api.figma.com/v1/analytics/...`);

// Por:
const response = await fetch(`https://api.allorigins.win/raw?url=${encodeURIComponent('https://api.figma.com/v1/analytics/...')}`);
```

#### Opción 2: Aplicación Flask Local
Para funcionalidad completa, descarga y ejecuta la aplicación Flask local:

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/prj-metriccs-figma-api.git

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python run_web_app.py
```

### 🎯 Características de la Versión Estática

- ✅ **Interfaz visual completa** con Bootstrap 5
- ✅ **Validación de formularios** en tiempo real
- ✅ **Responsive design** para móviles y desktop
- ✅ **Manejo de errores** con mensajes claros
- ✅ **Generación de CSV** (con datos de prueba)
- ✅ **Métricas visuales** de resultados

### 🔒 Seguridad

- **No almacena tokens** en el navegador
- **Validación client-side** de parámetros
- **Manejo seguro** de datos sensibles

### 📱 Compatibilidad

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### 🐛 Solución de Problemas

#### Error 404 en GitHub Pages
- Verifica que el archivo se llame `index.html` (no `Index.html`)
- Asegúrate de que esté en la raíz del repositorio
- Espera 5-10 minutos después del push

#### Error CORS
- Usa la aplicación Flask local para funcionalidad completa
- O implementa un proxy CORS como se muestra arriba

#### No se descarga el CSV
- Verifica que el navegador permita descargas
- Revisa la consola del navegador para errores

### 📞 Soporte

Para problemas específicos de GitHub Pages:
1. Revisa los logs de GitHub Actions
2. Verifica la configuración en Settings → Pages
3. Consulta la documentación oficial de GitHub Pages

---

**Nota**: Esta versión estática es ideal para demostraciones y pruebas de interfaz. Para uso en producción con datos reales, se recomienda la aplicación Flask local.
