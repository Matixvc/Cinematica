# Flujo de Ramas y Responsabilidades - Cinematica UE5.6.1

## Diagramas de Flujo

```
                    +------------------+
                    |      main        |
                    | (Entregable,     |
                    |   versiones)     |
                    +---------+--------+
                              |
                              | Pull Request approvd
                              v
                    +---------+--------+
                    |    develop       |
                    | (Integración,    |
                    |   avances)       |
                    +---------+--------+
                           / | \
                          /  |  \
                         /   |   \
                        /    |    \
           +---------+  +---------+  +---------+
           |feature/  |  |feature/  |  |feature/  |
           |escenario-  |  |camaras    |  |personajes|
           |blocking   |  |           |  |          |
           +---------+  +---------+  +---------+
                           \   |   /
                            \  |  /
                             \ | /
                      +---------+--------+
                      |   feature/animas |
                      |   (animaciones)  |
                      +--------------------+
```

## Responsabilidades por Rama

### main
- **Propósito**: Versión estable y entregable
- **Acceso**: Todos los integrantes pueden ver, solo mantenedores pueden fusionar
- **Cuándo actualizar**: Cuando develop esté estable y todas las features estén completadas
- **Protección**: Branch protection enabled en GitHub

### develop
- **Propósito**: Integración de los avances de los cuatro integrantes
- **Acceso**: Todos los integrantes pueden crear PRs hacia develop
- **Cuándo actualizar**: Después de fusionar todas las feature branches
- **Checklist antes de fusionar**:
  - [ ] Todas las feature branches fusionadas
  - [ ] Builds exitosos en UE 5.6.1
  - [ ] Mapas principales cargan correctamente
  - [ ] No hay conflictos de archivos binarios sin resolver

### feature/escenario-blocking
- **Propósito**: Escenario, Landscape, blocking e integración técnica
- **Responsable**: Matixvc
- **Archivos clave**:
  - Escena.umap
  - Landscape con capas Grass, Dirt, Path
  - Materiales del entorno
  - Setup de iluminación básica

### feature/camaras
- **Propósito**: Cámaras, encuadres y cinematografía
- **Responsable**: Compañero 2
- **Archivos clave**:
  - LS_Cinematica_Final.uasset (o secuencias individuales)
  - Configuración de cámaras en Sequencer
  - Referencias y animaciones de cámara

### feature/personajes
- **Propósito**: Personajes, materiales y preparación de recursos
- **Responsable**: Compañero 3
- **Archivos clave**:
  - BP_Father_ThirdPersonCharacter.uasset
  - BP_Son_ThirdPersonCharacter.uasset
  - Materiales y texturas de personajes
  - Configuración de animación

### feature/animaciones
- **Propósito**: Animaciones y secuencias correspondientes
- **Responsable**: Compañero 4
- **Archivos clave**:
  - Secuencias de animación en Sequencer
  - Montajes y poses de personajes
  - Montajes de cámara con animación

## Prevención de Conflictos de Archivos Binarios

### Reglas Críticas

1. **Mapa principal (Escena.umap)**:
   - Solo Matixvc edita directamente
   - Otros integrantes realizan cambios en copias locales y proponen PR
   - Si es necesario editar, desbloquear LFS, editar, y volverse a bloquear

2. **Secuencia principal (LS_Cinematica_Final.uasset)**:
   - Compañero 2 es el responsable principal para secuencias cinematográficas
   - Animaciones independientes deben mantenerse en subsecuencias separadas
   - Evitar editar las mismas pistas de animación simultáneamente

3. **Materiales y Texturas**:
   - Compañero 3 es responsable de materiales de personajes y entorno
   - No editar simultáneamente los mismos materiales
   - Utilizar nombres únicos para variantes de materiales

4. **Landscape**:
   - Matixvc es responsable del Landscape con capas Grass, Dirt, Path
   - Las capas no deben entrarse en conflicto (cada uno trabaja en áreas diferentes)

### Flujo para Ediciones Críticas

```bash
# 1. Verificar estado LFS actual
git lfs status

# 2. Bloquear el archivo antes de editar
git lfs lock Escena.umap

# 3. Realizar ediciones
# ... (editar el mapa) ...

# 4. Desbloquear y subir cambios
git lfs unlock Escena.umap
git add Escena.umap
git commit -m "feat: update scene blocking - [descripción corta]"
git push origin feature/escenario-blocking

# 5. Crear Pull Request hacia develop
# ... (en GitHub web) ...
```

## Checklist de Integración

### Antes de fusionar un Pull Request a `develop`:

- [ ] Código y assets compatibles con UE 5.6.1
- [ ] El mapa principal carga sin errores
- [ ] No hay referencias rotadas a assets locales
- [ ] Git LFS desbloqueado y cambios subidos
- [ ] README y documentación actualizados si es necesario
- [ ] Commit de mensaje profesional y descriptivo

### Después de fusionar a `develop`:

- [ ] Verificar que el build en UE 5.6.1 aún funciona
- [ ] Sincronizar repositorios locales de todos los integrantes
- [ ] Revisar que no haya conflictos locales sin resolver
- [ ] Actualizar el estado del proyecto si es necesario