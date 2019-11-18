# me2_vna_instvirtual

## Preparar environment

```bash
conda activate me2
conda install -y --file env.packages
conda install -y -c conda-forge pyvisa
```

## Prerequisitos del VNA

* Tiene que estar en modo NA
* Cantidad de traces: 4

## Como correr el backend

* Abrir una consola
    ```bash
    conda activate me2 # solo si esta instalado conda, en la raspberry no hace falta
    cd backend
    python3 app.py
    ```

## Como correr el frontend

* Abrir una consola
    ```bash
    cd ui
    node app.js
    ```

## Recursos:

* Fieldfox Programming Guide: http://na.support.keysight.com/fieldfox/help/Programming/webhelp/FFProgrammingHelp.htm

* 