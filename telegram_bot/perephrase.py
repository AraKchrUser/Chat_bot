import torch
from transformers import FSMTModel, FSMTTokenizer, FSMTForConditionalGeneration


def paraphrase(text, gram=4, num_beams=5, **kwargs):
    """ Generate a paraphrase using back translation.
    Parameter `gram` denotes size of token n-grams of the original sentence that cannot appear in the paraphrase.
    """
    tokenizer = FSMTTokenizer.from_pretrained("facebook/wmt19-en-ru")
    model = FSMTForConditionalGeneration.from_pretrained("facebook/wmt19-en-ru")
    inverse_tokenizer = FSMTTokenizer.from_pretrained("facebook/wmt19-ru-en")
    inverse_model = FSMTForConditionalGeneration.from_pretrained("facebook/wmt19-ru-en")
    # model.cuda();
    # inverse_model.cuda();
    input_ids = inverse_tokenizer.encode(text, return_tensors="pt")
    with torch.no_grad():
        outputs = inverse_model.generate(input_ids.to(inverse_model.device), num_beams=num_beams, **kwargs)
    other_lang = inverse_tokenizer.decode(outputs[0], skip_special_tokens=True)
    # print(other_lang)
    input_ids = input_ids[0, :-1].tolist()
    bad_word_ids = [input_ids[i:(i + gram)] for i in range(len(input_ids) - gram)]
    input_ids = tokenizer.encode(other_lang, return_tensors="pt")
    with torch.no_grad():
        outputs = model.generate(input_ids.to(model.device), num_beams=num_beams, bad_words_ids=bad_word_ids, **kwargs)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return decoded


if __name__ == '__main__':
    text = 'Скорее всего переговоры между Россией и Украиной не состоятся, так как украинская сторона оттягивает это'
    # Переговоры Россия-Украина вряд ли будут вестись - об этом предупреждает украинское руководство.
    # Переговоры между Россией и Украиной, скорее всего, не состоятся, поскольку украинская сторона настаивает на этом
    # Вероятнее всего, переговоры России и Украины не пройдут, поскольку украинская сторона настаивает на этом.

    text = 'Женщина-дайвер исчезла в Черном море во время научных работ на побережье Анапы.'
    # Женщина-водолаз пропала в акватории Черного моря, когда выполняла исследовательские работы у берегов Анапы.
    # В Черном море пропала женщина-дайвер, выполнявшая исследовательские работы у берегов Анапы.
    # Женщина-дайвер пропала в Черном море, когда проводила исследования у берегов Анапы.
    # Водолаз женского пола, выполнявший исследовательские работы у берегов анапской акватории, пропал без вести.

    print(paraphrase(text, gram=10, num_beams=10, do_sample=False))

