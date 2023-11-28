'''
Final Project
Arjoneel Dhar
Professor: Rich Thompson
Section Leader: Olivia Fernflores
11/27/2023
'''

'''
The following file has a 
'''


from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

def get_df():
    soup = BeautifulSoup(open('murder_scrape.html'))
    tag = soup.find('div', class_='post-body entry-content')
    url = tag.span.next_sibling.next_sibling.next_sibling.find('a').next_sibling.next_sibling['href']
    df = pd.read_csv(url)
    return df

def prep_sers_and_dfs(df):
    national_mrd = df.loc[(df['YEAR'] == 2021)].sort_values("MRD", ascending = False).head(25).reset_index()
    national_ser = pd.Series(data=national_mrd['MRD'].values, index=national_mrd['Name'])
    baltimore = df.loc[(df['County'] == 'Baltimore city, MD') & (df['Name']== 'BALTIMORE') & (df['Agency']== 'Baltimore')].sort_values('YEAR').reset_index()
    baltimore_df = pd.Series(data=baltimore['MRD'].values, index=baltimore['YEAR'])
    arizona = df.loc[(df['State'] == 'Arizona') & (df['YEAR'] == 2021)].reset_index()
    arizona_ser = pd.Series(data=arizona['MRD'].values, index=arizona['Name'])
    return baltimore_df, national_ser, arizona_ser

def display_bar(data, title='insert title', xlab='insert x axis label', ylab='insert y axis label'):
    fig = plt.figure(facecolor='#aaeeee')
    ax = fig.add_subplot(facecolor='#ccffff')
    data.plot.bar(
        ax=ax,
        width=0.5,
        rot=0,
    )
    # plt.tick_params(
    #     axis='x',          # changes apply to the x-axis
    #     which='both',      # both major and minor ticks are affected
    #     bottom=False,      # ticks along the bottom edge are off
    #     top=False,         # ticks along the top edge are off
    #     labelbottom=False # labels along the bottom edge are off
    # )
    ax.set_title(title, fontsize=18)
    ax.set_xlabel(xlab, fontsize=14)
    ax.set_ylabel(ylab, fontsize=14)
    plt.xticks(rotation=90)
    plt.tick_params(axis='x', which='major', labelsize=6)
    plt.show()

def get_ols_parameters(data):
    """Get the ols parameters from a series"""
    x = data.index.values
    X = sm.add_constant(x)
    model = sm.OLS(data, X)
    results = model.fit()
    return results.params['x1'], results.params['const'], results.rsquared, results.pvalues['x1']

def make_scatterplot(data, m, b):
    """Make a very pretty figure with the data from get_data"""
    fig = plt.figure(facecolor='#aaeeee')
    ax = fig.add_subplot(facecolor='#ccffff')
    data.plot(style='m.', label='Data Point of Murders in said Year')
    plt.plot(data.index, m * data.index + b, color='tab:red', label=f"{m:.4f}x + {b:.4f}")
    plt.legend(loc='lower right')
    ax.set_title('Number of Murders Per Year in Baltimore City', fontsize=18)
    ax.set_xlabel('Years (10 Years Intervals)', fontsize=14)
    ax.set_ylabel('Number of Murders', fontsize=14)
    plt.tight_layout()
    plt.show()

def main():
    baltimore_df, national_ser, arizona_ser = prep_sers_and_dfs(get_df())
    m, b, *_ = get_ols_parameters(baltimore_df)
    make_scatterplot(baltimore_df, m, b)
    display_bar(national_ser,title='Top 25 Juristictions with the Highest Murder Rates (circa 2021)',xlab='City',ylab='Number of Murders')
    display_bar(arizona_ser,title='Number of Arizona Murders in the Year 2021',xlab='Police Jurisdiction',ylab='Number of Murders')

# That Other Stuff:

if __name__ == "__main__":
    main()
    