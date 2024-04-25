"""
Funções de transformação a serem usadas nas cargas ("T" do ETL).
"""

import html
import re
from datetime import date, datetime


"""
Módulo com as classes de transformação de dados ("T" do ETL)
"""

class Copia():
    """
    Cópia simples de dados, sem transformações ou nenhum tipo de alteração.
    """

    def transforma(self, entradas):
        """
        Copia a entrada, sem nenhuma transformação.

        Args:
            entradas   : tupla com o valor a ser copiado; como não faz
                         transformação alguma, só pode haver um elemento na
                         tupla
        Ret:
            cópia do valor de entrada
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada para cópia.")

        return entradas[0]

class ValorFixo():
    """
    Transforma a entrada num valor fixo.
    """

    def __init__(self, valor):
        self.__valor = valor

    def transforma(self, entradas):
        """
        Retorna um valor fixo, definido na instanciação do objeto. Para valores
        NULL em banco de dados, informar tipo de dados None do Python.

        Args:
            entradas   : não é necessário, mantido apenas para consistência da 
                         interface
        Ret:
            Valor definido na instanciação da classe
        """

        return self.__valor

class DePara():
    """
    Faz um de/para dos valores de entrada.
    """

    def __init__(self, 
            de_para, 
            copia_se_nao_encontrado=True,
            trim=True):
        """
        Args:
            de_para: dict com o de/para desejado
            copia_se_nao_encontrado: se True, copia valor da entrada para a
                                     saída caso valor de entrada não seja
                                     encontrado no de/para; se False, dispara
                                     exceção
            trim: indica se antes do de/para será feito um trim no dado de
                  entrada
        """
        self.__de_para = de_para
        self.__copia_se_nao_encontrado = copia_se_nao_encontrado
        self.__trim = trim

        # TODO: criar outras condições se não achar o valor no de/para: preenche null ou um valor específico; tem que mudar o método transforma() abaixo e ver quais impactos na classe filha deparasn

    def transforma(self, entradas):
        """
        Retorna um de/para dos valores de entrada.

        Args:
            entradas   : tupla com o valor a ser transformado; como só
                         transforma um valor em outro, só pode haver um
                         elemento na tupla
        Ret:
            De/para da entrada.
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada para um de/para.")

        for item in entradas:
            # pandas utiiliza nan para valores não informados num dataframe
            if str(item) == "nan":
                item = None

            if item is not None and self.__trim:
                try:
                    item = item.strip()
                except:
                    # se tipo não for uma string (ou seja, não implementar
                    # strip()) então não faz nada
                    pass

            if item in list(self.__de_para):
                return self.__de_para[item]

        if self.__copia_se_nao_encontrado:
            return entradas[0]
        else:
            # TODO: disparar uma exceção específica pra master job decidir se quer continuar ou não se não achar de/para não achou a key no de_para informado no construtor
            raise RuntimeError(
                "Impossível fazer a transformação, valor de de/para não encontrado.")

class DeParaSN(DePara):
    """
    Faz um de/para de campos S/N para 1/0 e vice-versa. Considera também
    a língua (por exemplo, Y/N ao invés de S/N).
    """

    def __init__(self, 
            copia_se_nao_encontrado=True, 
            inverte=False, 
            val_int=True, 
            lingua="pt"):
        """
        Args:
            copia_se_nao_encontrado : dispara execeção de erro caso valor não
                                      seja encontrado no de/para; se False,
                                      copia valor da entrada para a saída
            inverte                 : se de/para é de S/N para 1/0 ou de 1/0 
                                      para S/N
            val_int                 : se valor 1/0 deve ser um inteiro ou
                                      string
            lingua                  : "pt" ou "en"
        """

        if lingua == "pt" and val_int and not inverte:
            de_para = {"S": 1, "N": 0}
        elif lingua == "pt" and not val_int and not inverte: 
            de_para = {"S": "1", "N": "0"}

        elif lingua == "pt" and val_int and inverte: 
            de_para = {1: "S", 0: "N"}
        elif lingua == "pt" and not val_int and inverte: 
            de_para = {"1": "S", "0": "N"}

        elif lingua == "en" and val_int and not inverte: 
            de_para = {"Y": 1, "N": 0}
        elif lingua == "en" and not val_int and not inverte: 
            de_para = {"Y": "1", "N": "0"}

        elif lingua == "en" and val_int and inverte: 
            de_para = {1: "Y", 0: "N"}
        elif lingua == "en" and not val_int and inverte: 
            de_para = {"1": "Y", "0": "N"}

        super().__init__(de_para, copia_se_nao_encontrado, trim=True)

class DeParaChar():
    """
    Faz um de/para de um ou mais caracteres em um texto.

    Atenção: não é preciso trocar aspa simples (') por duas aspas simples ('')
    antes de salvar uma string com aspas simples no banco (por exemplo, a
    string "d'água"), o Blipy já faz essa troca por default.
    """

    def __init__(self, de_para = None):
        """
        Args:
             de_para  : dict com o(s) de/para de caracteres desejados
        """
        self.__de_para = de_para

    def transforma(self, entradas):
        """
        Retorna um texto com um conjunto de caracteres transformados a partir de
        um dict de/para.

        Args:
            entradas : tupla contendo o texto de entrada a ser transformado
        """

        if self.__de_para is None:
            raise RuntimeError(
                "Impossível fazer a transformação, dicionário de/para não encontrado.")

        texto = entradas[0]

        # pandas utiiliza nan para valores não informados num dataframe
        if str(texto) == "nan":
            texto = None

        if texto is not None:
            for chave in self.__de_para.keys():
                texto = texto.replace(chave, self.__de_para[chave])

        return texto

class Somatorio():
    """
    Calcula o somatório dos valores de entrada.
    """

    def transforma(self, entradas):
        """
        Calcula o somatório dos valores de entrada.

        Args:
            entradas   : tupla com os valores a serem somados
        Ret:
            somatório dos valores de entrada
        """

        soma = 0
        for item in entradas:
            if item is not None and str(item) != "nan":
                soma += item
        return soma

class Media():
    """
    Calcula a média dos valores de entrada.
    """

    def transforma(self, entradas):
        """
        Calcula a média dos valores de entrada.

        Args:
            entradas   : tupla com os valores dos quais calcular a média
        Ret:
            média dos valores de entrada
        """

        soma = f_somatorio.transforma(entradas)
        return soma/len(entradas)

class Agora():
    """
    Calcula o dia ou dia/hora atual do banco de dados ou do sistema 
    operacional.
    """

    def __init__(self, conexao=None, so_data=False):
        """
        Args:
            conexao : conexão com o banco de dados (caso se busque a
                      informação no banco) ou None se for para buscar no
                      sistema operacional
            so_data : flag se é para trazer só a data ou a hora também
        """
        self.__so_data = so_data
        self.__conn = conexao

    def transforma(self, entradas):
        """
        Calcula o dia/hora atual.

        Args:
            entradas   : não é necessário, mantido apenas para consistência da 
                         interface
        Ret:
            Dia (ou dia/hora) atual do banco de dados ou do sistema
            operacional, a depender de como o objeto foi construído.
        """

        if self.__conn is None:
            # busca do sistema operacional
            if self.__so_data:
                ret = date.today()
            else:
                ret = datetime.now().replace(microsecond=0)
        else:
            # busca do banco de dados
            if self.__so_data:
                ret = self.__conn.get_agora().replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                ret = self.__conn.get_agora().replace(microsecond=0)

        return ret

class HTMLParaTxt():
    """
    Converte uma string com formatação em HTML (tags e acentuação) para um
    texto puro. As tags encontradas serão simplesmente eliminadas do texto
    final. 

    Como textos em HMTL tendem a ser grandes, opcionalmente a string de retorno
    pode ser truncada em uma determinada quantidade de bytes; este trunc leva
    em consideração os bytes necessários para acentuação em UTF-8.
    """
 
    def __init__(self, qtd_bytes=None):
        """
        Args:
        :param qtd_bytes: opcional; quantidade de bytes para um trunc da string
        final.
        """
        self.__qtd_bytes = qtd_bytes
 
    def transforma(self, entradas):
        """
        Retorna a string da entrada em HTML transformada para texto puro, com
        ou sem trunc. Se entrada for None, retorna None.

        # TODO: FIXME: se o HTML tiver os caracteres '<' ou '>' na sua parte
        # textual essa função provavelmente falhará

        Args:
            entradas : tupla contendo a string a ser transformada
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada.")

        if entradas[0] is None or   \
           str(entradas[0]) == "nan":
            return None

        ret = entradas[0]
        ret = ret.replace("\r", " ")
        ret = ret.replace("\n", " ")
        ret = ret.replace("\t", " ")

        # trata o html, corrigindo os acentos e retirando as tags
        ret = re.sub("(?<=<).*?(?=>)", "", html.unescape(ret))
        ret = ret.replace("\xa0", " ")
        ret = ret.replace("<>", "")

        # troca aspas simples do texto por duas aspas simples, para não dar
        # problema na hora da inserção no oracle
        ret = DeParaChar({"'": "''"}).transforma((ret, ))

        # retira excessos de espaços em branco
        ret = Trim().transforma((ret, ))
        ret = re.sub("\s{2,}", " ", ret)

        if self.__qtd_bytes is not None:
            ret = TruncaStringByte(self.__qtd_bytes).transforma((ret, ))

        return ret

class Trim():
    """
    Faz um trim numa string. Pode-se parametrizar se será um trim no início e
    fim, só no início ou só no fim.
    """
 
    def __init__(self, tipo_trim = "inicio_fim"):
        """
        Args:
        :param tipo_trim: tipo de trim a ser feito. Valores possíveis:
        "inicio_fim", "inicio", "fim"
        """
        self.__tipo_trim = tipo_trim
 
    def transforma(self, entradas):
        """
        Retorna a string da entrada com trim. Se entrada for None, retorna
        None.

        Args:
            entradas : tupla contendo a string a ser transformada
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada para trim.")

        if entradas[0] is None or   \
           str(entradas[0]) == "nan":
            return None

        if self.__tipo_trim == "inicio_fim":
            trim = entradas[0].strip()
        elif self.__tipo_trim == "inicio":
            trim = entradas[0].ltrip()
        elif self.__tipo_trim == "fim":
            trim = entradas[0].rtrip()
        else:
            raise RuntimeError(
                "Tipo de trim incorreto.")

        return trim

class TruncaStringByte():
    """
    Trunca uma string até o número de bytes informado. Caracteres acentuados
    são considerados, de forma que é garantido que a quantidade de bytes
    utilizados para a string nunca é maior que a quantidade máxima de bytes
    informado no construtor.
    """
 
    def __init__(self, qtd_bytes):
        """
        Args:
        :param qtd_bytes: quantidade de bytes que a string terá ao final
        """
        self.__qtd_bytes = qtd_bytes
 
    def transforma(self, entradas):
        """
        Retorna a string truncada. Se entrada for None, retorna None.

        Args:
            entradas : tupla contendo a string a ser transformada
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada para truncar.")

        if entradas[0] is None or       \
           str(entradas[0]) == "nan":
            return None
        
        # solução obtida em https://stackoverflow.com/questions/13665001/python-truncating-international-string
        if len(entradas[0].encode('utf-8')) > self.__qtd_bytes:
            trunc = \
                entradas[0].encode('utf-8')[:self.__qtd_bytes].decode('utf-8',
                'ignore')
        else: 
            trunc = entradas[0]

        return trunc

class LookupViaTabela():
    """
    Transforma o dado a partir de uma tabela de lookup informada.
    """
 
    def __init__(self, 
            conexao, 
            tabela_lookup, 
            campo, 
            chave,
            filtro = ""):
        """
        Args:
        conexao:        conexão com o banco de dados que contém a tabela de
                        lookup
        tabela_lookup:  a tabela de lookup
        campo:          o campo a ser retornado da lookup
        chave:          o(s) campo(s) na tabela de lookup que liga(m) as duas
                        tabelas. Pode ser uma string apenas ou uma lista de
                        strings com os nomes dos campos
        filtro:         opcional; um filtro que pode ser aplicado ao montar a
                        cláusula WHERE do SQL de busca

        Por exemplo, para buscar o texto de informação na tabela de informação
        da solução para o tipo 31 de uma determinada solução, ou seja, para
        executar o comando SQL abaixo:

        'select TX_INFORMACAO 
        from INFO_SOLUCAO 
        where
        ID_TIPO_INFORMACAO = 31 and ID_SOLUCAO = 2207'

        e considerando que a chave que liga as duas tabelas na lookup é
        ID_SOLUCAO, os parâmetros devem ser:

        tabela_lookup = 'INFO_SOLUCAO'
        campo = 'TX_INFORMACAO'
        chave = 'ID_SOLUCAO'
        filtro = 'ID_TIPO_INFORMACAO = 31'

        O valor de ID_SOLUCAO no SQL final será preenchido automaticamente a
        cada linha no loop de carga da tabela de origem.
        """

        self.__conexao = conexao
        self.__tabela_lookup = tabela_lookup
        self.__campo = campo
        self.__chave = chave
        self.__filtro = filtro
 
    def transforma(self, entradas):
        """
        Retorna o dado buscado numa tabela de lookup, usando a entrada
        informada como parâmetro de busca na lookup.

        Args:
            entradas: lista com a(s) chave(s) de busca da lookup
        """

        # não faz sentido buscar por uma chave que seja NULL
        for i in entradas:
            if i is None or str(i) == "nan":
                return None

        where = \
            self.__filtro + " AND " if self.__filtro != "" else \
            ""

        sql =   "select " + self.__campo +              \
                " from " + self.__tabela_lookup +       \
                " where " + where

        # TODO: FIXME: se o tipo da chave for date, o código abaixo
        # provavelmente não vai funcionar, pois datas devem ter uma formatação
        # específica para serem usadas na string SQL. Mas quem põe data como
        # chave de lookup merece sofrer mesmo
        if type(self.__chave) is list:
            chave = ""
            for i, v in enumerate(self.__chave):
                chave += v + " = "
                chave += \
                    str(entradas[i]) if type(entradas[i]) is not str else \
                    "'" + str(entradas[i]) + "'"
                chave += " AND "
            chave = chave[:-5]
        else:
            chave = self.__chave + " = "
            chave += \
                str(entradas[0]) if type(entradas[0]) is not str else \
                "'" + str(entradas[0]) + "'"
        sql += chave

        try:
            registro = self.__conexao.consulta(sql)
        except:
            raise RuntimeError("Erro na execução do SELECT no banco de dados.")

        try:
            ret = next(registro)[0]
        except StopIteration:
            ret = None

        return ret
    

class ConcatenaStrings():
    """
    Concatena duas ou mais strings.
    """
 
    def __init__(self, trim=None, sep=None):
        """
        Args:
        trim:   tipo de trim que será feito nas strings de entrada e/ou de
                saída. Valores possíveis: None (nenhum trim é efetuado),
                "entradas" (um trim é feito em cada string de entrada antes da
                concatenação) ou "resultado" (um trim é feito apenas na string
                resultante da concatenação das entradas). Todos os trims, se
                feitos, são feitos tanto no início como no fim da string
        sep:    string opcional para ser usada como um separador entre as
                strings de entrada
        """
        if trim is not None and trim != "entradas" and trim != "resultado":
            raise RuntimeError("Parâmetro de trim incorreto.")

        self.__trim = trim
        self.__sep = sep

    def transforma(self, entradas):
        """
        Retorna a concatenação das strings de entrada, na ordem em que foram
        informadas.

        Args:
            entradas : tupla com as strings a serem concatenadas
        """

        if len(entradas) < 2:
            raise RuntimeError(
                    "São necessárias ao menos duas strings para fazer a "
                    "concatenação.")

        ret = ""
        for s in entradas:
            if s is not None:
                if self.__trim == "entradas":
                    ret += str(s).strip()
                else:
                    ret += str(s)

                if self.__sep is not None:
                    ret += self.__sep

        if self.__sep is not None and ret != "":
            ret = ret[0:len(ret) - len(self.__sep)]

        if self.__trim == "resultado":
            ret = ret.strip()

        return ret

class MontaDataMesAno():
    """
    Dados um mês e ano obtidos de um registro de entrada, cria uma data com o
    dia informado no construtor desta classe. Se mês ou ano forem None, retorna
    None. O ano pode ter 2 ou 4 dígitos.
    """
 
    def __init__(self, dia=1):
        """
        Args:
        dia: o dia a ser juntado ao mês e ano para formar uma data
        """

        if dia < 1 or dia > 31:
            raise RuntimeError(
                "Dia para criação da data tem que estar entre 1 e 31.")

        self.__dia = dia

    def transforma(self, entradas):
        """
        Gera uma data a partir do mês e ano lidos do registro de entrada.

        Args:
            entradas :  tupla com o mês e o ano para a geração da data. Se mês
                        ou ano forem None, retorna None. O ano pode ter 2 ou 4
                        dígitos.
        """

        if len(entradas) != 2:
            raise RuntimeError(
                "Um mês e um ano devem ser informados para gerar uma data.")

        if entradas[0] is None or entradas[1] is None:
            return None

        return datetime.strptime(
                str(self.__dia) + "/" + 
                str(entradas[0]).zfill(2) + "/" + str(entradas[1]), 
                "%d/%m/%Y" if len(str(entradas[1])) == 4 else "%d/%m/%y" )

class InverteSinal():
    """
    Inverte o sinal de um valor. Trata tanto números quanto strings que
    contenham um número.
    """

    def transforma(self, entradas):
        """
        Inverte o sinal do valor passado como argumento. Caso o argumento seja
        uma string, ela é primeiro transformada num número, não importando se
        o separador de decimal da string é vírgula ou ponto.

        Args:
        entradas: tupla com o valor a ter o sinal invertido
        """
        
        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada para uma "
                "inversão de sinal.")

        if entradas[0] is None:
            return None

        if type(entradas[0]) == str:
            val = entradas[0].replace(",", ".")
            val = float(val)
        else:
            val = entradas[0]

        return val*(-1)

# TODO: implementar classe de transformação de conversão tipo

#  objetos de classes de transformação que só fazem sentido ter uma instância 
#  (singletons). Desta forma, ao importar este módulo estes objetos já estarão
#  instanciandos e bastará utilizá-los, sem necessidade de criar uma nova
#  instância no código que importou este módulo
f_copia     = Copia()
f_somatorio = Somatorio()
f_media     = Media()

