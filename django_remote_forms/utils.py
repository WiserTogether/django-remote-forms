from django.forms.util import ErrorList, ErrorDict


def normalize_error_dict(error_dict):
    normalized_error_dict = {}
    for error_type, error_detail in error_dict.items():
        if isinstance(error_detail, (list, tuple, ErrorList)):
            error_detail = normalize_error_list(error_detail)
        elif not isinstance(error_detail, (str, unicode)):
            error_detail = unicode(error_detail)

        normalized_error_dict[error_type] = error_detail

    return normalized_error_dict


def normalize_error_list(error_list):
    normalized_error_list = []
    if isinstance(error_list, (list, ErrorList)):
        for error_message in error_list:
            error_message = unicode(error_message)
            normalized_error_list.append(error_message)

    return normalized_error_list


def normalize_errors(error_container):
    if isinstance(error_container, (list, tuple, ErrorList)):
        return normalize_error_list(error_container)
    elif isinstance(error_container, (dict, ErrorDict)):
        return normalize_error_dict(error_container)
    else:
        return error_container
