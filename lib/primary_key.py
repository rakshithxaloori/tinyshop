import shortuuid


def get_primary_key(prefix: str):
    return lambda: "{prefix}_{uuid_hash}".format(
        prefix=prefix, uuid_hash=shortuuid.uuid()
    )
