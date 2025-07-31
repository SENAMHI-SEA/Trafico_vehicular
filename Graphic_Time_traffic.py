# Importar librerias

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import seaborn as sns
from datetime import timedelta
import os

#import matplotlib.dates as mdates

# Configuración global
sns.set(style='whitegrid')
plt.rcParams["figure.autolayout"] = True

# --- Parámetros ajustables ---
EXCEL_PATH = r'C:\Users\usuario1\Documents\SEA\trafico\tiempo_demora.xlsx'
TIME_COLUMN = 'Tiempo de demora'
DATE_COLUMN = 'date'
RUTAS = ["Avenida Sanchez Cerro", "Avenida Progreso", "Avenida Guardia Civil"]

# --- Funciones ---
def load_and_clean_data(path):
    df = pd.read_excel(path)

    df[TIME_COLUMN] = df[TIME_COLUMN].str.replace('min', '', regex=False).astype(float)

    df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors='coerce')

    latest_date = df[DATE_COLUMN].max().date()
    recent_days = [latest_date - timedelta(days=i) for i in range(3)]
    df['only_date'] = df[DATE_COLUMN].dt.date
    df = df[df['only_date'].isin(recent_days)].copy()
    df.drop(columns='only_date', inplace=True)

    df['hour'] = df[DATE_COLUMN].dt.hour
    df['day'] = df[DATE_COLUMN].dt.date
    

    return df

#df['datetime'] = df[DATE_COLUMN].dt.strftime("%Y-%m-%d %H")
def aggregate_and_pivot(df):
    df_avg = (
        df.groupby(['Zona', 'day', 'hour'])[TIME_COLUMN]
        .mean()
        .reset_index(name='avg_delay')
    )
    df_pivot = df_avg.pivot_table(index=['day', 'hour'], columns='Zona', 
                                  values='avg_delay').reset_index()
    df_pivot = df_pivot.sort_values(by=['day', 'hour'])
    df_pivot['date'] = pd.to_datetime(df_pivot['day'].astype(str) + ' ' + 
                                      df_pivot['hour'].astype(str) + ':00:00')
    return df_pivot


def get_midnights(df):
    start_date = df['date'].min().floor('D')
    end_date = df['date'].max().ceil('D')
    return pd.date_range(start=start_date, end=end_date, freq='D')


def plot_multiple_stations(df_pivot, midnights, routes, save_path=None, ymin=None, ymax=None):
    n = len(routes)
    cols = 1
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, route in enumerate(routes):
        ax = axes[i]
        if route not in df_pivot.columns:
            print(f"[Advertencia] {route} no está en los datos.")
            ax.set_visible(False)
            continue

        sns.lineplot(x=df_pivot['date'], y=df_pivot[route], ax=ax, marker='o', color='blue')
        ax.set_title(route, fontsize=12, weight='bold')
        ax.set_ylabel("Tiempo de demora (min)", fontsize=12, weight='bold')
        ax.set_xlabel("Fecha y hora", fontsize=12, weight='bold')
        ax.xaxis.set_major_formatter(DateFormatter('%d-%b %H:%M'))
        ax.tick_params(axis='x', labelrotation=45)
        ax.grid(True)

        if ymin is not None and ymax is not None:
            plt.ylim(ymin, ymax)

        for m in midnights:
            ax.axvline(x=m, color='red', linestyle='dashed', linewidth=0.8)

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    if save_path:
        plt.savefig(save_path, format='jpg', dpi=300)
        print(f"[Info] Panel guardado en: {save_path}")
    plt.tight_layout()
    plt.show()


def main_panel():
    nombre_archivo = "panel_trafico.jpg"
    base_dir = os.path.dirname(EXCEL_PATH)
    save_path = os.path.join(base_dir, nombre_archivo)

    if not os.path.exists(EXCEL_PATH):
        print(f"[Error] Archivo no encontrado: {EXCEL_PATH}")
        return

    df = load_and_clean_data(EXCEL_PATH)
    df_pivot = aggregate_and_pivot(df)
    midnights = get_midnights(df_pivot)

    plot_multiple_stations(df_pivot, midnights, routes=RUTAS, save_path=save_path, 
                           ymin=0, ymax=14)


if __name__ == "__main__":
    main_panel()      


# En el caso de gráfico para una ruta en específico


def plot_single_station(df_pivot, midnights, route_name, save_path=None):
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=df_pivot, x='date', y=route_name, color='blue', marker='o')

    plt.title(route_name, fontsize=16, weight='bold')
    plt.xlabel("Fecha y Hora", fontsize=16, weight='bold')
    plt.ylabel("Tiempo de demora (minutos)", fontsize=16, weight='bold')
    plt.xticks(rotation=0)
    plt.grid(True)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%b %H:%M'))

    for m in midnights:
        plt.axvline(x=m, color='red', linestyle='dashed', linewidth=0.8)

    if save_path:
        plt.savefig(save_path, format='jpg', dpi=300)
        print(f"[Info] Gráfico guardado en: {save_path}")

    plt.tight_layout()
    plt.show()


def main_individual():

    ruta = "Avenida Progreso"
    nombre_archivo = f"{ruta.replace(' ', '_').lower()}.jpg"
    base_dir = os.path.dirname(EXCEL_PATH)
    save_path = os.path.join(base_dir, nombre_archivo)

    if not os.path.exists(EXCEL_PATH):
        print(f"[Error] Archivo no encontrado: {EXCEL_PATH}")
        return

    df = load_and_clean_data(EXCEL_PATH)
    df_pivot = aggregate_and_pivot(df)
    midnights = get_midnights(df_pivot)

    if ruta not in df_pivot.columns:
        print(f"[Error] La ruta '{ruta}' no se encuentra en los datos.")
        return

    plot_single_station(df_pivot, midnights, route_name=ruta, save_path=save_path)


if __name__ == "__main__":
    main_individual()  




