import json


def get_params(argv):
    if len(argv) != 2:
        raise ReferenceError("Usage: st_cli [FILE_PATH]")
        # sys.stderr.write("Usage: st_cli [FILE_PATH]\n")
        # exit(1)

    try:
        with open(argv[1]) as f:
            params = json.load(f)
    except Exception:
        raise ReferenceError("Error: ignore params file, " + argv[1])
        # sys.stderr.write("Error: ignore params file, " + argv[1] + "\n")
        # exit(1)

    return params


def create_signed_transaction(argv):
    params = get_params(argv)
    print(params)
