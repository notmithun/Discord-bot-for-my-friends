import json
def check(id) -> bool:
    """
    Checks if the given user id exists in the money.json file.

    Parameters
    ----------
    id : int
        The user id to check.

    Returns
    -------
    bool
        True if the user id exists in the JSON file, False otherwise.
    """
    with open("money.json", "r") as f:
        d = json.load(f)
        try:
            t = d[str(id)]
            return True
        except KeyError:
            return False
        except IndexError:
            return False