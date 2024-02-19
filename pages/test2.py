def find_matching_paragraphs(data, phrases):
    paragraphs = data.split("\n\n")  # Assuming paragraphs are separated by two newlines
    matching_paragraphs = []
    for phrase in phrases:
        for paragraph in paragraphs:
            if phrase in paragraph:
                matching_paragraphs.append(paragraph.strip())
                break  # Break once a matching paragraph is found for the current phrase
    return matching_paragraphs if matching_paragraphs else ["No matching paragraphs found"]

# Dummy multiple-paragraph data
dummy_data = """
Paragraph 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Phasellus non dolor eu neque dictum fringilla. Vivamus vel commodo massa. 
Donec sit amet ligula non justo blandit pretium. 

Paragraph 2: Nullam vehicula, arcu et convallis sollicitudin, dui augue congue magna, 
at sollicitudin risus tortor nec dui. 

Paragraph 3: Fusce eget felis sit amet augue consequat suscipit. Ut at urna vel metus 
condimentum tincidunt. Proin et ultricies justo. 

Paragraph 4: Aenean varius augue velit, nec tristique tortor volutpat nec. 
Sed et leo ut felis posuere lobortis. Vestibulum eget diam vitae nisi sollicitudin 
fringilla. Vestibulum in purus risus. 
"""

phrases_to_search = ["sit amet", "consectetur", "felis sit amet"]  # Phrases to search for

matching_paragraphs = find_matching_paragraphs(dummy_data, phrases_to_search)

print("Matching Paragraphs:")
for idx, paragraph in enumerate(matching_paragraphs, 1):
    print(f"Match {idx}:")
    print(paragraph)
    print()