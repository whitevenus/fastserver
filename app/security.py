import re


def validate_sql(sql: str) -> bool:
    """检查是否为合法的DML语句"""
    clean_sql = re.sub(r"[\s;]", "", sql, flags=re.IGNORECASE)
    return re.match(r"^(SELECT|INSERT|UPDATE|DELETE)", clean_sql, re.I) is not None
