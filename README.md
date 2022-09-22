# Нужна ли буква "Ё"?
## Моё мнение - да.

Чтобы ответить на этот вопрос для начала откроем [правила русской орфографии](http://orthographia.ru/orfografia.php?sid=11) и прочитаем:

## Употребление буквы ё может быть последовательным и выборочным.

Последовательное употребление буквы **ё** обязательно в следующих разновидностях печатных текстов:

  - в текстах с последовательно поставленными знаками ударения;

  - в книгах, адресованных детям младшего возраста;

  - в учебных текстах для школьников младших классов и иностранцев, изучающих русский язык.

### Примечание 1.
Последовательное употребление **ё** принято для иллюстративной части настоящих правил.

### Примечание 2.
По желанию автора или редактора любая книга может быть напечатана последовательно с буквой **ё**.

### Примечание 3.
В словарях слова с буквой **ё** размещаются в общем алфавите слов с буквой **е**, напр.: еле, елейный, ёлка, еловый, елозить, ёлочка, ёлочный, ель; веселеть, веселить(ся), весёлость, весёлый, веселье.

В обычных печатных текстах буква **ё** употребляется выборочно. Рекомендуется употреблять её в следующих случаях.
  1. Для предупреждения неправильного опознания слова, напр.: всё, нёбо, лётом, совершённый (в отличие соответственно от слов все, небо, летом, совершенный), в том числе для указания на место ударения в слове, напр.: вёдро, узнаём (в отличие от ведро, узнаем).
  
  2. Для указания правильного произношения слова — либо редкого, недостаточно хорошо известного, либо имеющего распространенное неправильное произношение, напр.: гёзы, сёрфинг, флёр, твёрже, щёлочка, в том числе для указания правильного ударения, напр.: побасёнка, приведённый, унесённый, осуждённый, новорождённый, филёр.
 
  3. В собственных именах — фамилиях, географических названиях, напр.: Конёнков, Неёлова, Катрин Денёв, Шрёдингер, Дежнёв, Кошелёв, Чебышёв, Вёшенская, Олёкма.

## Мой исследование
Мне стало интересно, сколько русских слов можно написать без **ё**, при этом привратив слово в слово с другим значением. Для этого я написал небольшую программу на JavaScript:

```js
const fs = require("fs");
let words1 = fs.readFileSync("./Data/russianUTF-8.txt").toString();
words1 = words1.split("\n");
if (words1.length && words1[0].at(-1) == "\r")
  words1 = words1.map((word) => word.slice(0, -1));

let words2 = fs.readFileSync("./Data/summary.txt").toString();
words2 = words2.split("\n");
if (words2.length && words2[0].at(-1) == "\r")
  words2 = words2.map((word) => word.slice(0, -1));

let output = "";
let searchWord = "";
let id = 1;
for (let i = 0; i < words1.length; i++) {
  if (/ё/gi.test(words1[i])) {
    searchWord = words1[i].replace("ё", "е");
    for (let j = 0; j < words2.length; j++) {
      if (searchWord == words2[j]) {
        output += "| " + id + " | " + words1[i] + " | " + words2[j] + " |\n";
        id++;
      }
    }
  }
}

fs.writeFileSync("./Data/Output.txt", output);
```
Она будет менять букву **ё** на **е** и искать в [базе данных](https://github.com/LussRus/Rus_words) из ~1 500 000 русских слов и искать совпадения. Ниже предоставлен вывод программы, 180 слов

| Id | Слово 1 | Слово 2 |
|-|-|-|
| 1 | акушёр | акушер |
| 2 | багрённый | багренный |
| 3 | белёна | белена |
| 4 | белённой | беленной |
| 5 | берёг | берег |
| 6 | берёстовый | берестовый |
| 7 | берёт | берет |
| 8 | благоприобретённый | благоприобретенный |
| 9 | бревёшко | бревешко |
| 10 | вахтёр | вахтер |
| 11 | вёдро | ведро |
| 12 | вёсельный | весельный |
| 13 | весьёгонский | весьегонский |
| 14 | взблёскивать | взблескивать |
| 15 | взвихрённый | взвихренный |
| 16 | вздвоённый | вздвоенный |
| 17 | вклинённый | вклиненный |
| 18 | вкраплённый | вкрапленный |
| 19 | гравёр | гравер |
| 20 | гружённый | груженный |
| 21 | далёко | далеко |
| 22 | далёко | далеко |
| 23 | двухвёсельный | двухвесельный |
| 24 | дёгтевой | дегтевой |
| 25 | доволочённый | доволоченный |
| 26 | ёканье | еканье |
| 27 | ёкать | екать |
| 28 | ёрник | ерник |
| 29 | желёзка | железка |
| 30 | жёлчеотделение | желчеотделение |
| 31 | живёте | живете |
| 32 | жолнёр | жолнер |
| 33 | жолнёрский | жолнерский |
| 34 | загнётка | загнетка |
| 35 | загружённый | загруженный |
| 36 | задёшево | задешево |
| 37 | заманённый | заманенный |
| 38 | замёта | замета |
| 39 | замётка | заметка |
| 40 | занаряжённый | занаряженный |
| 41 | заозёрье | заозерье |
| 42 | запоём | запоем |
| 43 | запорошённый | запорошенный |
| 44 | запрёт | запрет |
| 45 | запружённый | запруженный |
| 46 | заряжённый | заряженный |
| 47 | засёкший | засекший |
| 48 | заснежённый | заснеженный |
| 49 | засолённый | засоленный |
| 50 | затворённый | затворенный |
| 51 | заторможённость | заторможенность |
| 52 | заторможённый | заторможенный |
| 53 | заточённый | заточенный |
| 54 | издалёка | издалека |
| 55 | изрёкший | изрекший |
| 56 | истёкший | истекший |
| 57 | источённый | источенный |
| 58 | клакёр | клакер |
| 59 | колёсник | колесник |
| 60 | колотьё | колотье |
| 61 | комбайнёр | комбайнер |
| 62 | комбайнёрка | комбайнерка |
| 63 | комбайнёрша | комбайнерша |
| 64 | лёгонек | легонек |
| 65 | лёгонько | легонько |
| 66 | лён | лен |
| 67 | лёта | лета |
| 68 | лёток | леток |
| 69 | лётом | летом |
| 70 | маркёр | маркер |
| 71 | матёрой | матерой |
| 72 | мёд | мед |
| 73 | мёдистый | медистый |
| 74 | мёл | мел |
| 75 | мёл | мел |
| 76 | мелёна | мелена |
| 77 | мерёжка | мережка |
| 78 | мёртво | мертво |
| 79 | мётчик | метчик |
| 80 | мётчик | метчик |
| 81 | мещёрский | мещерский |
| 82 | миткалёвый | миткалевый |
| 83 | многовёсельный | многовесельный |
| 84 | наволочённый | наволоченный |
| 85 | нагружённый | нагруженный |
| 86 | надушённый | надушенный |
| 87 | наперчённый | наперченный |
| 88 | напоённый | напоенный |
| 89 | наряжённый | наряженный |
| 90 | натружённый | натруженный |
| 91 | начинённый | начиненный |
| 92 | нёбо | небо |
| 93 | недалёко | недалеко |
| 94 | оберёг | оберег |
| 95 | обрамлённый | обрамленный |
| 96 | обронённый | оброненный |
| 97 | оглашённые | оглашенные |
| 98 | оглашённый | оглашенный |
| 99 | околёсица | околесица |
| 100 | окунёвый | окуневый |
| 101 | падёж | падеж |
| 102 | падёжный | падежный |
| 103 | пёк | пек |
| 104 | пеклёванный | пеклеванный |
| 105 | первоочерёдной | первоочередной |
| 106 | переволочённый | переволоченный |
| 107 | перегружённый | перегруженный |
| 108 | перёд | перед |
| 109 | перезаряжённый | перезаряженный |
| 110 | перекошённый | перекошенный |
| 111 | переманённый | переманенный |
| 112 | перемёр | перемер |
| 113 | пересёкший | пересекший |
| 114 | пересёкшийся | пересекшийся |
| 115 | пересечённый | пересеченный |
| 116 | разгромлённый | разгромленный |
| 117 | разгружённый | разгруженный |
| 118 | раздвоённый | раздвоенный |
| 119 | раздроблённость | раздробленность |
| 120 | раздроблённый | раздробленный |
| 121 | разжижённый | разжиженный |
| 122 | размётка | разметка |
| 123 | размёточный | разметочный |
| 124 | размётчик | разметчик |
| 125 | размётчица | разметчица |
| 126 | разряжённый | разряженный |
| 127 | рассёкший | рассекший |
| 128 | рассёкшийся | рассекшийся |
| 129 | рассорённый | рассоренный |
| 130 | растворённый | растворенный |
| 131 | растлённый | растленный |
| 132 | расторможённость | расторможенность |
| 133 | расторможённый | расторможенный |
| 134 | расточённый | расточенный |
| 135 | сажённый | саженный |
| 136 | сволочённый | сволоченный |
| 137 | свящённый | священный |
| 138 | сёкший | секший |
| 139 | селезнёвый | селезневый |
| 140 | сечённый | сеченный |
| 141 | силён | силен |
| 142 | твёрдо | твердо |
| 143 | твержённый | тверженный |
| 144 | тёлок | телок |
| 145 | тёмненько | темненько |
| 146 | тёмно | темно |
| 147 | тёмно | темно |
| 148 | топлёный | топленый |
| 149 | тополёвый | тополевый |
| 150 | точённый | точенный |
| 151 | травлёный | травленый |
| 152 | трёпан | трепан |
| 153 | уволочённый | уволоченный |
| 154 | угрёвой | угревой |
| 155 | угрызённый | угрызенный |
| 156 | уменьшённый | уменьшенный |
| 157 | унижённо | униженно |
| 158 | унижённость | униженность |
| 159 | унижённый | униженный |
| 160 | упоённый | упоенный |
| 161 | уравнённый | уравненный |
| 162 | усёкший | усекший |
| 163 | усугублённый | усугубленный |
| 164 | утончённый | утонченный |
| 165 | уторённый | уторенный |
| 166 | Фёдора | Федора |
| 167 | фён | фен |
| 168 | холёный | холеный |
| 169 | чабёр | чабер |
| 170 | чём | чем |
| 171 | чёркан | черкан |
| 172 | чёрта | черта |
| 173 | четвёрток | четверток |
| 174 | чинённый | чиненный |
| 175 | шабёр | шабер |
| 176 | шёлкография | шелкография |
| 177 | шёрстопрядильня | шерстопрядильня |
| 178 | шестивёсельный | шестивесельный |
| 179 | шлём | шлем |
| 180 | шумёр | шумер |

## Вывод

При свободном использовании буквы **ё** есть небольшая вероятность изменить значение предложения, поэтому я не согласен с изменениями правил орфографии в 1956 году, допускающих добровольное использование данной буквы.

Да, они похожи в написании, но на этом их сходства заканчиваются. Фонетически у них разное звучание и человек может не правильно трактировать смысл вашего текста.

Так же стоит подметить, что мои притензии не распространяются на переписку в разговорном стиле. Там допустимо и сокращение слов и использование буквы **е** вместо **ё** для быстроты диалога.
