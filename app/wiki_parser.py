import wikipedia


def search_wiki(point):
    wikipedia.set_lang("ru")
    answer = wikipedia.summary(point, sentences=10)
    if answer:
        return answer
    else:
        return "Вибачте, необхідно ввести конкретніші дані!"
