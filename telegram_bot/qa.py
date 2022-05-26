import deeppavlov
from deeppavlov import configs
from deeppavlov.core.commands.infer import build_model
import tensorflow as tf
from database.test_scrapping import get_news
from perephrase import paraphrase

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


model_ru = build_model(configs.squad.squad_ru_rubert, download=False)
struct = get_news()
text = [struct[key][1] for i, key in enumerate(struct)][4]
print(text)
text = 'На портале «Объясняем.рф» в разделе «Меры поддержки» собрана информация о мерах, принятых Правительством страны для поддержки населения и экономики в условиях санкций. Особенность раздела — навигатор для поиска подходящих мер. Новый раздел поможет сориентироваться в мерах поддержки: найти актуальные, изучить их суть и узнать способы получения. В карточках мер содержится описание, срок действия и дополнительная информация, в том числе условия получения поддержки, ссылки на полезные ресурсы и нормативные документы. Для удобства пользователей в разделе есть навигатор в виде анкеты. Перейти туда можно, нажав на кнопку «Пройти опрос», а ответив на несколько вопросов, — получить список мер, которые подходят под заданные вами параметры.'
question = 'Какая информация соержися в разделе "Мои документы" ?'
question = 'Как перейти в навигатор ?'
ans = model_ru([text], [question])
txt = ans[0][0]
print(txt)
print(paraphrase(txt, gram=10, num_beams=10, do_sample=False))
# , text[ans[1][0] - 1:ans[1][0] + 1000], sep='\n')
