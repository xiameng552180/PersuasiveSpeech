import language_check

tool = language_check.LanguageTool('en-US')


def find_sentence_errors(texts):
    matches = tool.check(texts)
    # errors
    errors_num = len(matches)
    # correct errors
    correct_texts = language_check.correct(texts, matches)

    return [errors_num, correct_texts, matches]


grammar_check = find_sentence_errors('But if a guy hard, he blown his chance')
print(grammar_check)