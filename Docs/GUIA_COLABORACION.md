# Guía de Colaboración - Cinematica Bloqueo 45s

## Integrantes y Responsabilidades

### Matias (Líder de proyecto)
- **Escenario**: Landscape, props, entorno residencial
- **Blocking**: Configuración inicial de bloqueo en LS_Cameras_45s
- **Cámaras**: CAM00, CAM01, CAM02, CAM03, CAM03.1 y CAM04
- **Rama existente**: `feature/escenario-blocking`
- **Archivos permitidos**: Escena.umap (con LFS lock), LS_Cameras_45s.uasset, Landscape, materiales del entorno

### Compañero 1
- **Cámaras**: CAM05, CAM05.1, CAM06, CAM07, CAM08
- **Rama existente**: `feature/camaras`
- **Archivos permitidos**: LS_Cameras_45s.uasset (referencia), secuencias de cámara, config de Sequencer

### Compañero 2
- **Personajes**: BP_Father_ThirdPersonCharacter
- **Animaciones**: Secuencia del padre
- **Rama existente**: `feature/animaciones` (trabajar en subsecuencia padre)
- **Archivos permitidos**: Secuencias de animación del padre, BP del padre

### Compañero 3
- **Personajes**: BP_Son_ThirdPersonCharacter
- **Animaciones**: Secuencia del hijo
- **Rama existente**: `feature/animaciones` (trabajar en subsecuencia hija)
- **Archivos permitidos**: Secuencias de animación del hijo, BP del hijo

## Ramas del Proyecto

### main
- Rama estable y entregable
- Solo se fusionan cambios aprobados desde `develop`
- Representa la versión lista para publicación

### develop
- Rama de integración de los avances de los cuatro integrantes
- Punto de fusión de todas las ramas `feature/`
- Debe estar estable antes de liberar a `main`

### feature/escenario-blocking
- Trabajo en el escenario, landscape, blocking e integración técnica
- Base: `develop`
- Responsable: Matias
- Flujo: `git checkout develop && git pull origin develop && git checkout -b feature/escenario-blocking` (o reutilizar rama existente si ya existe)

### feature/camaras
- Desarrollo de cámaras, encuadres y secuencias cinematográficas
- Base: `develop`
- Responsable: Compañero 1
- Flujo: `git checkout develop && git pull origin develop && git checkout -b feature/camaras` (o reutilizar rama existente si ya existe)

### feature/animaciones
- Animaciones y secuencias correspondientes (división padre/hijo)
- Base: `develop`
- Responsables: Compañero 2 (padre) e Compañero 3 (hijo), coordinación requerida
- Flujo: `git checkout develop && git pull origin develop && git checkout -b feature/animaciones`
- **Importante**: Trabajar en subsecuencias separadas dentro de esta rama:
  - Compañero 2: animación del padre - mantener pistas separadas
  - Compañero 3: animación del hijo - mantener pistas separadas
  - Evitar editar simultáneamente las mismas pistas de animación

## Flujo de Trabajo

### 1. Sincronizar o crear una rama feature
```bash
git checkout develop
git pull origin develop
```
- Las tres ramas feature ya existen: `feature/escenario-blocking`, `feature/camaras`, `feature/animaciones`
- Si es necesario crear una nueva (solo si realmente no existe):
  `git checkout -b feature/escenario-blocking`
  `git checkout -b feature/camaras`
  `git checkout -b feature/animaciones`

### 2. Desarrollar y hacer commits
- Realizar cambios en los archivos correspondientes
- Commit con mensajes descriptivos
- Usar Git LFS locking para archivos binarios grandes cuando sea necesario
- **Importante**: Bloquear archivos LFS antes de editarlos (`git lfs lock <archivo.uasset>`)
- **Importante**: Desbloquear y subir cambios después de commit (`git lfs unlock <archivo.uasset>`)

### 3. Subir la rama y crear Pull Request
```bash
git push -u origin <rama-asignada>
```
- Crear Pull Request hacia `develop`
- Solicitar revisión de un compañero
- Resolver conflictos antes de fusionar

### 4. Fusionar a develop
- Una vez aprobado el PR, fusionar a `develop`
- `git checkout develop && git pull origin develop && git merge --no-ff <rama-asignada>`
- Eliminar la rama feature después de fusionar

### 5. Integración a main
- Cuando `develop` esté estable y todas las features estén completadas
- `git checkout main && git pull origin main && git merge --no-ff develop`
- Crear tag de versión si corresponde

## Archivos Binarios y Prevención de Conflictos en Unreal

### Mapas (.umap)
- No permitir que dos personas editen el mismo mapa simultáneamente
- Matias es el responsable principal del mapa Escena.umap
- Si es necesario editar, desbloquear LFS, editar, y volverse a bloquear
- Realizar backups antes de ediciones significativas

### Secuencias (.uasset)
- Secuencias de animación independientes cuando sea posible
- Utilizar subsecuencias (SubSequencer) para partes específicas
- LS_Cinematica_Final.uasset debe ser editado con cuidado
- Cada integrante debe trabajar en sus subsecuencias asignadas
- **Nunca editar simultáneamente las mismas pistas de animación**

### Subsecuencias recomendadas
- `LS_Cameras_00_04`: Matias (cámaras 00, 01, 02, 03, 03.1, CAM04)
- `LS_Cameras_05_08`: Compañero 1 (cámaras CAM05, CAM05.1, CAM06, CAM07, CAM08)
- Subsecuencia independiente para animación del padre
- Subsecuencia independiente para animación del hijo
- LS_Cameras_45s: referencia del bloqueo actual y base del montaje

### Líneas de archivo
- Matias: Content/Animacion/Cinematica/LS_Cameras_00_04
- Compañero 1: Content/Animacion/Cinematica/LS_Cameras_05_08
- Compañero 2: Content/Animacion/Personajes/padre/
- Compañero 3: Content/Animacion/Personajes/hijo/

## Comandos Útiles

```bash
# Ver estado LFS
git lfs status

# Bloquear archivo LFS antes de editar
git lfs lock nombre_archivo.uasset

# Desbloquear archivo LFS
git lfs unlock nombre_archivo.uasset

# Ver quién tiene el bloqueo
git lfs locks nombre_archivo.uasset

# Ver estado de ramas
git branch -a

# Sincronizar con develop
git checkout develop && git pull origin develop

# Subir rama feature
git push -u origin <rama>
```

## Checklist antes de fusionar un Pull Request a `develop`

- [ ] Código y assets compatibles con UE 5.6.1
- [ ] El mapa principal carga sin errores
- [ ] No hay referencias rotadas a assets locales
- [ ] Git LFS desbloqueado y cambios subidos
- [ ] Secuencias de animación desbloqueadas
- [ ] Documentación actualizada (README, GUIA_COLABORACION.md)
- [ ] Commit de mensaje profesional y descriptivo

## Checklist después de fusionar a `develop`

- [ ] Verificar que el build en UE 5.6.1 aún funciona
- [ ] Sincronizar repositorios locales de todos los integrantes
- [ ] Revisar que no haya conflictos locales sin resolver
- [ ] Actualizar el estado del proyecto si es necesario