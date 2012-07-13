У нашей команды всю жизнь была жуткая проблема: много людей собираются участвовать, но мало людей контрибьютит, причём даже эти люди постепенно отваливаются, так что в конце остаётся один Влад по большому счёту. Это, наверное, потому, что мы пишем плохой код, который не позволяет участникам легко и непринуждённо найти место для приложения усилий и приложить их.

Одна сторона проблемы состоит в "just for fun" природе эвента. Когда я пишу код "just for fun", я не делаю всех тех вещей, которые я делаю когда пишу код по работе/для опенсорсного проекта/для себя чтобы использовать его потом долго -- я не пишу тесты, описание того как оно всё работает вообще, примеры использования, комментарии. С другой стороны, когда я с таким же "just for fun" отношением читаю так же написанный чужой код, я вовсе не горю желанием налить себе чаю и сесть разбираться в нём как если бы мне начальник сказал что вот, надо разобраться, в лучшем случае я займусь каким-нибудь другим аспектом проблемы, в плохом случае -- напишу свой несовместимый вариант, в худшем -- пойду читать Реддит в надежде что кто-нибудь другой разберётся в этом коде и напишет пример использования который я смогу скопипейстить и начать разбираться и контрибьютить (этого обычно не происходит, естественно). В результате всем становится грустно и плохо, включая авторов кода который никто почему-то не хочет использовать и улучшать.

Кроме очевидных общих слов "не делайте так, пишите понятный код с комментариями, высокоуровневым описанием, примерами использования, doctests/integration tests, иначе самим же будет неприятно когда все усилия пропадут втуне", вот небольшой список конкретных предложений по оформлению кода, которые, надеюсь, сделают его более доступным для совместной работы в суровых условиях ICFPC:

--------

### Library-oriented programming: Python is __the__ scripting language.

Мы не пишем executable scripts, мы пишем библиотеки/модули. Всю функциональность, которую предоставляет ваш код, я должен иметь возможность натуральным образом использовать из своего test.py (который я использую вместо REPL). Я никогда не должен открывать шелл и что-то вызывать оттуда.

Исключения: основной скрипт который нужно будет сабмитить, плюс если очень нужно, можно добавить к своему `awesome_module.py` `awesome_module_cli.py` (в котором не должно быть ничего кроме argparse/optparse и вызова функций из базового модуля, то же относится к основному скрипту). Алсо напоминаю, что в питоне есть например модули glob, subprocess и другие, если хочется поприменять алгоритм к куче файликов -- совершенно необязательно делать это из шелла.

Смысл этого в том, что размножение шелл-скриптов (под винду и линукс причём) мешает понять и использовать чужой код, так как он перестаёт быть самоочевидным и начинает требовать черезжопных обёрток.

--------

### Tests are good.

В случае ICFPC (как в общем и в реальной жизни ИМХО) смысл тестов не в том, чтобы доказать кому-то корректность кода, а, во-первых, в том, что они показывают пример использования кода, во-вторых, устраняют бОльшую часть боязни того, что если ты что-то поправишь в чужом коде, ты можешь его сломать _вообще весь_.

И по крайней мере на начальных этапах чрезмерного количества тестов, одержимости покрытием и т.п. не нужно (это только затруднит изменение интерфейсов, если вдруг возникнет потребность). Достаточно проверки, что хоть что-то работает.

http://docs.python.org/library/doctest.html -- посмотрите по диагонали, но не злоупотребляйте: основной смысл доктестов более в демонстрации того, как использовать код.

http://docs.python.org/library/unittest.html -- но использовать скорее в качестве integration tests, которые тестируют много функциональности сразу (но не помогают найти где что-то сломалось, если оно сломалось, в отличие от традиционных unit tests).

Раз уж у нас все модули -- библиотеки, то везде должно быть:

    if __name__ == '__main__':
        import doctest, unittest
        doctest.testmod()
        unittest.main()

--------

### Flat passive imperative code is good, data structures are the best interface.

Императивный не в смысле "не функциональный" или "не ООП": мне всё равно, "`world = apply_action(world, action)`", или "`apply_action(world, action)`", или "`world.apply_action(action)`". Императивный -- в смысле не безумное ООП где ты оверрайдишь пятнадцать методов и отдаёшь объект мега-функции которая их вызывает как-то, а они потом ещё вызывают всякое, или делаешь то же самое higher-order функциями.

Код должен выглядеть так: "`output = do_stuff(input)`". Функция `do_stuff` получает всё что она получает через параметры, возвращает всё что она возвращает через возвращаемые значения и/или мутабельные параметры, и _больше ничего не делает_, не вызывает всякие левые коллбэки, не содержит у себя внутри мини-мейнлуп, ничего такого. Функции должны пассивно обрабатывать данные.

Мейнлуп должен быть один, на самом верхнем уровне, причём поначалу у каждого свой, в своём test.py (не нужно раньше времени пытаться зафиксировать его структуру, копипейстить проще и удобнее), и он должен быть плоским:

    while not world.is_game_over():
        action = strategy1.best_action(world)
        world.apply_action(action)
        action = strategy2.best_action(world)
        world.apply_action(action)
 
Смысл этого в том, что если хочется посмотреть, как оно работает, можно тривиально вставить дебаг принт сюда. Если хочется потестить свою стратегию, можно тривиально это сделать. Если нужно переконвертировать данные из своего формата в тот, который используется чужой функцией, если хочется писать экшены в файл, снапшоты состояния мира в файл, читать их из файла вместо вызова одной или обоих стратегий, использовать reference virtual machine чтобы сравнивать её состояние со своим, или сравнивать разные свои виртуальные машины, или дампить необходимую для визуализатора инфу или визуализировать online, или сдампить текущее состояние и запускать разные стратегии с этой точки, это всё совершенно тривиально делается с таким плоским императивным кодом на самом верхнем уровне.

Если функции принимают и возвращают/модифицируют данные и больше ничего не делают, если наш основной интерфейс это данные, то код становится модульным, легко-понимаемым и легко-модифицируемым.

С другой стороны, как показал прошлый контекст, создание интерфейса Strategy с кучей коллбэков, дёргаемых `world.main_loop()`, вызывает разные безумные желания вроде имплементировать враппер над reference VM как стратегию (что никто кроме автора АПИ не может сделать потому что хуй проссышь, и что нифига не позволяет делать интересные вещи), и дальше Ктулху пожирает мозги. Реально. This actually happened last year, and was not fun at all for everyone involved.

--------

### Reification!

Реификация -- это когда алгоритм `2 + 2` представляется в виде `('+', ('literal', 2), ('literal', 2))`, плюс интерпретатор для этого. Де-реификация -- это наоборот, как бы компиляция в непрозрачную штуку которая делает вещи.

Например, в курсе "Design of Computer Programs" на udacity.com, Peter Norvig показал как написать простенький парсер, который жрёт BNF и текст, и возвращает распарсенное AST. А потом, такой, зацените, что если вместо того, чтобы вернуть тупл `('+', subtree1, subtree2)`, мы вернём `lambda env: subtree1(env) + subtree2(env)`! И так рекурсивно! Совместив таким образом парсер с эвалюатором! Офигенно же, правда? И даже может быть быстрее работает!

Нет, это очень, очень плохо. Если парсер возвращает данные -- AST -- то на них потом можно посмотреть чтобы понять чо ваще, их можно скормить своему эвалюатору, или компилятору который возвращает точно такое же скомпилированное дерево лямбд, или который компилирует его в сишный код, или оптимизатору который делает constant folding and common subexpression elimination, или отдать визуализатору...

А с возвращённой opaque function нифига не сделаешь, и если захочется например вставить внутрь парсера оптимизатор, то во-первых нужно будет понять как работает весь парсер (а не только что он возвращает), потом договориться с чуваком который над ним работает что он там ничего не меняет пока ты не закоммитишь свои улучшения, ну и короче это такой жуткий геморрой что никто этого делать не будет.

Это частный случай предыдущего пункта -- передавать нужно данные, передавать данные -- хорошо (но без фанатизма, конечно).

--------

### `icfpc2012-tbd/username_scratch` is good!

Влад уже написал более детальное описание ("organization.md"), если вкратце: все свои эксперименты и test.py храним в таких директориях на верхнем уровне репозитория, когда очередная штука становится более или менее юзабельной -- пишем докстринг с описанием, тесты всякие, и перекидываем в production.

Смысл в том, что:

* эксперименты тоже важны, не хочется их потерять если что, хочется иметь возможность удалить ненужный код зная что его можно будет достать из истории, хочется показывать их товарищам даже пока они не совсем готовы, другие люди могут на них смотреть чтобы понять как чо и скопипейстить мейнлуп, etc.

* То, что код в личном скретче может быть сколь угодно казуальным, означает что мы можем требовать соответствия минимальным стандартам качества от кода, засунутого в production.

* Побочные эффекты кажутся незначительными: `development/gitk_here.cmd` отсеивает неинтересную историю чужих скретчей, случайно импортнуть модуль из скретча вроде довольно тяжело.

--------

### Хода нет -- пиши инфраструктуру.

Если хочется чего-то поделать, а вроде бы и так уже пять человек пишут свои виртуальные машины (что совершенно прекрасно, потому что потом можно будет их сравнивать и отлавливать глюки!), или усталый моск уже не особо соображает но всё же хочется что-нибудь полезное сделать: у нас наверняка будет огромное количество независимых инфраструктурных возможностей, которые как бы не то что критичны, но окупятся сторицей in the long run (и позволят занять себя и не потерять боевой дух). Программный интерфейс к их вебсайту если там будет что-то интересное или хотя бы чтобы автоматически послать текущую версию, скрипт который запускает все тесты в development, всяческие визуализаторы и анализаторы...

Ну и вообще вкладываться в юзабельные (!) инструменты обычно очень выгодно, даже если дело происходит на вторые-третьи сутки.

--------

### Code style guide, наконец.

Отступы -- четыре пробела. 

Стараемся использовать 'одинарные кавычки' для строк. И '''тройные одинарные кавычки''' для докстрингов (хотя если кто привык к """тройным двойным""" -- ну как хотите, но мне больше нравятся одинарные).

http://docs.python.org/library/logging.html -- в коде в продакшене не должно быть ни одного отладочного print statement. Потому что если нам нужно будет писать результат работы в stdout, и какая-нибудь CENSORED оставит где-нибудь редко-случающийся отладочный принт... А настройки логирования делаются либо в скратчах, либо в самой главной энтри пойнт субмишена, но не в другом продакшон коде.

http://www.python.org/dev/peps/pep-0008/

--------

### Misc.

* Мне, например, не нравится, когда у нас ещё нифига не написано вообще, и совершенно непонятно в чём собственно суть задачи на самом деле, а люди начинают обсуждать всякие высокоуровневые идеи.

* Кстати, давайте попытаемся embrace the spirit of Worse is Better и отправить что-то работающее на lightning round (в первые 24 часа)? Потому что ещё одна recurring theme наших попыток это то, что мы долго пишем всякие крутые штуки, а потом, когда наконец начинаем смотреть как оно всё работает, обнаруживаем что для эффективного решения нужно совсем не то, и проблемы там совсем другие.

Например, в ICFPC 2007 (самом первом в котором мы участвовали) сначала я всех убедил что нефиг разбираться как работает виртуальная машина, надо написать быстрый интерпретатор и решать головоломки; за пять часов до конца контеста я таки решил посмотреть как там всё работает на низком уровне, за три часа до конца контеста я понял какая там function call convention и мы в срочном порядке собрали голыми руками кусочек кода который вызывал разные функции; ну и тогда стало понятно, что основной смысл контеста состоял в написании удобного компилятора который бы это делал. Причём это можно было бы понять через три часа после начала контеста, а не за три часа до конца.

Типа, worse is better потому что пока у тебя нет чего-то работающего хоть как-то, ты практически наверняка не понимаешь что тебе на самом деле нужно сделать. Поэтому чем быстрее сделать что-нибудь хоть как-то работающее (но аджильно, имея в виду что потом лучше бы переписать это _правильно_ и реюзать как можно больше кода при этом), тем больше времени останется на решение по-настоящему интересных проблем.

--------

Комментарии приветствуются.