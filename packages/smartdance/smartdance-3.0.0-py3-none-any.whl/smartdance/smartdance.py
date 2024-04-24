import re

def dance(template_string: str, local_dict: dict, hyperparameters: dict = None) -> str:
    # Regular expression to find function calls or variables in {{}}
    pattern = r"\{\{(.*?)\}\}"

    # Find all matches in the template string
    matches = re.findall(pattern, template_string)

    for match in matches:
        result = ""  # Initialize result to an empty string for each match
        try:
            # Check if it's a function call
            if '(' in match and ')' in match:
                function_name, parameters = match.split('(')
                parameters = parameters.rstrip(')')
                # Execute the function with the parameters and get the result
                result = eval(f"{function_name}({parameters})", globals(), local_dict)
            else:
                # It's a variable
                variable_name = match
                # Get the value of the variable
                if hyperparameters and variable_name in hyperparameters:
                    result = hyperparameters[variable_name]
                else:
                    result = eval(variable_name, globals(), local_dict)
        except Exception as e:
            # If there's an error, result is already an empty string
            # Optionally, log the error or handle it as needed
            pass

        # Replace the function call or variable in the template string with the result
        template_string = template_string.replace(f"{{{{{match}}}}}", str(result))

    return template_string


def name() -> str:
    return "Marcelo"

if __name__ == "__main__":
    print(dance("My name is {{name()}}, from {{country}}!", locals(), {'country': 'Chile'}))
