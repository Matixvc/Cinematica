# Guía de Colaboración - Cinematica UE5.6.1

## Integrantes

1. **Matixvc** - Escenario, blocking e integración técnica
2. **Compañero 2** - Cámaras, encuadres y cinematografía
3. **Compañero 3** - Personajes, materiales y preparación de recursos
4. **Compañero 4** - Animaciones y secuencias correspondientes

## Ramas del Proyecto

### main
- Rama estable y entregable
- Solo se fusionan cambios aprobados desde `desarroll`
- Representa la versión lista para producción

### develop
- Rama de integración de los avances de los cuatro integrantes
- Punto de fusión de todas las ramas `feature/`
- Estable antes de liberar a `main`

### feature/escenario-blocking
- Trabajo en el escenario, landscape, blocking e integración técnica
- Responsable: Matixvc
- Base: `desarroll`

### feature/camaras
- Desarrollo de cámaras, encuadres y secuencias cinematográficas
- Responsable: Compañero 2
- Base: `desarroll`

### feature/personajes
- Personajes, materiales y preparación de recursos
- Responsable: Compañero 3
- Base: `desarroll`

### feature/animaciones
- Animaciones y secuencias correspondientes
- Responsable: Compañero 4
- Base: `desarroll`

## Flujo de Trabajo

### 1. Crear una rama feature
```bash
git checkout develop
git pull origin develop
git checkout -b feature/escenario-blocking
```

### 2. Desarrollar y hacer commits
- Realizar cambios en los archivos correspondientes
- Commit con mensajes descriptivos
- Usar Git LFS locking para archivos binarios grandes cuando sea necesario

### 3. Subir la rama y crear Pull Request
```bash
git push -u origin feature/escenario-blocking
```
- Crear Pull Request hacia `desarroll`
- Solicitar revisión de un compañero
- Resolver conflictos antes de fusionar

### 4. Fusionar a develop
- Una vez aprobado el PR, fusionar a `desarroll`
- `git checkout develop && git pull origin develop && git merge --no-ff feature/escenario-blocking`
- Eliminar la rama feature después de fusionar

### 5. Integración a main
- Cuando `desarroll` esté estable y todas las features estén completadas
- `git checkout main && git pull origin main && git merge --no-ff develop`
- Crear tag de versión si corresponde

## Consejos para Evitar Conflictos en Unreal

### Archivos Binarios
- Unreal utiliza archivos binarios que Git no puede fusionar automáticamente
- Designar un responsable por tipo de archivo
- Utilizar `git lfs lock <archivo>` antes de editar archivos críticos

### Mapas (.umap)
- No permitir que dos personas editen el mismo mapa simultáneamente
- Matixvc es el responsable principal del mapa Escena.umap
- Realizar backups antes de ediciones significativas

### Secuencias ( .uasset )
- Secuencias de animación independientes cuando sea posible
- Utilar subsecuencias (SubSequencer) para partes específicas
- LS_Cinematica_Final.uasset debe ser editado con cuidado

### Carpetas separadas
- Mantener los personajes en carpetas separadas
- Content/Animacion/Personajes/ para assets de personajes
- Evitar superposición de rutas de archivo

## Comandos Útiles

```bash
# Ver estado LFS
git lfs status

# Bloquear archivo LFS
git lfs lock nombre_archivo.uasset

# Desbloquear archivo LFS
git lfs unlock nombre_archivo.uasset

# Ver quién tiene el bloqueo
git lfs locks nombre_archivo.uasset
```