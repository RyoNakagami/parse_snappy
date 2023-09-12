import sys
import pandas as pd

def main(args):
    df = pd.read_parquet(args)
    df.to_csv(sys.stdout, index=False)

if __name__ == "__main__":
   main(sys.argv[1])