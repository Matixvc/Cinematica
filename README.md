# La casita del perro

**Cinemática Low-Poly desarrollada en Unreal Engine 5.6.1**

[![Unreal Engine 5.6.1](https://img.shields.io/badge/Unreal%20Engine-5.6.1-blue.svg)](https://www.unrealengine.com/es/)
[![Git LFS](https://img.shields.io/badge/Git%20LFS-enabled-green.svg)](https://git-lfs.com/)
[![Status: In Production](https://img.shields.io/badge/Status-In%20Production-orange.svg)]

## Descripción

Cinemática animada low-poly de aproximadamente 40 segundos que narra la historia de un padre construyendo una casa para perros mientras su hijo permanece distraído con su teléfono y audífonos. El proyecto explora la dinámica familiar y la distracción digital en un entorno residencial low-poly.

## Características

- **Entorno low-poly**: Estilo artístico estilizado con geometría simplificada y materiales optimizados
- **Escenario residencial**: Casas, árboles, vallas, vegetación y herramientas detalladas
- **Personajes**: Padre construyendo y hijo utilizando dispositivos móviles
- **Landscape con capas**: Grass, Dirt y Path para caminos y vegetación
- **Cinematografía mediante Sequencer**: Cinco cámaras cinematográficas con encuadres cuidadosamente diseñados
- **Pipeline colaborativo**: Estructura organizada para cuatro integrantes con ramas Git dedicadas

## Tecnologías

- Unreal Engine 5.6.1
- Sequencer y Cinematografía
- Git y GitHub para control de versiones
- Git LFS para archivos binarios grandes
- Assets y animaciones integradas

## Requisitos

- Unreal Engine 5.6.1 instalado
- Git instalado
- Git LFS configurado
- Acceso al repositorio GitHub

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Matixvc/Cinematica-UE56.git

# Descargar recursos LFS
git lfs pull

# Abrir el proyecto
# Ejecutar: C:\Users\matia\Documents\Cinematica\Cinematica.uproject
```

## Estructura del proyecto

```
/Content/
  /Animacion/
    /Cinematica/          # Secuencias y assets principales
    /Escenario/           # Mapa y landscape
    /Personajes/          # Blueprints de personajes
    /Recursos/            # Materiales, texturas y funciones
  /Extra/                 # Content externo
  /__ExternalActors__/    # Actors externos

/Config/                  # Configuración del proyecto
/Cinematica.uproject     # Archivo principal del proyecto

## Equipo y Responsabilidades

| Integrante | Responsabilidad |
|------------|-----------------|
| Matixvc | Escenario, blocking e integración técnica |
| Compañero 2 | Cámaras, encuadres y cinematografía |
| Compañero 3 | Personajes, materiales y preparación de recursos |
| Compañero 4 | Animaciones y secuencias correspondientes |

## Flujo de Trabajo

1. **main**: Rama estable y entregable. Solo se fusionan cambios aprobados desde `develop`.
2. **desarroll**: Integración de los avances de los cuatro integrantes. Los feature branches se fusionan aquí.
3. **feature/escenario-blocking**: Trabajo en el escenario, landscape, blocking e integración técnica.
4. **feature/camaras**: Desarrollo de cámaras, encuadres y secuencias cinematográficas.
5. **feature/personajes**: Personajes, materiales y preparación de recursos.
6. **feature/animaciones**: Animaciones y secuencias correspondientes.

**Reglas**:
- No permitir que todos editen simultáneamente Escena.umap o LS_Cinematica_Final.uasset
- Utilizar Pull Requests hacia `desarroll`
- Integración de `desarroll` hacia `main` cuando el proyecto esté estable
- Utilizar Git LFS locking para archivos binarios compartidos cuando sea adecuado
- Secuencias de animación independientes para evitar conflictos

## Estado del Proyecto

- ✅ Proyecto migrado de UE 5.8.4 a UE 5.6.1
- ✅ Mapa principal: Escena.umap
- ✅ Secuencia principal: LS_Cinematica_Final.uasset
- ✅ 5 cámaras cinematográficas identificadas
- ✅ Landscape con capas Grass, Dirt y Path
- ⚠️ Trabajo colaborativo en progreso (4 integrantes)
- ⚠️ Documentación adicional por crear

## Créditos y Licencias

- **Matixvc**: Dirección y producción del proyecto
- **Compañeros**: Contribución de escenas, personajes, animaciones y cinematografía
- **Assets externos**: Verificar licencias antes de redistribución pública
- **Licencia**: Los recursos deben verificarse para derechos de redistribución. No se agrega licencia MIT automática sin derechos sobre todos los recursos.

## Próximos Pasos

- Crear ramas feature para cada integrante
- Establecer flujo de Pull Requests y revisión de código
- Implementar Git LFS locking para activos compartidos
- Continuar desarrollo de cinemática y cinematografía