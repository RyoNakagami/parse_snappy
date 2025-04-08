"""
Snappy、Gzip、Zstd、LZO、LZ4  Parquet 圧縮  Parquet → CSV converter
"""

import sys
import argparse
import polars as pl
import json
import pickle
from pathlib import Path

# ---------- polars dtype mapping for simple types ----------
type_map = {
    "Int8": pl.Int8,
    "Int16": pl.Int16,
    "Int32": pl.Int32,
    "Int64": pl.Int64,
    "Int128": pl.Int128,
    "UInt8": pl.UInt8,
    "UInt16": pl.UInt16,
    "UInt32": pl.UInt32,
    "UInt64": pl.UInt64,
    "Float32": pl.Float32,
    "Float64": pl.Float64,
    "Decimal": pl.Decimal,
    "Utf8": pl.Utf8,
    "String": pl.Utf8,
    "Categorical": pl.Categorical,
    "Boolean": pl.Boolean,
    "Date": pl.Date,
    "Datetime": pl.Datetime,
    "Time": pl.Time,
    "Duration": pl.Duration,
    "Binary": pl.Binary,
    "Null": pl.Null,
    "Object": pl.Object,
}


# ---------- schema loading ----------
def load_schema(schema_path: str):
    path = Path(schema_path)
    if not path.exists():
        print(f"[Error] Schema file not found: {schema_path}", file=sys.stderr)
        sys.exit(1)

    if path.suffix == ".pkl":
        with open(schema_path, "rb") as f:
            schema = pickle.load(f)
    elif path.suffix == ".json":
        with open(schema_path, "r") as f:
            schema = json.load(f)
    else:
        print(f"[Error] Unsupported schema format: {path.suffix}", file=sys.stderr)
        sys.exit(1)

    # Convert to polars dtypes
    schema_pl = {}
    for col, dtype in schema.items():
        if dtype not in type_map:
            print(f"[Warning] Unsupported dtype '{dtype}' for column '{col}', skipping")
            continue
        schema_pl[col] = type_map[dtype]

    return schema_pl if schema_pl else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file path")
    parser.add_argument(
        "--output", default=None, help="Output file (default: stdout for CSV/JSON)"
    )
    parser.add_argument(
        "--sep", default=",", help="CSV separator (ignored for JSON/Parquet)"
    )
    parser.add_argument(
        "--threads", type=int, default=None, help="Number of CPU threads"
    )
    parser.add_argument(
        "--input-format",
        choices=["parquet", "csv"],
        default="parquet",
        help="Input file format (default: parquet)",
    )
    parser.add_argument(
        "--output-format",
        choices=["csv", "json", "parquet"],
        default="csv",
        help="Output file format (default: csv)",
    )
    parser.add_argument(
        "--schema", default=None, help="Schema file (.json or .pkl) for simple types"
    )
    args = parser.parse_args()

    if args.threads is not None:
        pl.Config.set_max_threads(args.threads)

    schema = load_schema(args.schema) if args.schema else None

    # Load input data
    if args.input_format == "parquet":
        df_lazy = pl.scan_parquet(args.input)
    elif args.input_format == "csv":
        if schema:
            df_lazy = pl.scan_csv(args.input, sep=args.sep, dtypes=schema)
        else:
            df_lazy = pl.scan_csv(args.input, sep=args.sep)
    else:
        print(f"[Error] Unsupported input format: {args.input_format}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.output_format == "csv":
            if args.output:
                df_lazy.collect(engine="streaming").write_csv(
                    args.output, separator=args.sep
                )
            else:
                df_lazy.collect(engine="streaming").write_csv(
                    sys.stdout.buffer, separator=args.sep
                )

        elif args.output_format == "json":
            if args.output:
                df_lazy.collect(engine="streaming").write_json(args.output)
            else:
                df_lazy.collect(engine="streaming").write_json(sys.stdout.buffer)

        elif args.output_format == "parquet":
            if args.output:
                df_lazy.collect(engine="streaming").write_parquet(
                    args.output, compression="snappy"
                )
            else:
                print(
                    "[Error] Parquet output requires --output file path",
                    file=sys.stderr,
                )
                sys.exit(1)

    except KeyboardInterrupt:
        print("\nInterrupted (Ctrl+C)", file=sys.stderr)
        sys.exit(130)
    except (BrokenPipeError, OSError):
        sys.exit(0)
    except Exception as e:
        print(f"[Error] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
