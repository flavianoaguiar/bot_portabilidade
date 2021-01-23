import base64
from datetime import date
import requests
import bs4
import os

import AntiCaptcha as anti
import BotInfos as bi
import Oracle
import cx_Oracle

os.environ['NLS_LANG'] = '.AL32UTF8'


def __ini__():
    get_captcha_solution()


def get_captcha_solution():
    request.headers =  bi.headers
    resp = request.get(bi.link_inicio)
    soup = bs4.BeautifulSoup(resp.content, 'html.parser')

    url_captcha = soup.find(id = 'jcap').get('src')
    cod_jcid = soup.find(id='jcid').get('value')

    img_captcha = request.get(bi.link_captcha + url_captcha)

    img_captcha_64 = base64.encodestring(img_captcha.content.strip()).decode()

    anticaptcha = anti.get_captcha(img_captcha_64,100)

    return cod_jcid,anticaptcha


def get_phones_in():
    phones_in = Oracle.consulta_fones()

    return phones_in


def search_phones(cod_jcid, anticaptcha, phones_in):
    phones = []

    for i in phones_in:
        try:
            phones.append(i.get('phone').__str__())
        except:
            pass

    print(len(phones))

    data_post = {'dataInicial': '01/09/2008',
                  'dataFinal': date.today().strftime("%d/%m/%Y"),
                  'arquivo': 'none',
                  'jcid': cod_jcid,
                  'jCaptchaValue': anticaptcha
                }

    for i in range(0,len(phones)):
        data_post.setdefault('telefone['+str(i)+']',phones[i])

    return data_post


def phones_result():

    for n in range(1,10):
        captcha_solution = get_captcha_solution()
        data_post = search_phones(captcha_solution[0], captcha_solution[1], phones_in)

        result = request.post(bi.link_post, data = data_post, timeout = 120 )

        result_soup = bs4.BeautifulSoup(result.content)

        if result_soup.findAll('input', value= 'Digite os caracteres corretamente!'):
            continue

        phones = []

        for phone in result_soup.find(id = 'resultado').findAll('tr'):
            if phone.findAll('td'):
                (fone, prestadora, razao_social, dt_portabilidade, mensagem) = phone.findAll('td')

                if fone.getText():
                    previous_phone = fone.getText()

                phones.append({'fone':previous_phone,
                             'prestadora': prestadora.getText(),
                              'razao_social': razao_social.getText(),
                              'dt_portabilidade': dt_portabilidade.getText(),
                              'mensagem': mensagem.getText()})
            else:
              pass
        return phones


def get_key(phones_in,phones_out):
    phone_key = {}

    for keyIn in phones_in:
        phone_key[keyIn.get('phone').__str__()] = {'pk': keyIn.get('pk'), 'results': [{'mensagem':'Telefone não localizado'}]}

    for keyOut in phones_out:
        if phone_key[keyOut.get('fone').strip()]['results'][0].get('mensagem')=='Telefone não localizado':
            phone_key[keyOut.get('fone').strip()]['results']=[]
        phone_key[keyOut.get('fone').strip()]['results'].append(keyOut)

    return phone_key


def set_phones(phones_key):

    conexao = cx_Oracle.connect('USER_BOT_PORTABILIDADE/bot%1@10.6.4.66:1521/DMBD')
    conexao.begin()

    for idx in phones_key.keys():

        for result in phones_key[idx].get('results'):
            print(result)
            try:
                conexao.cursor().callproc("BOT_PORTABILIDADE.SP_ATUALIZA",[[int(phones_key[idx].get('pk'))],
                                                                                [int(idx)],
                                                                                [str(result.get('prestadora')).strip() or str(' ')] ,
                                                                                [str(result.get('razao_social')).strip()  or str(' ')] ,
                                                                                [str(result.get('dt_portabilidade')).strip() or str(' ')],
                                                                                [str(result.get('mensagem')).strip()],
                                                                                [int(4)]])
            except Exception as e:
                    print(e.args.__str__())

    conexao.close()


if __name__ == '__main__':

    while True:
        try:
            request = requests.Session()

            phones_in = get_phones_in()

            phones_out = phones_result()

            phones_key = get_key(phones_in,phones_out)

            set_phones(phones_key)
        except:
            pass



