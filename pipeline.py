import pandas as pd

ANO_INICIAL = 2000
ANO_FINAL = 2026

COLUNAS_NUMERICAS = [
    "val_gerhidraulica",
    "val_gertermica",
    "val_gereolica",
    "val_gersolar",
    "val_carga",
    "val_intercambio"
]

dfs = []

for ano in range(ANO_INICIAL, ANO_FINAL + 1):

    print(f"Baixando {ano}...")

    url = (
        f"https://ons-aws-prod-opendata.s3.amazonaws.com/"
        f"dataset/balanco_energia_subsistema_ho/"
        f"BALANCO_ENERGIA_SUBSISTEMA_{ano}.parquet"
    )

    df = pd.read_parquet(url)

    for coluna in COLUNAS_NUMERICAS:
        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )

    dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)

df_final.to_parquet(
    "balanco_energia_ons.parquet",
    index=False
)

print()
print("Pipeline concluído!")
print("Linhas:", len(df_final))
print(
    "Período:",
    df_final["din_instante"].min(),
    "até",
    df_final["din_instante"].max()
)
print("Arquivo: balanco_energia_ons.parquet")