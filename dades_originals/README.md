# Dades originals

Els arxius historic.csv no formen part de les dades que es van descarregar, sinó que es van crear per facilitar el tractament de les dades.

## historic.csv (general)

Conté la informació clau per identificar els diferents conjunts de dades:

- **identificador**: Identificador únic per cada conjunt de dades i nom de la subcarpeta on es troben les dades.
- **titol**
- **resum**
- **darrera_actualitzacio_web**: Data d'actualització del conjunt de dades a la web
- **etiqueta**: Categoria principal del conjunt de dades.
- **categories**: Categories adicionals que descriuen el conjunt de dades.
- **frequencia_actualitzacio**: Freqüència d'actualització teòrica a la web (alguns conjunts de dades van deixar d'actualitzar-se)
- **data_descarrega**: Data en què es van descarregar les dades

## historic.csv (específic)

A cada conjunt de dades hi ha un document amb informació dels arxius que conté:

- **web_date**: Data del fitxer a la web
- **name**: Nom del fitxer
- **download_date**: Data en què es va descarregar