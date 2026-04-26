import re

def calculate_gradient(equation):
    # Normalize the equation
    equation = equation.replace(" ", "").lower()

    # Handle equations that don't contain '=' sign
    if "=" not in equation:
        return None

    # Split the equation into left and right sides
    left_side, right_side = equation.split('=', 1)

    # Initialize coefficients
    coeff_y = 0.0
    coeff_x = 0.0
    constant = 0.0

    # Function to parse a side of the equation
    def parse_side(side, is_left_side):
        local_coeff_x = 0.0
        local_coeff_y = 0.0
        local_constant = 0.0
        
        # Use a regex to find terms (e.g., -3x, +2y, 5, -1.5)
        # It looks for an optional sign, then an optional number (decimal included), then optional 'x' or 'y'
        terms = re.findall(r'([+-]?\d*\.?\d*[xy]?)', side)
        
        for term in terms:
            if not term: # Skip empty terms from regex
                continue

            sign = 1.0
            if term.startswith('-'):
                sign = -1.0
                term = term[1:]
            elif term.startswith('+'):
                term = term[1:]

            if 'x' in term:
                num_str = term.replace('x', '')
                if num_str == '': # case 'x'
                    local_coeff_x += sign * 1.0
                else:
                    local_coeff_x += sign * float(num_str)
            elif 'y' in term:
                num_str = term.replace('y', '')
                if num_str == '': # case 'y'
                    local_coeff_y += sign * 1.0
                else:
                    local_coeff_y += sign * float(num_str)
            else:
                # It's a constant term
                if term != '': # Ensure it's not an empty string
                    local_constant += sign * float(term)
        return local_coeff_x, local_coeff_y, local_constant

    # Parse both sides
    left_coeff_x, left_coeff_y, left_constant = parse_side(left_side, True)
    right_coeff_x, right_coeff_y, right_constant = parse_side(right_side, False)

    # Combine terms to get into the form Ay = Bx + C
    total_coeff_y = left_coeff_y - right_coeff_y
    total_coeff_x = right_coeff_x - left_coeff_x
    total_constant = right_constant - left_constant

    # If there's no 'y' term, it's not a linear equation in y = mx + c form (e.g., x = 5)
    if total_coeff_y == 0:
        return None
    
    # If there's no 'x' term, it's a horizontal line (y = constant), gradient is 0
    if total_coeff_x == 0:
        return 0

    # Calculate the gradient (m = B/A)
    gradient = total_coeff_x / total_coeff_y
    return gradient

if __name__ == "__main__":
    test_cases = [
        "y = 3x + 7",
        "y = -x + 2",
        "y = 5",
        "y = x",
        "y = -x",
        "y = 0.5x - 1",
        "y = -2.3x + 4",
        "y = 7 + 3x",
        "y = 2 - x",
        "y = -4x",
        "y = x - 0",
        "y = -1.0x + 0",
        "y = 0",
        "x + y = 5",  # Should result in -1
        "2y = 4x + 6", # Should result in 2
        "-y = -2x + 1", # Should result in 2
        "y + x = 0", # Should result in -1
        "3x = y + 2", # Should result in 3
        "y = 0x + 5" # Should result in 0

    ]

    for equation_input in test_cases:
        gradient = calculate_gradient(equation_input)
        if gradient is not None:
            print(f"The gradient of {equation_input} is: {gradient}")
        else:
            print(f"Could not determine the gradient for {equation_input}. Please enter a valid linear equation.")
