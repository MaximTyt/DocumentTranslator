import cgi
from googletrans import Translator
from docx2python import docx2python
from nltk import tokenize, download
import docx

len_max = 3000


file_name = '23.11.22.DOCX'
# download('punkt')


def read_txt(path):
    text = ''
    with open(path, encoding="utf_8") as f:
        text = f.read()
    return text


def read_docx(path):
    text_docx = docx2python(path)
    translator = Translator()
    new_list = []
    for i in text_docx.body_runs:
        for j in i:
            for k in j:
                for l in k:
                    for n in l:
                        if n != [] and n.upper().isupper():
                            if '<latex>' in n or '</latex>' in n:
                                n = n.replace('<latex>', '').replace('</latex>', '')
                            new_list.append(n)
    new_list = sorted(list(set(new_list)), reverse=True, key=len)
    for i in range(len(new_list)):
        new_list[i] = new_list[i].replace('\n', '')
    block_list = []
    # разбиваем список на блоки меньше 4к символов
    for i in range(len(new_list)):
        temp = tokenize.sent_tokenize(new_list[i])
        new_list.pop(i)
        for j in temp:
            new_list.append(j)
    temp = ''
    new_list = sorted(list(set(new_list)), reverse=True, key=len)
    for i in new_list:
        if len(temp + i + '\n') <= len_max:
            temp += i + '\n'
        else:
            block_list.append(temp[:-1])
            temp = i + '\n'
    if temp != '':
        block_list.append(temp[:-1])

    # result = [translator.translate(i).text for i in new_list]
    result = []
    for i in block_list:
        print(len(i))
        result.append(translator.translate(i).text)

    new_result = []
    for i in result:
        for j in i.split('\n'):
            new_result.append(j)
    document = docx.Document(path)
    for i in range(len(new_result)):
        for paragraph in document.paragraphs:
            if new_list[i] in paragraph.text:
                paragraph.text = paragraph.text.replace(new_list[i], new_result[i])
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        if new_list[i] in paragraph.text:
                            paragraph.text = paragraph.text.replace(new_list[i], new_result[i])
    document.save('translated_' + path)
    text_docx.close()


# text_txt = read_txt('test.txt')
# result = translator.translate(text_txt)
# print(result.text)


# print(new_list)
# sent_docx = tokenize.sent_tokenize('\r'.join(new_list))
# ent_docx = [i.split('\r') for i in sent_docx]
# n_sent_docx = []
# for i in sent_docx:
#    for j in i:
#        n_sent_docx.append(j)

# n_sent_docx = sorted(list(set(n_sent_docx)), reverse=True, key=len)
# print(new_list)






def docx_find_replace_text(search_text, replace_text, paragraphs):
    """Replace strings and retain the same style.
    The text to be replaced can be split over several runs so
    search through, identify which runs need to have text replaced
    then replace the text in those identified
    """
    for p in paragraphs:
        if search_text in p.text:
            inline = p.runs
            started = False
            search_index = 0
            # found_runs is a list of (inline index, index of match, length of match)
            found_runs = list()
            found_all = False
            replace_done = False
            for i in range(len(inline)):
                # case 1: found in single run so short circuit the replace
                if search_text in inline[i].text and not started:
                    found_runs.append((i, inline[i].text.find(search_text), len(search_text)))
                    text = inline[i].text.replace(search_text, str(replace_text))
                    inline[i].text = text
                    replace_done = True
                    found_all = True
                    break
                if search_text[search_index] not in inline[i].text and not started:
                    # keep looking ...
                    continue
                # case 2: search for partial text, find first run
                if search_text[search_index] in inline[i].text and inline[i].text[-1] in search_text and not started:
                    # check sequence
                    start_index = inline[i].text.find(search_text[search_index])
                    check_length = len(inline[i].text)
                    for text_index in range(start_index, check_length):
                        if inline[i].text[text_index] != search_text[search_index]:
                            # no match so must be false positive
                            break
                    if search_index == 0:
                        started = True
                    chars_found = check_length - start_index
                    search_index += chars_found
                    found_runs.append((i, start_index, chars_found))
                    if search_index != len(search_text):
                        continue
                    else:
                        # found all chars in search_text
                        found_all = True
                        break
                # case 2: search for partial text, find subsequent run
                if search_text[search_index] in inline[i].text and started and not found_all:
                    # check sequence
                    chars_found = 0
                    check_length = len(inline[i].text)
                    for text_index in range(0, check_length):
                        if inline[i].text[text_index] == search_text[search_index]:
                            search_index += 1
                            chars_found += 1
                        else:
                            break
                    # no match so must be end
                    found_runs.append((i, 0, chars_found))
                    if search_index == len(search_text):
                        found_all = True
                        break
            if found_all and not replace_done:
                for i, item in enumerate(found_runs):
                    index, start, length = [t for t in item]
                    if i == 0:
                        text = inline[index].text.replace(inline[index].text[start:start + length], str(replace_text))
                        inline[index].text = text
                    else:
                        text = inline[index].text.replace(inline[index].text[start:start + length], '')
                        inline[index].text = text




# _paragraphs = list(document.paragraphs)
# for t in document.tables:
#    for row in t.rows:
#        for cell in row.cells:
#            for paragraph in cell.paragraphs:
#                _paragraphs.append(paragraph)

# for i in range(len(new_result)):
#    print(f'{new_list[i]} -> {new_result[i]}')
#    docx_find_replace_text(new_list[i], new_result[i], _paragraphs)


