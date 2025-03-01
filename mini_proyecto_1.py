import pandas as pd
import random

# Define operations and their corresponding lambda functions
operations = {
    'SUM': lambda a, b: a + b,
    'SUB': lambda a, b: a - b,
    'MUL': lambda a, b: a * b,
    'DIV': lambda a, b: a / b if b != 0 else "Error: Division by zero",
    'POW': lambda a, b: a ** b  # limit exponent to avoid very large numbers
}

# Generate data
data = []
for _ in range(1000):
    operation = random.choice(list(operations.keys()))
    operand_1 = random.randint(1, 1000)
    operand_2 = random.randint(1, 1000)
    
    # Ensure the exponent is not too large for POW operation
    if operation == 'POW' and operand_2 > 10:
        operand_2 = random.randint(1, 10)
    
    # Calculate the correct result using the corresponding lambda function
    correct_result = operations[operation](operand_1, operand_2)
    
    # Append the data with the operation, operands, and correct result
    data.append([operation, operand_1, operand_2, correct_result])

# Create DataFrame
df = pd.DataFrame(data, columns=['operation', 'operand_1', 'operand_2', 'correct_result'])

# Save to CSV
csv_path = './data/math_operations.csv'
df.to_csv(csv_path, index=False)

print(f"CSV file saved at {csv_path}")