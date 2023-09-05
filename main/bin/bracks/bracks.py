"""
// Variables 
{{key}} // Placeholder
${key} // Declared

// Modifiers
~ {{key}} // Approximate
+ {{key}} // Concatenate
= {{key}} // Exact match 
! {{key}} // Exclude
- {{key}} // Subtract
* {{key}} // Repeat
>, <, <=, >= {{key}} // Comparisons

// Conditionals  
? {{key1}} : {{key2}} // If key1 then key2

// Keywords
ANY, ALWAYS, NEVER, WITH, AND, ONLY, NOT, UNIQUE

// Functions
between({{key1}}, {{key2}}) // Range
random({{key1}}, ...) // Random
mixed({{key1}}, ...) // Combination
contains({{key}}) // Must contain  
optimize({{key}}) // Optimize
limit({{key}}, {{value}}) // Limit

// Function Arguments
fn(-{{key}}) // Remove 
fn(*{{key}}) // Repeat
fn(?{{key1}}:{{key2}}) // Conditional

// Comments 
// This is a comment

// Includes
include({{filename}})
  
// Math
{{key1}} + {{key2}}  
{{key1}} - {{key2}}
{{key1}} * {{key2}}
{{key1}} / {{key2}}

// Nesting
{{outerKey {{innerKey}}}}

// Default values
${key=defaultValue}

// Data types  
${key=123} // Number
${flag=true} // Boolean
${text="Hello"} // String

// Object properties  
{{person.name}}  
{{person.age}}

// JSON import
import_json({{filename}})

// Looping
for {{i}} in {{array}} {
  // loop body 
}
"""
# Python Implementation Example

# Define a function to process the custom syntax
def process_custom_syntax(input_text, context={}):

  # Split input into tokens
  tokens = input_text.split()  

  # Initialize output
  output = ""

  # Loop through tokens
  for token in tokens:
    
    # Check if placeholder
    if token.startswith("{{") and token.endswith("}}"):
    
      key = token[2:-2]  
      if key in context:
        output += context[key]
      else:
        output += token
    
    else:
      output += token

    # Add space after token  
    output += " "

  # Remove trailing space    
  return output.strip()

# Example usage
custom_syntax = "This is a {{key1}} example {{key2}} with some {{key3}}."
context = {
  "key1": "custom",
  "key2": "text", 
  "key3": "placeholders"
}

result = process_custom_syntax(custom_syntax, context)
print(result)
