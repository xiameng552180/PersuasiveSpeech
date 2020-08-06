import language_check

tool = language_check.LanguageTool('en-US')


def find_sentence_errors(texts):
    matches = tool.check(texts)
    # errors
    errors_num = len(matches)
    # correct errors
    correct_texts = language_check.correct(texts, matches)
    
    # print(matches)
    detailed = []
    for m in matches:
        detailed.append({
            "category": m.category,
            "contextoffset": m.contextoffset,
            "errorlength": m.errorlength,
            "message": m.msg,
            "replacements":m.replacements,
        })
        # print(m.contextoffset, m.errorlength, m.category ,m.msg, m.replacements, m.locqualityissuetype)
    
    return [errors_num, correct_texts, detailed]

grammar_check = find_sentence_errors('But if a guy hard, he blown his chance')
print(grammar_check)