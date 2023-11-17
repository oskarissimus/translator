def format_log(input, log_type):
    space_padded_log_type = f" {log_type} "
    formatted_log = f"{space_padded_log_type.center(90, '=')}\n{input}\n{'=' * 90}\n\n"
    return formatted_log
