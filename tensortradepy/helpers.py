default_return = {
    "txs": {
        "lastValidBlockHeight": None,
        "tx": None,
        "txV0": None
    }
}

def build_tensor_query(
    name,
    sub_name,
    parameters,
    return_format=default_return
):
    param_string = [
        f"${param_name}: {param_type}!"
        for (param_name, param_type) in parameters
    ]
    params = "\n".join(param_string)
    sub_param_string = [
        f"{param_name}: ${param_name}"
        for (param_name, _) in parameters
    ]
    sub_params = ", ".join(sub_param_string)
    result_fields = []
    for variable, value in return_format.items():
        if value is None:
            result_fields.append(variable)
        else:
            result_fields.append(variable)
            result_fields.append("{")
            for subvariable, subvalue in value.items():
                if subvalue is None:
                    result_fields.append(subvariable)
            result_fields.append("}")
    result_variables = "\n".join(result_fields)
    return """query %s(
  %s
) {
  %s(%s) {
    %s
  }
}
""" % (name, params, sub_name, sub_params, result_variables)
