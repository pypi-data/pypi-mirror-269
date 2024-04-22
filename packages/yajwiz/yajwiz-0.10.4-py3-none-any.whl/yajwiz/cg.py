import yajwiz

def main():
    while True:
        text = input()
        for token_type, token_text in yajwiz.tokenize(text):
            if token_type == "PUNCT":
                print(f'"<{token_text}>"')
                print(f'\t"{token_text}" Punct')

            elif token_type == "WORD":
                print(f'"<{token_text}>"')
                for analysis in yajwiz.analyze(token_text, True, True):
                    print(f'\t"{analysis["LEMMA"]}"', "Word", *analysis["SYNTAX_INFO"]["BITS"], sep=" ")

if __name__ == "__main__":
    main()
