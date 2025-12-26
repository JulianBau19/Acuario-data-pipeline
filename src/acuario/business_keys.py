"""
Business keys de tablas CLN.
Definen cómo se deduplican las cargas desde STG.

Regla:
- Cada tabla tiene UNA business key (simple o compuesta)
- Las tablas marcadas como unused se ignoran
"""

BUSINESS_KEYS = {
    "almacenes": {
        "keys": ["cod_almacen"],
        "used": True,
    },
    "articulos": {
        "keys": ["cod_articulo"],
        "used": True,
    },
    "clientes": {
        "keys": ["cod_cliente"],
        "used": True,
    },
    "facturas": {
        "keys": ["tipo_factura", "num_factura"],
        "used": True,
    },
    "facturas_linea": {
        "keys": ["tipo_linea","num_factura", "num_linea"],
        "used": True,
    },
    "entradas": {
        "keys": ["cod_entrada"],
        "used": True,
    },
    "entradas_linea": {
        "keys": ["cod_entrada", "num_linea"],
        "used": True,
    },
    "familias": {
        "keys": ["codigo_familia"],
        "used": True,
    },
    "listado_de_tarifas": {
        "keys": ["cod_articulo"],
        "used": True,
    },
    "proveedores": {
        "keys": ["cod_proveedor"],
        "used": True,
    },
    "stock": {
        "keys": ["cod_articulo"],
        "used": True,
    },


    # TABLAS NO UTILIZADAS
 
    "costos_mercaderias": {
        "keys": [],
        "used": False,
    },
    "tarifas": {
        "keys": [],
        "used": False,
    },
}
