"""
Pipeline de coleta e consolidação do Balanço de Energia por Subsistema (ONS).

Baixa os arquivos anuais publicados pelo ONS (2000 até o ano mais recente
disponível), padroniza os tipos de coluna, consolida tudo em um único
DataFrame e valida a base antes de gravar o Parquet final.

Uso:
    python pipeline.py
"""

import sys
from datetime import datetime

import pandas as pd

ANO_INICIAL = 2000
ANO_FINAL = datetime.now().year  # sempre tenta até o ano corrente

COLUNAS_NUMERICAS = [
    "val_gerhidraulica",
    "val_gertermica",
    "val_gereolica",
    "val_gersolar",
    "val_carga",
    "val_intercambio",
]

SUBSISTEMAS_ESPERADOS = {
    "NORTE",
    "NORDESTE",
    "SUL",
    "SUDESTE/CENTRO-OESTE",
    "SISTEMA INTERLIGADO NACIONAL",
}

CAMINHO_SAIDA = "balanco_energia_ons.parquet"


def baixar_ano(ano: int) -> pd.DataFrame | None:
    """Baixa e padroniza o arquivo de um ano. Retorna None se o ano falhar
    (por exemplo, ano ainda não publicado pelo ONS)."""
    url = (
        "https://ons-aws-prod-opendata.s3.amazonaws.com/"
        "dataset/balanco_energia_subsistema_ho/"
        f"BALANCO_ENERGIA_SUBSISTEMA_{ano}.parquet"
    )
    try:
        print(f"Baixando {ano}...")
        df = pd.read_parquet(url)
    except Exception as erro:
        print(f"⚠️  Não foi possível baixar {ano}: {erro}")
        return None

    for coluna in COLUNAS_NUMERICAS:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

    return df


def validar_base(df: pd.DataFrame) -> list[str]:
    """Roda checagens básicas de qualidade na base consolidada.
    Retorna a lista de problemas encontrados (vazia = tudo certo)."""
    problemas = []

    # 1. A base não pode estar vazia
    if len(df) == 0:
        problemas.append("Base consolidada está vazia.")
        return problemas  # sem dados, não faz sentido rodar as checagens seguintes

    # 2. Colunas obrigatórias precisam existir
    colunas_obrigatorias = {"din_instante", "nom_subsistema", *COLUNAS_NUMERICAS}
    faltantes = colunas_obrigatorias - set(df.columns)
    if faltantes:
        problemas.append(f"Colunas obrigatórias ausentes: {sorted(faltantes)}")

    # 3. din_instante precisa ser um datetime válido, sem nulos
    if "din_instante" in df.columns:
        instantes = pd.to_datetime(df["din_instante"], errors="coerce")
        n_invalidos = instantes.isna().sum()
        if n_invalidos > 0:
            problemas.append(f"{n_invalidos} valores de din_instante inválidos/nulos.")

    # 4. Subsistemas devem bater com os 5 esperados (nem a mais, nem a menos)
    if "nom_subsistema" in df.columns:
        subsistemas_encontrados = set(df["nom_subsistema"].dropna().unique())
        inesperados = subsistemas_encontrados - SUBSISTEMAS_ESPERADOS
        faltando = SUBSISTEMAS_ESPERADOS - subsistemas_encontrados
        if inesperados:
            problemas.append(f"Subsistemas inesperados na base: {sorted(inesperados)}")
        if faltando:
            problemas.append(f"Subsistemas esperados e não encontrados: {sorted(faltando)}")

    # 5. Sem linhas duplicadas de (instante, subsistema)
    if {"din_instante", "id_subsistema"}.issubset(df.columns):
        duplicadas = df.duplicated(subset=["din_instante", "id_subsistema"]).sum()
        if duplicadas > 0:
            problemas.append(f"{duplicadas} linhas duplicadas em (din_instante, id_subsistema).")

    # 6. Carga não pode ser negativa (geração pode, por convenção de intercâmbio,
    #    mas carga negativa indica erro de dado)
    if "val_carga" in df.columns:
        n_negativos = (df["val_carga"] < 0).sum()
        if n_negativos > 0:
            problemas.append(f"{n_negativos} valores de val_carga negativos.")

    # 7. Checagem de completude: nº de timestamps distintos vs. intervalo esperado
    if "din_instante" in df.columns and len(df) > 0:
        instantes = pd.to_datetime(df["din_instante"], errors="coerce").dropna()
        if len(instantes) > 0:
            horas_esperadas = pd.date_range(instantes.min(), instantes.max(), freq="h")
            horas_faltando = len(horas_esperadas) - instantes.dt.floor("h").nunique()
            if horas_faltando > 0:
                # Aviso, não bloqueia — falhas pontuais de coleta do próprio ONS acontecem
                print(f"ℹ️  Aviso: {horas_faltando} horas sem nenhum registro no período coberto.")

    return problemas


def main() -> None:
    dfs = []
    for ano in range(ANO_INICIAL, ANO_FINAL + 1):
        df_ano = baixar_ano(ano)
        if df_ano is not None:
            dfs.append(df_ano)

    if not dfs:
        print("❌ Nenhum ano foi baixado com sucesso. Abortando.")
        sys.exit(1)

    df_final = pd.concat(dfs, ignore_index=True)

    print()
    print("Validando base consolidada...")
    problemas = validar_base(df_final)

    if problemas:
        print("❌ Validação encontrou os seguintes problemas:")
        for p in problemas:
            print(f"  - {p}")
        print()
        print("O arquivo NÃO foi gravado. Corrija os problemas acima antes de prosseguir.")
        sys.exit(1)

    print("✅ Validação concluída sem problemas.")

    df_final.to_parquet(CAMINHO_SAIDA, index=False)

    print()
    print("Pipeline concluído!")
    print("Linhas:", f"{len(df_final):,}".replace(",", "."))
    print("Período:", df_final["din_instante"].min(), "até", df_final["din_instante"].max())
    print("Subsistemas:", sorted(df_final["nom_subsistema"].dropna().unique()))
    print("Arquivo:", CAMINHO_SAIDA)


if __name__ == "__main__":
    main()
