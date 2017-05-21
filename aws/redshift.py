import sys
import os


def parse_odbc(url):
    """
    Parse Redshift ODBC URL
    -----------------------

    :param url: Fully Qualified ODBC URL
    :type  url: str
    :return parsed: ODBC fields parsed into respective fields.
    :rtype  parsed: dict

    .. example::

        Driver={Amazon Redshift (x64)};
        Server=server_name.xxxxxx.us-east-1.redshift.amazonaws.com;
        Database=mydb;
        UID=myuser;
    """
    secrets = 'Database', 'Port', 'Server', 'UID'
    parsed = dict([
        dr.strip().split('=') for dr in url.strip().split(';')
        if any(secret in dr for secret in secrets)
    ])
    # Ensure all fields were serialized
    assert set(parsed) == set(secrets)

    return parsed


def gen_redshift_query():

    # `raw_input` is input in Python 3
    if sys.version_info.major == 2:
        input = raw_input

    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID") or eval(input("AWS_ACCESS_KEY: "))
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY") or eval(input("AWS_SECRET_ACCESS_KEY"))

    s3_bucket = eval(input("S3 Output Bucket: "))
    output_table = eval(input("Output Redshift Table: "))

    upload = """
        COPY           \'cc.{output_table}\'
        FROM           \'{s3_bucket}\'
        CREDENTIALS    \'aws_access_key_id={aws_access_key_id};aws_secret_access_key={aws_secret_access_key};\'
        DELIMITER      \'\\t\'
        REGION         \'us-east-1\'
        ACCEPTINVCHARS  AS \'^\'
        NULL            AS \'\\000\'
        TRUNCATECOLUMNS REMOVEQUOTES;
        """.format(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            s3_bucket=s3_bucket,
            output_table=output_table,
    )
    return upload
