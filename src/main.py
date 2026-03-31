from textnode import TextNode, TextType
# hello world
print("Hello, World!")

def main():
    def create_text_node(text, text_type, url):
        return TextNode(text, text_type, url)
    
    text_node1 = create_text_node("Some anchor text", TextType.LINK, "https://example.com")     
    print(text_node1)
    
if __name__ == "__main__":
    main()