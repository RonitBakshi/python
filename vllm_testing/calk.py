
def calculate_average_lengths(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        paragraphs = file.read().split('\n\n')  # Split paragraphs by empty lines

        # Calculate average length in characters
        total_characters = sum(len(paragraph) for paragraph in paragraphs)
        average_characters = total_characters / len(paragraphs) if paragraphs else 0

        # Calculate average length in words
        total_words = sum(len(paragraph.split()) for paragraph in paragraphs)
        average_words = total_words / len(paragraphs) if paragraphs else 0

        return average_characters, average_words

# Example usage:
file_path = '/home/tisuper/Desktop/python/vllm_testing/char4.txt'
average_characters, average_words = calculate_average_lengths(file_path)
print(f"Average length of paragraphs in characters: {average_characters}")
print(f"Average length of paragraphs in words: {average_words}")
