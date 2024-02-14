"""Taller evaluable"""

import glob

import pandas as pd


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #
    files = glob.glob(f"{input_directory}/*")
    dataframes = [
        pd.read_csv(
            file,
            header=None,
            delimiter="\t",
            names=["line"],
            index_col=None,
        )
        for file in files
    ]

    dataframe = pd.concat(dataframes, ignore_index=True)

    return dataframe


def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas.
    #
    dataframe = dataframe.copy()
    dataframe["line"] = dataframe["line"].str.lower()
    dataframe["line"] = dataframe["line"].str.replace(",", "").str.replace(".", "")
    return dataframe


def count_words(dataframe):
    """Word count"""

    dataframe = dataframe.copy()
    dataframe["line"] = dataframe["line"].str.split()
    dataframe = dataframe.explode("line")
    dataframe = dataframe.groupby("line").size().reset_index(name="count")
    return dataframe


def save_output(dataframe, output_filename):
    """Save output to a file."""
    dataframe.to_csv(output_filename, sep="\t", index=False, header=False)


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Job"""
    dataframe = load_input(input_directory)
    dataframe = clean_text(dataframe)
    dataframe = count_words(dataframe)
    save_output(dataframe, output_filename)


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
