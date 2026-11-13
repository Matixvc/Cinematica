# Estructura del Proyecto - Cinematica UE5.6.1

## Directorio Raíz

```
/Cinematica/
  .gitignore
  .gitattributes
  Cinematica.uproject
  Config/
  Content/
    /Animacion/
      /Cinematica/
        LS_Cinematica_Final.uasset
      /Escenario/
        Escena.umap
        Landscape_01
      /Personajes/
        BP_Father_ThirdPersonCharacter.uasset
        BP_Son_ThirdPersonCharacter.uasset
        Fhater_BP_ThirdPersonCharacter1.uasset
        Son_BP_ThirdPersonCharacter.uasset
      /Recursos/
        /Material/
          Casa_NoneMap_baseColor_Mat_3e64a96f60.uasset
          MA_lowpolyGrass_120dfcc824.uasset
          M_BaseColor_c781d8634b.uasset
          M_ColorMaster_ae15093014.uasset
          M_Landscape_Master_8ddf63a90e.uasset
          M_UE4Man_Body_6947a97098.uasset
          Material_003_8c5515eb3c.uasset
          WoodenCrate_Diffuse_Mat_e52203713d.uasset
        /MaterialFunction/
          ML_GlossyBlack_Latex_UE4_8bbd553ad7.uasset
          ML_Plastic_Shiny_Beige_854ff1c14b.uasset
          ML_Plastic_Shiny_Beige_LOGO_5613cb6110.uasset
          ML_SoftMetal_UE4_96cb80f75e.uasset
          PN_Bending_8d44768338.uasset
          PN_MultiBend_0a4572af07.uasset
          PN_WindAnimation_17155630cc.uasset
        /MaterialInstanceConstant/
          canopy_*.uasset
          Grass_02_Brush_*_Mat_*.uasset
          MI_Fence_03_62315e966e.uasset
          MI_Manny_01_New_*.uasset
          MI_Manny_02_New_04c058aa15.uasset
          M_UE4Man_ChestLogo_bc12a6141a.uasset
          PBR_001_158238e821.uasset
          PBR_cf90414f78.uasset
          WoodenCrate_Material_1730c56663.uasset
        /Recursos/Texture2D/
          doghouse0908_PBR_*.uasset
          grass_02_Brush_*_Vec_*.uasset
          grass_05_brush_04_*.uasset
          T_*.uasset
      /__ExternalActors__/
      /Extra/
/Docs/
  CONTRIBUTING.md
  PROJECT_STRUCTURE.md
  WORKFLOW.md
/Saved/
/Intermediate/
/DerivedDataCache/
/Binaries/
/Plugins/
```

## Mapas Principales

### Escena.umap
- Mapa principal de la cinemática "La casita del perro"
- 404 actores distribuidos en el escenario residencial
- Landscape con capas Grass, Dirt y Path
- 5 cámaras cinematográficas etiquetadas

### Niveles Adicionales
- Lvl_ThirdPerson: Niveles de la plantilla Third Person original (no forman parte de la cinemática principal, contenido de referencia)

## Secuencias Principales

### LS_Cinematica_Final.uasset
- Secuencia principal de cinematografía
- Contiene las 5 cámaras cinematográficas identificadas
- Punto de referencia para la edición de secuencias

## Personajes

### BP_Father_ThirdPersonCharacter.uasset
- Personaje del padre que construye la casa para perros

### BP_Son_ThirdPersonCharacter.uasset
- Personaje del hijo que utiliza teléfono y audífonos

### Fhater_BP_ThirdPersonCharacter1.uasset
- Variante adicional del personaje del padre

### Son_BP_ThirdPersonCharacter.uasset
- Variante adicional del personaje del hijo

## Landscape

### Landscape_01
- Landscape con capas Grass, Dirt y Path
- Escenario residencial donde ocurre la cinemática

## Recursos Externos y Plugins

### Plugins Verificados
- ModelingToolsEditorMode
- GameplayStateTree

### Assets Externos
- doghouse0908_PBR_: Activo principal de la casa para perros
- Manny*: Personajes de referencia (pueden ser de la plantilla Third Person)
- WoodenCrate*: Assets de props del entorno

**Nota**: Verificar licencias de assets externos antes de redistribución pública. Algunos modelos pueden tener restricciones de uso.