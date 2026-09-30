import pandas as pd


CSV_FILE = "books.csv"


def main():
    df = pd.read_csv(CSV_FILE)

  

    print(df.head())
    print("\nShape:", df.shape)
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values:")
    print(df.isna().sum())
    print("\nIn stock:")
    print(df["in_stock"].value_counts())


if __name__ == "__main__":
    main()
    
    
    
    # Output
    
#                                    title  price  ...  in_stock                                                url
# 0                   A Light in the Attic  51.77  ...      True  https://books.toscrape.com/a-light-in-the-atti...
# 1                     Tipping the Velvet  53.74  ...      True  https://books.toscrape.com/tipping-the-velvet_...
# 2                             Soumission  50.10  ...      True  https://books.toscrape.com/soumission_998/inde...
# 3                          Sharp Objects  47.82  ...      True  https://books.toscrape.com/sharp-objects_997/i...
# 4  Sapiens: A Brief History of Humankind  54.23  ...      True  https://books.toscrape.com/sapiens-a-brief-his...

# [5 rows x 5 columns]

# Shape: (100, 5)

# Data types:
# title        object
# price       float64
# rating        int64
# in_stock       bool
# url          object
# dtype: object

# Missing values:
# title       0
# price       0
# rating      0
# in_stock    0
# url         0
# dtype: int64

# In stock:
# in_stock
# True    100
# Name: count, dtype: int64