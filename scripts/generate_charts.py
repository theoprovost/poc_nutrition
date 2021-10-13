import pandas as pd
import plotly
import plotly.express as px
from pathlib import Path


def genMulti(df, mode='w'):
    '''Function that plot (if mode=s or ws), and returns
        a list of :
        - plot name
        - plot HTML div w/ JS script

    Mode :
        'w' : writes
        's' : show
        'ws' : write and show

    NB: mode other than w are meant to be used in a jupyter env
    '''
    fig = px.scatter_matrix(df, width=1200, height=1100)
    fig.update_layout(
        title="Multivariate plot of selected labels.",
        font=dict(
            size=10
        )
    )
    div = [[fig['layout']['title']['text'], plotly.offline.plot(
        fig, include_plotlyjs=False, output_type='div')]]
    if (mode == 'w'):
        return div
    elif (mode == 's'):
        fig.show()
        return False
    elif (mode == 'ws'):
        fig.show()
        return div
    else:
        return False


def genUni(df, mode='w'):
    '''Function that plot (if mode=s or ws), and returns
        a list of list of :
        - plot name
        - plot HTML div w/ JS script

     Mode :
        'w' : writes
        's' : show
        'ws' : write and show

    NB: mode other than w are meant to be used in a jupyter env
    '''
    divs = []
    for x in df.columns:
        fig = px.histogram(df[[x]], histnorm='percent')
        fig.layout.showlegend = False
        fig.update_layout(
            title=f'Univariate histogram of {x}:',
            font=dict(
                size=10
            )
        )
        divs.append([fig['layout']['title']['text'],
                     plotly.offline.plot(fig, include_plotlyjs=False, output_type='div')])

    if (mode == 'w'):
        return divs
    elif (mode == 's'):
        fig.show()
        return False
    elif (mode == 'ws'):
        fig.show()
        return divs
    else:
        return False


def main(df, folder_path, mode='w'):
    # Generate the plots
    div_uni = genUni(df, mode)
    div_multi = genMulti(df, mode)

    divs = div_uni + div_multi

    # Empty the folder
    [f.unlink() for f in Path(folder_path).glob("*") if f.is_file()]

    # Create a file for each plot with it's name as file name (+ ejs extension : for backend purposes)
    for x in divs:
        file_name = x[0].lower().replace('.', '').replace(
            ':', '').rstrip().replace(' ', '_')
        f = open(f'{folder_path}{file_name}.ejs', 'w')
        f.write(x[1])
        f.close()

    print(f'Plots generated in : {folder_path}')


#############################################
#        INIT GENERATE CHARTS BELOW
#############################################
# Gets the corresponding DF, select some defined columns and reduce the df on those
csv_path = '../data/en.openfoodfacts.org.products_processed.csv'
df = pd.read_csv(csv_path)
targeted_columns = ['fat_100g', 'saturated-fat_100g', 'carbohydrates_100g',
                    'sugars_100g', 'proteins_100g', 'salt_100g', 'energy-kcal_100g', 'energy_100g']
df = df[targeted_columns]
folder_path = '../app/frontend/views/partials/charts/'

# Init the main function
main(df, folder_path)
#############################################
