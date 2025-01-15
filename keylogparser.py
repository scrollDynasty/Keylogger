def convert_layout(char):
    # Complete dictionary mapping Russian keyboard layout to English
    layout_map = {
        # Upper case (with Shift)
        'Й': 'Q', 'Ц': 'W', 'У': 'E', 'К': 'R', 'Е': 'T', 'Н': 'Y', 'Г': 'U',
        'Ш': 'I', 'Щ': 'O', 'З': 'P', 'Х': '[', 'Ъ': ']', 'Ф': 'A', 'Ы': 'S',
        'В': 'D', 'А': 'F', 'П': 'G', 'Р': 'H', 'О': 'J', 'Л': 'K', 'Д': 'L',
        'Ж': ';', 'Э': "'", 'Я': 'Z', 'Ч': 'X', 'С': 'C', 'М': 'V', 'И': 'B',
        'Т': 'N', 'Ь': 'M', 'Б': ',', 'Ю': '.', 'Ё': '~',

        # Lower case (without Shift)
        'й': 'q', 'ц': 'w', 'у': 'e', 'к': 'r', 'е': 't', 'н': 'y', 'г': 'u',
        'ш': 'i', 'щ': 'o', 'з': 'p', 'х': '[', 'ъ': ']', 'ф': 'a', 'ы': 's',
        'в': 'd', 'а': 'f', 'п': 'g', 'р': 'h', 'о': 'j', 'л': 'k', 'д': 'l',
        'ж': ';', 'э': "'", 'я': 'z', 'ч': 'x', 'с': 'c', 'м': 'v', 'и': 'b',
        'т': 'n', 'ь': 'm', 'б': ',', 'ю': '.', 'ё': '`',

        # Numbers and symbols (upper case)
        '!': '!', '@': '@', '№': '#', '$': '$', '%': '%', '^': '^', '&': '&',
        '*': '*', '(': '(', ')': ')', '_': '_', '+': '+',

        # Numbers and symbols (lower case)
        '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
        '8': '8', '9': '9', '0': '0', '-': '-', '=': '=', '\\': '\\', '/': '/',
        '.': '.', ',': ',', ' ': ' ',

        # Additional symbols
        '?': '?', ';': ';', ':': ':', '"': '"', "'": "'", '[': '[', ']': ']',
        '{': '{', '}': '}', '<': '<', '>': '>'
    }
    return layout_map.get(char, char)  # Return converted character or original if not in dictionary

def parse_keylog(raw_text):
    temp_buffer = []  # Buffer for storing characters
    skip_next = False  # Flag to skip next character after ctrl
    
    # Split input text into tokens
    tokens = []
    current_token = ""
    in_key = False
    
    # Parse text into tokens
    for char in raw_text:
        if char == '<':
            if current_token:
                tokens.append(current_token)
            current_token = '<'
            in_key = True
        elif char == '>' and in_key:
            current_token += '>'
            tokens.append(current_token)
            current_token = ""
            in_key = False
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)

    # Process tokens
    i = 0
    while i < len(tokens):
        token = tokens[i].strip()
        
        # Skip token if skip_next flag is set
        if skip_next:
            skip_next = False
            i += 1
            continue
            
        # Handle special keys
        if token.startswith('<Key.'):
            clean_token = token.strip('<>').lower()
            
            if 'ctrl' in clean_token:
                skip_next = True  # Skip next character after ctrl
            elif 'backspace' in clean_token:
                if temp_buffer:
                    temp_buffer.pop()  # Remove last character
            elif 'space' in clean_token:
                temp_buffer.append(' ')
            elif 'enter' in clean_token:
                temp_buffer.append('\n')
            elif 'shift' in clean_token or 'cmd' in clean_token:
                pass  # Ignore shift and cmd
        else:
            # Handle regular characters
            if token and not skip_next:
                # Convert each character separately
                for char in token:
                    converted_char = convert_layout(char)
                    temp_buffer.append(converted_char)
        i += 1
    
    # Combine final text
    parsed_text = ''.join(temp_buffer)
    return ' '.join(parsed_text.split())

def main():
    try:
        print("Enter keyboard log (press Enter twice to finish input):")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        
        raw_keylog = '\n'.join(lines)
        
        # Parse the text
        result = parse_keylog(raw_keylog)
        
        print("\nDecoded text:")
        print(result if result else "[No text received]")
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()