# hack
Skillbox интенсив от 16.11.2020
random + requests
День второй 
flask + requests + itertools

Реализован перебор паролей 
1. Из файла со списком возможных паролей - get_bad_passwords()
2. Последовательный перебор - get_bruteforce()
3. Перебор слов из информации о пользователе get_self_user_words

методы реализованны в виде генираторов 
get_bruteforce() принимает алфавит перебора
Алфавиты :
1. get_alphabet() - числа и строчные английские буквы
2. get_self_user_alphabet() - набор из символов содержащихся в Имени ,Эл.почте и Дне рождения нужного человека

Имя пользователя будем переводить в строчные английские путем транслитирации

реализован подбор пароля hack_password() - принимает имя пользователя и url 
1.  пытаемся подставить общеупотребимый пароль
2.  получаем перечень слов в информации о пользователе и пробуем их разные комбинации (перебор комбинаций - itertools.permutations)
3.  получаем личный алфавит пользователя - и перебираем его
4.  пробуем подбор по общему алфавиту
 
И это будет долго
 
  
 
