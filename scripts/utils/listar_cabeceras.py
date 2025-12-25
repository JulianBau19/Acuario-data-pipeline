
from acuario.config import RAW
from acuario.io_load import leer_excels

def main():
    dfs = leer_excels(RAW)  # lee todos los .xlsx en data/raw
    for nombre, df in dfs.items():
        print(f"\n--- {nombre} ---")
        print(df.head())    #  head() solo muestra primeras 5 filas

if __name__ == "__main__":
    main()
