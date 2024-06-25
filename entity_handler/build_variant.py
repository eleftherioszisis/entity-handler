import pyarrow
import pyarrow.fs
import pandas as pd

def load_arrow(filepath):
    with pyarrow.fs.LocalFileSystem().open_input_file(filepath) as fd:
        df = pyarrow.RecordBatchFileReader(fd).read_pandas()
        return df


def write_arrow(df, filepath):
    table = pyarrow.Table.from_pandas(df, preserve_index=False)
    write_options = pyarrow.ipc.IpcWriteOptions()

    with pyarrow.fs.LocalFileSystem().open_output_stream(str(filepath)) as fd:
        with pyarrow.RecordBatchFileWriter(fd, table.schema, options=write_options) as writer:
            writer.write_table(table)


def write_variant_matrix(er_path, dd_path, output_path):

    er = load_arrow(er_path)
    dd = load_arrow(dd_path)

    er["variant"] = "placeholder__erdos_renyi"
    dd["variant"] = "placeholder__distance_dependent"

    columns = ["side", "source_region", "target_region", "source_mtype", "target_mtype", "variant"]

    res = pd.concat([er, dd], ignore_index=True)[columns]

    for cat in columns:
        res[cat] = res[cat].astype("category")

    write_arrow(res, output_path)


if __name__ == "__main__":


    er_path = "/gpfs/bbp.cscs.ch/data/scratch/proj134/home/pokorny/BBPP134-193/SBO_micro_ER.arrow"
    dd_path = "/gpfs/bbp.cscs.ch/data/scratch/proj134/home/pokorny/BBPP134-193/SBO_micro_DD.arrow"

    output_file = "variant_matrix.arrow"

    write_variant_matrix(er_path, dd_path, output_file)
