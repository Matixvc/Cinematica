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
git clone https://github.com/Matixvc/Cinematica.git

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

### Proyecto

La casita del perro — Cinemática de animación 3D low-poly sobre la relación familiar entre un padre y su hijo.

Unreal Engine 5.6.1.
Duración: 45 segundos.
Frecuencia: 24 fps.
Total: 1080 frames.
11 planos cinematográficos.

### Responsabilidades

- Matias: escenario, blocking y cámaras CAM00, CAM01, CAM02, CAM03, CAM03.1 y CAM04.
- Compañero 1: cámaras CAM05, CAM05.1, CAM06, CAM07 y CAM08.
- Compañeros 2 y 3: personajes y animaciones. Propuesta de división: padre e hijo respectivamente, con coordinación de objetos interactivos.

### Documentación

- Docs/Escaleta_01_Camaras.docx
- Docs/Escaleta_02_Animaciones.docx
- Docs/GUIA_COLABORACION.md

### Timeline compartida

| Plano | Tiempo |
|---|---|
| CAM00 | 0–3 s |
| CAM01 | 3–8 s |
| CAM02 | 8–12 s |
| CAM03 | 12–18 s |
| CAM03.1 | 18–19 s |
| CAM04 | 19–25 s |
| CAM05 | 25–28 s |
| CAM05.1 | 28–29 s |
| CAM06 | 29–33 s |
| CAM07 | 33–39 s |
| CAM08 | 39–45 s |

## Flujo de Trabajo

### Ramas existentes y responsables definitivos

El repositorio tiene tres ramas feature principales más `develop` y `main`:

| Rama | Responsable | Área |
|---|---|---|
| **feature/escenario-blocking** | Matias | Escenario, landscape, blocking e integración técnica |
| **feature/camaras** | Compañero 1 | Cámaras, encuadres y secuencias cinematográficas (CAM00-CAM08) |
| **feature/animaciones** | Compañeros 2 y 3 | Personajes y animaciones. División: padre (Compañero 2) e hijo (Compañero 3) con coordinación de objetos interactivos |
| **develop** | Equipo integrado | Integración de avances de las tres feature branches |
| **main** | Equipo / Producción | Versión estable y entregable para publicación |

### Flujo de trabajo por rama

**feature/escenario-blocking** (Matias):
- Base: `develop`
- Trabajar en escenario, landscape, blocking técnico
- Cuidado con Escena.umap: usar Git LFS lock al editar
- Pull Request hacia `develop` tras completar bloqueo

**feature/camaras** (Compañero 1):
- Base: `develop`
- Desarrollo de todas las cámaras CAM00 a CAM08
- Trabajar en LS_Cameras_45s.uasset con LFS lock
- Secuencias de cámara en subsecuencias separadas
- Pull Request hacia `develop` tras finalizar secuencias

**feature/animaciones** (Compañeros 2 y 3):
- Base: `develop`
- **Compañero 2**: Animación del padre - subsecuencia independiente
- **Compañero 3**: Animación del hijo - subsecuencia independiente
- Coordinación requerida para objetos interactivos
- Evitar editar simultáneamente las mismas pistas de animación
- Utilizar nombres únicos para variantes
- Pull Request hacia `develop` tras completar animaciones

### Flujo completo

1. Cada integrante parte de `develop`: `git checkout develop && git pull origin develop`
2. Crear rama específica o trabajar en la existente
3. Realizar cambios con `git lfs lock <archivo>` para archivos binarios críticos
4. Commit con mensajes descriptivos
5. Subir y crear Pull Request hacia `develop`
6. Revisión y fusión a `develop`: `git checkout develop && git pull origin develop && git merge --no-ff <rama>`
7. Integración a `main` cuando `develop` esté estable

**Reglas**:
- No permitir que todos editen simultáneamente Escena.umap o LS_Cinematica_Final.uasset
- Utilizar Pull Requests hacia `develop`
- Integración de `develop` hacia `main` cuando el proyecto esté estable
- Utilizar Git LFS locking para archivos binarios compartidos cuando sea adecuado
- Secuencias de animación independientes para evitar conflictos
- Preferir subsecuencias sobre edición directa en LS_Cinematica_Final.uasset

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