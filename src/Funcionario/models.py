from django.db import models
from django.dispatch import receiver
import os
from django.core.validators import RegexValidator
from . import utilities
from ControleAdministrativo.models import FuncionarioCargo, FuncionarioNivel
from datetime import date

# App Logic ------------------------------------------------------------------------------------------------------------------------------------------

# Choice Fields Lists
brazilian_states_choices    = [
    ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'),
    ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')
]
race_choices                = [
    ('INDIGENA', 'Indigena'), ('BRANCA', 'Branca'), ('NEGRA', 'Negra'), ('AMARELA', 'Amarela'), ('PARDA', 'Parda'), ('NAO_INFORMADO', 'Prefiro Não Informar')
]
gender_choices              = [
    ('MASCULINO', 'Masculino'), ('FEMININO', 'Feminino'), ('OUTRO', 'Outro'), ('NAO_INFORMADO', 'Prefiro Não Informar')
]
civil_state_choices         = [
    ('CASADO', 'Casado(a)'), ('SOLTEIRO', 'Solteiro(a)'), ('VIUVO', 'Viuvo(a)'),
    ('DIVORCIADO', 'Divorciado(a)'), ('UNIAO ESTAVEL', 'União Estável')
]
country_choices             = [
    ('Afeganistão', 'Afeganistão'), ('África do Sul', 'África do Sul'), ('Akrotiri', 'Akrotiri'), ('Albânia', 'Albânia'), ('Alemanha', 'Alemanha'), ('Andorra', 'Andorra'), ('Angola', 'Angola'), ('Anguila', 'Anguila'), ('Antárctida', 'Antárctida'), ('Antígua e Barbuda', 'Antígua e Barbuda'), ('Arábia Saudita', 'Arábia Saudita'), ('Arctic Ocean', 'Arctic Ocean'), ('Argélia', 'Argélia'), ('Argentina', 'Argentina'), ('Arménia', 'Arménia'), ('Aruba', 'Aruba'), ('Ashmore and Cartier Islands', 'Ashmore and Cartier Islands'), ('Atlantic Ocean', 'Atlantic Ocean'), ('Austrália', 'Austrália'), ('Áustria', 'Áustria'), ('Azerbaijão', 'Azerbaijão'), ('Baamas', 'Baamas'), ('Bangladeche', 'Bangladeche'), ('Barbados', 'Barbados'), ('Barém', 'Barém'), ('Bélgica', 'Bélgica'), ('Belize', 'Belize'), ('Benim', 'Benim'), ('Bermudas', 'Bermudas'), ('Bielorrússia', 'Bielorrússia'), ('Birmânia', 'Birmânia'), ('Bolívia', 'Bolívia'), ('Bósnia e Herzegovina', 'Bósnia e Herzegovina'), ('Botsuana', 'Botsuana'), ('Brasil', 'Brasil'), ('Brunei', 'Brunei'), ('Bulgária', 'Bulgária'), ('Burquina Faso', 'Burquina Faso'), ('Burúndi', 'Burúndi'), ('Butão', 'Butão'), ('Cabo Verde', 'Cabo Verde'), ('Camarões', 'Camarões'), ('Camboja', 'Camboja'), ('Canadá', 'Canadá'), ('Catar', 'Catar'), ('Cazaquistão', 'Cazaquistão'), ('Chade', 'Chade'), ('Chile', 'Chile'), ('China', 'China'), ('Chipre', 'Chipre'), ('Clipperton Island', 'Clipperton Island'), ('Colômbia', 'Colômbia'), ('Comores', 'Comores'), ('Congo-Brazzaville', 'Congo-Brazzaville'), ('Congo-Kinshasa', 'Congo-Kinshasa'), ('Coral Sea Islands', 'Coral Sea Islands'), ('Coreia do Norte', 'Coreia do Norte'), ('Coreia do Sul', 'Coreia do Sul'), ('Costa do Marfim', 'Costa do Marfim'), ('Costa Rica', 'Costa Rica'), ('Croácia', 'Croácia'), ('Cuba', 'Cuba'), ('Curacao', 'Curacao'), ('Dhekelia', 'Dhekelia'), ('Dinamarca', 'Dinamarca'), ('Domínica', 'Domínica'), ('Egipto', 'Egipto'), ('Emiratos Árabes Unidos', 'Emiratos Árabes Unidos'), ('Equador', 'Equador'), ('Eritreia', 'Eritreia'), ('Eslováquia', 'Eslováquia'), ('Eslovénia', 'Eslovénia'), ('Espanha', 'Espanha'), ('Estados Unidos', 'Estados Unidos'), ('Estónia', 'Estónia'), ('Etiópia', 'Etiópia'), ('Faroé', 'Faroé'), ('Fiji', 'Fiji'), ('Filipinas', 'Filipinas'), ('Finlândia',
    'Finlândia'), ('França', 'França'), ('Gabão', 'Gabão'), ('Gâmbia', 'Gâmbia'), ('Gana', 'Gana'), ('Gaza Strip', 'Gaza Strip'), ('Geórgia', 'Geórgia'), ('Geórgia do Sul e Sandwich do Sul', 'Geórgia do Sul e Sandwich do Sul'), ('Gibraltar', 'Gibraltar'), ('Granada', 'Granada'), ('Grécia', 'Grécia'), ('Gronelândia', 'Gronelândia'), ('Guame', 'Guame'), ('Guatemala', 'Guatemala'), ('Guernsey', 'Guernsey'), ('Guiana', 'Guiana'), ('Guiné', 'Guiné'), ('Guiné Equatorial', 'Guiné Equatorial'), ('Guiné-Bissau', 'Guiné-Bissau'), ('Haiti', 'Haiti'), ('Honduras', 'Honduras'), ('Hong Kong', 'Hong Kong'), ('Hungria', 'Hungria'), ('Iémen', 'Iémen'), ('Ilha Bouvet', 'Ilha Bouvet'), ('Ilha do Natal', 'Ilha do Natal'), ('Ilha Norfolk', 'Ilha Norfolk'), ('Ilhas Caimão', 'Ilhas Caimão'), ('Ilhas Cook', 'Ilhas Cook'), ('Ilhas dos Cocos', 'Ilhas dos Cocos'), ('Ilhas Falkland', 'Ilhas Falkland'), ('Ilhas Heard e McDonald', 'Ilhas Heard e McDonald'), ('Ilhas Marshall', 'Ilhas Marshall'), ('Ilhas Salomão', 'Ilhas Salomão'), ('Ilhas Turcas e Caicos', 'Ilhas Turcas e Caicos'), ('Ilhas Virgens Americanas', 'Ilhas Virgens Americanas'), ('Ilhas Virgens Britânicas', 'Ilhas Virgens Britânicas'), ('Índia', 'Índia'), ('Indian Ocean', 'Indian Ocean'), ('Indonésia', 'Indonésia'), ('Irão', 'Irão'), ('Iraque', 'Iraque'), ('Irlanda', 'Irlanda'), ('Islândia', 'Islândia'), ('Israel', 'Israel'), ('Itália', 'Itália'), ('Jamaica', 'Jamaica'), ('Jan Mayen', 'Jan Mayen'), ('Japão', 'Japão'), ('Jersey', 'Jersey'), ('Jibuti', 'Jibuti'), ('Jordânia', 'Jordânia'), ('Kosovo', 'Kosovo'), ('Kuwait', 'Kuwait'), ('Laos', 'Laos'), ('Lesoto', 'Lesoto'), ('Letónia', 'Letónia'), ('Líbano', 'Líbano'), ('Libéria', 'Libéria'), ('Líbia', 'Líbia'), ('Listenstaine', 'Listenstaine'), ('Lituânia', 'Lituânia'), ('Luxemburgo', 'Luxemburgo'), ('Macau',
    'Macau'), ('Macedónia', 'Macedónia'), ('Madagáscar', 'Madagáscar'), ('Malásia', 'Malásia'), ('Malávi', 'Malávi'), ('Maldivas', 'Maldivas'), ('Mali', 'Mali'), ('Malta', 'Malta'), ('Man, Isle of', 'Man, Isle of'), ('Marianas do Norte', 'Marianas do Norte'), ('Marrocos', 'Marrocos'), ('Maurícia', 'Maurícia'), ('Mauritânia', 'Mauritânia'), ('México', 'México'), ('Micronésia', 'Micronésia'), ('Moçambique', 'Moçambique'), ('Moldávia', 'Moldávia'), ('Mónaco', 'Mónaco'), ('Mongólia', 'Mongólia'), ('Monserrate', 'Monserrate'), ('Montenegro', 'Montenegro'), ('Mundo', 'Mundo'), ('Namíbia', 'Namíbia'), ('Nauru', 'Nauru'), ('Navassa Island', 'Navassa Island'), ('Nepal', 'Nepal'), ('Nicarágua', 'Nicarágua'), ('Níger', 'Níger'), ('Nigéria', 'Nigéria'), ('Niue', 'Niue'), ('Noruega', 'Noruega'), ('Nova Caledónia', 'Nova Caledónia'), ('Nova Zelândia', 'Nova Zelândia'), ('Omã', 'Omã'), ('Pacific Ocean', 'Pacific Ocean'), ('Países Baixos', 'Países Baixos'), ('Palau', 'Palau'), ('Panamá', 'Panamá'), ('Papua-Nova Guiné', 'Papua-Nova Guiné'), ('Paquistão', 'Paquistão'), ('Paracel Islands', 'Paracel Islands'), ('Paraguai', 'Paraguai'), ('Peru', 'Peru'), ('Pitcairn', 'Pitcairn'),
    ('Polinésia Francesa', 'Polinésia Francesa'), ('Polónia', 'Polónia'), ('Porto Rico', 'Porto Rico'), ('Portugal', 'Portugal'), ('Quénia', 'Quénia'), ('Quirguizistão', 'Quirguizistão'), ('Quiribáti', 'Quiribáti'), ('Reino Unido', 'Reino Unido'), ('República Centro-Africana', 'República Centro-Africana'), ('República Checa', 'República Checa'), ('República Dominicana', 'República Dominicana'), ('Roménia', 'Roménia'), ('Ruanda', 'Ruanda'), ('Rússia', 'Rússia'), ('Salvador', 'Salvador'), ('Samoa', 'Samoa'), ('Samoa Americana', 'Samoa Americana'), ('Santa Helena', 'Santa Helena'), ('Santa Lúcia', 'Santa Lúcia'), ('São Bartolomeu', 'São Bartolomeu'), ('São Cristóvão e Neves', 'São Cristóvão e Neves'), ('São Marinho', 'São Marinho'), ('São Martinho', 'São Martinho'), ('São Pedro e Miquelon', 'São Pedro e Miquelon'), ('São Tomé e Príncipe', 'São Tomé e Príncipe'), ('São Vicente e Granadinas', 'São Vicente e Granadinas'), ('Sara Ocidental', 'Sara Ocidental'), ('Seicheles', 'Seicheles'), ('Senegal', 'Senegal'), ('Serra Leoa', 'Serra Leoa'), ('Sérvia', 'Sérvia'), ('Singapura', 'Singapura'), ('Sint Maarten', 'Sint Maarten'), ('Síria', 'Síria'), ('Somália', 'Somália'), ('Southern Ocean', 'Southern Ocean'), ('Spratly Islands', 'Spratly Islands'), ('Sri Lanca', 'Sri Lanca'), ('Suazilândia', 'Suazilândia'), ('Sudão', 'Sudão'), ('Sudão do Sul', 'Sudão do Sul'), ('Suécia', 'Suécia'), ('Suíça', 'Suíça'), ('Suriname', 'Suriname'), ('Svalbard e Jan Mayen', 'Svalbard e Jan Mayen'), ('Tailândia', 'Tailândia'), ('Taiwan', 'Taiwan'), ('Tajiquistão', 'Tajiquistão'), ('Tanzânia', 'Tanzânia'), ('Território Britânico do Oceano Índico', 'Território Britânico do Oceano Índico'), ('Territórios Austrais Franceses', 'Territórios Austrais Franceses'), ('Timor Leste', 'Timor Leste'), ('Togo', 'Togo'), ('Tokelau', 'Tokelau'), ('Tonga', 'Tonga'), ('Trindade e Tobago', 'Trindade e Tobago'), ('Tunísia', 'Tunísia'), ('Turquemenistão', 'Turquemenistão'), ('Turquia', 'Turquia'), ('Tuvalu', 'Tuvalu'), ('Ucrânia', 'Ucrânia'), ('Uganda', 'Uganda'), ('União Europeia', 'União Europeia'), ('Uruguai', 'Uruguai'), ('Usbequistão', 'Usbequistão'), ('Vanuatu', 'Vanuatu'), ('Vaticano', 'Vaticano'), ('Venezuela', 'Venezuela'), ('Vietname', 'Vietname'), ('Wake Island', 'Wake Island'), ('Wallis e Futuna', 'Wallis e Futuna'), ('West Bank', 'West Bank'), ('Zâmbia', 'Zâmbia'), ('Zimbabué', 'Zimbabué')
]
CNH_category_choices        = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E')
]
disableness_choices         = [
    ('Motora', 'Motora'),
    ('Visual', 'Visual'),
    ('Física', 'Física'),
    ('Auditiva', 'Auditiva'),
    ('Mental', 'Mental'),
    ('Intelectual', 'Intelectual'),
    ('Reabilitado', 'Reabilitado')
]
bank_choices                = [
    ('Banco do Brasil', 'Banco do Brasil'), ('Banco Central do Brasil', 'Banco Central do Brasil'), ('Banco da Amazônia', 'Banco da Amazônia'), ('Banco do Nordeste do Brasil', 'Banco do Nordeste do Brasil'), ('Banco Nacional de Desenvolvimento Econômico e Social', 'Banco Nacional de Desenvolvimento Econômico e Social'), ('Caixa Econômica Federal', 'Caixa Econômica Federal'), ('Banco Regional de Desenvolvimento do Extremo Sul', 'Banco Regional de Desenvolvimento do Extremo Sul'), ('Banco de Desenvolvimento de Minas Gerais', 'Banco de Desenvolvimento de Minas Gerais'), ('Banco de Brasília', 'Banco de Brasília'), ('Banco do Estado de Sergipe', 'Banco do Estado de Sergipe'), ('Banco do Estado do Espírito Santo', 'Banco do Estado do Espírito Santo'), ('Banco do Estado do Pará', 'Banco do Estado do Pará'), ('Banco do Estado do Rio Grande do Sul', 'Banco do Estado do Rio Grande do Sul'), ('Banco ABN Amro S.A.', 'Banco ABN Amro S.A.'), ('Banco Alfa', 'Banco Alfa'), ('Banco Banif', 'Banco Banif'), ('Banco BBM', 'Banco BBM'), ('Banco BMG', 'Banco BMG'),
    ('Banco Bonsucesso', 'Banco Bonsucesso'), ('Banco BTG Pactual', 'Banco BTG Pactual'), ('Banco Cacique', 'Banco Cacique'), ('Banco Caixa Geral - Brasil', 'Banco Caixa Geral - Brasil'), ('Banco Citibank', 'Banco Citibank'), ('Banco Credibel', 'Banco Credibel'), ('Banco Credit Suisse', 'Banco Credit Suisse'), ('Banco Fator', 'Banco Fator'), ('Banco Fibra', 'Banco Fibra'), ('Agibank', 'Agibank'), ('Banco Guanabara', 'Banco Guanabara'), ('Banco Industrial do Brasil', 'Banco Industrial do Brasil'), ('Banco Industrial e Comercial', 'Banco Industrial e Comercial'), ('Banco Indusval', 'Banco Indusval'), ('Banco Inter', 'Banco Inter'), ('Banco Itaú BBA', 'Banco Itaú BBA'), ('Banco ItaúBank', 'Banco ItaúBank'), ('Banco Itaucred Financiamentos', 'Banco Itaucred Financiamentos'), ('Banco Mercantil do Brasil', 'Banco Mercantil do Brasil'), ('Banco Modal', 'Banco Modal'), ('Banco Morada', 'Banco Morada'), ('Banco Pan', 'Banco Pan'), ('Banco Paulista', 'Banco Paulista'), ('Banco Pine', 'Banco Pine'), ('Banco Renner', 'Banco Renner'), ('Banco Ribeirão Preto', 'Banco Ribeirão Preto'), ('Banco Safra', 'Banco Safra'), ('Banco Santander', 'Banco Santander'), ('Banco Sofisa', 'Banco Sofisa'),
    ('Banco Topázio', 'Banco Topázio'), ('Banco Votorantim', 'Banco Votorantim'), ('Bradesco', 'Bradesco'), ('Itaú Unibanco', 'Itaú Unibanco'), ('Banco Original', 'Banco Original'), ('Nu Pagamentos S.A', 'Nu Pagamentos S.A')
]
intern_schooling_choices    = [
    ('Fundamental','Fundamental'),
    ('Médio', 'Médio'),
    ('Técnico', 'Técnico'),
    ('Superior', 'Superior')
]
grau_parentesco_choices     = [
    ('Cônjuge', 'Cônjuge'),
    ('Companheiro (a) com o (a) qual tenha filhos ou viva a mais de 05 anos ou possua Declaração de união Estável ','Companheiro (a) com o (a) qual tenha filhos ou viva a mais de 05 anos ou possua Declaração de união Estável '),
    ('Filho(a) ou Enteado(a)','Filho(a) ou Enteado(a)'),
    ('Filho(a) ou Enteado(a), universitario(a) ou cursando escola técnica de 2º Grau','Filho(a) ou Enteado(a), universitario(a) ou cursando escola técnica de 2º Grau'),
    ('Irmão(ã), Neto(a) ou Bisneto(a) sem arrimo dos pais, do(a) qual detenha a guarda judicial ','Irmão(ã), Neto(a) ou Bisneto(a) sem arrimo dos pais, do(a) qual detenha a guarda judicial '),
    ('Irmão(ã), Neto(a) ou Bisneto(a) sem arrimo dos pais, universitário(a) ou cursando escola técnica de 2º Grau do(a) qual detenha Guarda Judicial','Irmão(ã), Neto(a) ou Bisneto(a) sem arrimo dos pais, universitário(a) ou cursando escola técnica de 2º Grau do(a) qual detenha Guarda Judicial'),
    ('Pais, avós e bisavós','Pais, avós e bisavós'),
    ('Menor pobre do qual detenha guarda judicial','Menor pobre do qual detenha guarda judicial'),
    ('A pessoa absolutamente incapaz, do qual seja tutor ou curador','A pessoa absolutamente incapaz, do qual seja tutor ou curador'),
    ('Ex-Cônjuge','Ex-Cônjuge')
]

# Regex Validators
phoneRegex = RegexValidator(
    regex=r'^(\+\d{0,4})?(\(\d{0,3}\))?([0-9\-]{7,15})$',
    message="Entre Telefone no Formato: '(DDD)99999-9999'."
)
# Models --------------------------------------------------------------------------------------------------------------------------------------------

# 1 - Basic Info
class BasicInfo(models.Model):

    id                          =   models.BigAutoField(primary_key = True)

    primeiro_nome               =   models.CharField(max_length = 100)
    ultimo_nome                 =   models.CharField(max_length = 100)
    data_nascimento             =   models.DateField(null = True, blank = True, validators = [utilities.validateNoFutureDates])
    genero                      =   models.CharField(max_length = 200, choices = gender_choices, null = True, blank = True)
    nacionalidade               =   models.CharField(max_length = 200, null = True, blank = True)
    estado_nascimento           =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    municipio_nascimento        =   models.CharField(max_length = 200, null = True, blank = True)
    numero_documento_CPF        =   models.CharField(max_length = 14, validators = [utilities.validateCPF]) # REQUIRED
    numero_inscricao_NIS        =   models.IntegerField(null = True, blank = True)
    numero_PIS_PASEP            =   models.IntegerField(null = True, blank = True)
    numero_NIT_INSS             =   models.IntegerField(null = True, blank = True)
    numero_codigo_NIT           =   models.IntegerField(null = True, blank = True)
    raca_cor                    =   models.CharField(max_length = 200, choices = race_choices, null = True, blank = True)
    nome_completo_mae           =   models.CharField(max_length = 200, null = True, blank = True)
    nome_completo_pai           =   models.CharField(max_length = 200, null = True, blank = True)
    estado_civil                =   models.CharField(max_length = 200, choices = civil_state_choices, null = True, blank = True)
    escolaridade                =   models.CharField(max_length = 200, null = True, blank = True, choices = intern_schooling_choices)

    primeiro_emprego            =   models.BooleanField(null = True, blank = True)
    estrangeiro                 =   models.BooleanField(null = True, blank = True)
    outro_emprego               =   models.BooleanField(null = True, blank = True)
    estagiario                  =   models.BooleanField(null = True, blank = True)
    deficiente                  =   models.BooleanField(null = True, blank = True)

    SEG                         =   models.BooleanField(default = True) # REQUIRED (SEG == True, Eireli == False)
    ativo                       =   models.BooleanField(default = True) # REQUIRED
    ferias                      =   models.BooleanField(default=False)  # REQUIRED
    afastamento                 =   models.BooleanField(default=False)  # REQUIRED

    status                      =   models.CharField(max_length = 100, null = True, blank = True)

    obs_status                  =   models.TextField(null = True, blank = True)
    obs_desligamento            =   models.TextField(null = True, blank = True)

    data_ultima_ativacao        =   models.DateTimeField(null = True, blank = True)
    data_ultima_modificacao     =   models.DateTimeField(null = True, blank = True)
    data_ultimo_desligamento    =   models.DateTimeField(null = True, blank = True)

    @property
    def age(self):
        
        """Get the current age."""
        
        today = date.today() 
        try:  
            birthday = self.data_nascimento.replace(year = today.year)     
        except ValueError:  
            birthday = self.data_nascimento.replace(year = today.year, 
                    month = self.data_nascimento.month + 1, day = 1) 
    
        if birthday > today: 
            return today.year - self.data_nascimento.year - 1
        else: 
            return today.year - self.data_nascimento.year

    def __str__(self):
        return self.primeiro_nome + ' ' + self.ultimo_nome

# 2 - Address Info
class AddressInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True, related_name = "address_info")

    end_residente_exterior      =   models.BooleanField(null = True, blank = True)
    end_geral                   =   models.CharField(max_length = 500, null = True, blank = True)
    end_numero                  =   models.IntegerField(null = True, blank = True)
    end_bairro                  =   models.CharField(max_length = 200, null = True, blank = True)
    end_complemento             =   models.CharField(max_length = 100, null = True, blank = True)
    end_municipio               =   models.CharField(max_length = 200, null = True, blank = True)
    end_estado                  =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    end_CEP                     =   models.CharField(max_length = 9, null = True, blank = True, validators=[utilities.validateCEP])
    end_pais                    =   models.CharField(max_length = 200, choices = country_choices, null = True, blank = True)
    end_residencia_propria      =   models.BooleanField(null = True, blank = True)
    end_comprado_FGTS           =   models.BooleanField(null = True, blank = True)

    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 3 - Documents Info (No Attachments)
class DocumentsInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True, related_name = "documents_info")

    docs_CTPS_numero_geral      =   models.IntegerField(null = True, blank = True)
    docs_CTPS_numero_serie      =   models.IntegerField(null = True, blank = True)
    docs_CTPS_UF                =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_CTPS_data_emissao      =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    docs_TE_numero_geral        =   models.DecimalField(max_digits = 12, decimal_places = 0, null = True, blank = True)
    docs_TE_secao               =   models.CharField(max_length = 10, null = True, blank = True)
    docs_TE_zona                =   models.CharField(max_length = 10, null = True, blank = True)
    docs_RG_numero_geral        =   models.DecimalField(max_digits = 11, decimal_places = 0, null = True, blank = True)
    docs_RG_emissor             =   models.CharField(max_length = 5, null = True, blank = True)
    docs_RG_UF                  =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_RG_data_emissao        =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    docs_RNE_numero_geral       =   models.CharField(max_length = 15, null = True, blank = True)
    docs_RNE_emissor            =   models.CharField(max_length = 5, null = True, blank = True)
    docs_RNE_UF                 =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_RNE_data_emissao       =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    docs_OC_numero_geral        =   models.CharField(max_length = 15, null = True, blank = True)
    docs_OC_emissor             =   models.CharField(max_length = 15, null = True, blank = True)
    docs_OC_UF                  =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_OC_data_emissao        =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    docs_CNH_numero_geral       =   models.CharField(max_length = 15, null = True, blank = True)
    docs_CNH_emissor            =   models.CharField(max_length = 10, null = True, blank = True)
    docs_CNH_UF                 =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_CNH_data_emissao       =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    docs_CNH_categoria          =   models.CharField(max_length = 1, choices = CNH_category_choices, null = True, blank = True)
    docs_CNH_data_primeira      =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    docs_CNH_data_validade      =   models.DateField(null = True, blank = True)

    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 4 - Contact Info
class ContactInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True, related_name = "contact_info")

    cont_tel_fixo               =   models.CharField(validators=[phoneRegex], max_length = 17, null = True, blank = True)
    cont_tel_cel                =   models.CharField(validators=[phoneRegex], max_length = 17, null = True, blank = True)
    cont_email_secundario       =   models.EmailField(null = True, blank = True)
    cont_email_principal        =   models.EmailField(null = True, blank = True)
    
    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 5 - Foreigner Info (If Needed)
class ForeignerInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True, related_name = "foreigner_info")

    estr_data_chegada           =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    estr_naturalizado           =   models.BooleanField(null = True, blank = True)
    estr_data_naturalizacao     =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    estr_casado_brasileiro      =   models.BooleanField(null = True, blank = True)
    estr_filhos_brasileiros     =   models.BooleanField(null = True, blank = True)

    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 6 - Handiccaped Info (If Needed)
class HandicappedInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True, related_name = "handicapped_info")

    deficiencia_tipo            =   models.CharField(max_length = 200, choices = disableness_choices, null = True, blank = True)
    deficiencia_obs             =   models.TextField(null = True, blank = True)

    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 7 - Banking Info
class BankingInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, related_name = "banking_info")

    banco_numero_codigo         =   models.DecimalField(max_digits = 4, decimal_places = 0, null = True, blank = True)
    banco_nome                  =   models.CharField(max_length = 200, choices = bank_choices, null = True, blank = True)
    banco_agencia               =   models.CharField(max_length = 10, null = True, blank = True)
    banco_tipo_conta            =   models.CharField(max_length = 200, choices = [('Corrente', 'C. Corrente'), ('Poupança', 'Poupança')], null = True, blank = True)
    banco_numero_conta_root     =   models.CharField(max_length = 10, null = True, blank = True)

    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 8 - Another Job Info (If Needed)
class AnotherJobInfo(models.Model):

    basicinfo                       =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True, related_name = "another_job")

    vinc_outra_emp_func             =   models.BooleanField(null = True, blank = True)
    vinc_outra_emp_soc              =   models.BooleanField(null = True, blank = True)
    vinc_outra_emp_nome             =   models.CharField(max_length = 300, null = True, blank = True)
    vinc_outra_emp_CNPJ             =   models.CharField(max_length = 18, null = True, blank = True, validators=[utilities.validateCNPJ])
    vinc_outra_emp_salario          =   models.CharField(max_length = 10, null = True, blank = True)
    vinc_outra_emp_nome_soc         =   models.CharField(max_length = 300, null = True, blank = True)
    vinc_outra_emp_CNPJ_soc         =   models.CharField(max_length = 18, null = True, blank = True, validators=[utilities.validateCNPJ])
    vinc_outra_emp_salario_soc      =   models.CharField(max_length = 10, null = True, blank = True)
    vinc_comentarios                =   models.TextField(null = True, blank = True)

    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 9 - Internship Info (If Needed)
class InternInfo(models.Model):

    basicinfo                       =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True, related_name = "intern_info")

    estag_data_inicio               =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    estag_data_fim                  =   models.DateField(null = True, blank = True)
    estag_obrigatorio               =   models.BooleanField(null = True, blank = True)
    estag_escolaridade              =   models.CharField(max_length = 200, choices = intern_schooling_choices, null = True, blank = True)
    estag_area_atuacao              =   models.CharField(max_length = 300, null = True, blank = True)
    estag_valor_bolsa               =   models.CharField(max_length = 10, null = True, blank = True)
    estag_instituto_nome            =   models.CharField(max_length = 200, null = True, blank = True)
    estag_instituto_CNPJ            =   models.CharField(max_length = 18, null = True, blank = True)
    estag_instituto_end             =   models.CharField(max_length = 200, null = True, blank = True)
    estag_instituto_end_numero      =   models.IntegerField(null = True, blank = True)
    estag_instituto_end_municipio   =   models.CharField(max_length = 200, null = True, blank = True)
    estag_instituto_UF              =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    estag_instituto_CEP             =   models.CharField(max_length = 9, null = True, blank = True, validators=[utilities.validateCEP])
    estag_instituto_tel             =   models.CharField(validators=[phoneRegex], max_length = 17, null = True, blank = True)

    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 10 - Contractual Info
class ContractualInfo(models.Model):

    basicinfo                           =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True, related_name = "contractual_info")

    contrat_data_admissao               =   models.DateField(null = True, blank = True, validators=[utilities.validateNoFutureDates])
    contrat_data_inicio                 =   models.DateField(null = True, blank = True)
    contrat_cargo_inicial               =   models.CharField(max_length = 100, null = True, blank = True)
    contrat_vale_alim                   =   models.BooleanField(null = True, blank = True)
    contrat_vale_alim_valor             =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_vale_ref                    =   models.BooleanField(null = True, blank = True)
    contrat_vale_ref_valor              =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_cesta                       =   models.BooleanField(null = True, blank = True)
    contrat_cesta_valor                 =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_vale_comb                   =   models.BooleanField(null = True, blank = True)
    contrat_vale_comb_valor             =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_vale_transp                 =   models.BooleanField(null = True, blank = True)
    contrat_vale_transp_valor           =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_salario_atual               =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_salario_base                =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_funcao_cargo                =   models.CharField(max_length = 100, null = True, blank = True)
    contrat_funcao_nivel                =   models.CharField(max_length = 100, null = True, blank = True)
    contrat_funcao_nivel_inicial        =   models.CharField(max_length = 100, null = True, blank = True)
    contrat_funcao_gestor               =   models.BooleanField(null = True, blank = True)
    contrat_funcao_CBO                  =   models.CharField(max_length = 50, null = True, blank = True)
    contrat_funcao_descricao            =   models.TextField(null = True, blank = True)
    contrat_data_ultima_alteracao_cargo =   models.DateField(null = True, blank = True)

    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 11 - Document File Attachments
class DocumentAttachments(models.Model):

    #   upload_to  =    os.path.join(str(basicinfo.numero_documento_cpf), %Y%m)

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True, related_name = "docscans")

    docscan_picture             =   models.ImageField(upload_to = utilities.funcionario_media_path_PICTURE, null = True, blank = True)
    docscan_CPF                 =   models.ImageField(upload_to = utilities.funcionario_media_path_CPF, null = True, blank = True)
    docscan_TE                  =   models.ImageField(upload_to = utilities.funcionario_media_path_TE, null = True, blank = True)
    docscan_CTPS                =   models.ImageField(upload_to = utilities.funcionario_media_path_CTPS, null = True, blank = True)
    docscan_reservista          =   models.ImageField(upload_to = utilities.funcionario_media_path_RESERVISTA, null = True, blank = True)
    docscan_certidao_nascimento =   models.ImageField(upload_to = utilities.funcionario_media_path_CERTIDAONASCIMENTO, null = True, blank = True)
    docscan_certidao_casamento  =   models.ImageField(upload_to = utilities.funcionario_media_path_CERTIDAOCASAMENTO, null = True, blank = True)
    docscan_comprovante_resid   =   models.ImageField(upload_to = utilities.funcionario_media_path_COMPROVANTERESIDENCIA, null = True, blank = True)
    docscan_comprovante_escolar =   models.ImageField(upload_to = utilities.funcionario_media_path_COMPROVANTEESCOLAR, null = True, blank = True)
    docscan_CV                  =   models.FileField(upload_to  = utilities.funcionario_media_path_CV, null = True, blank = True)

    def __str__(self):
        return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome

# 12 - Dependent Info (If Needed)
class Dependente(models.Model):

    basicinfo                   =   models.ForeignKey(BasicInfo, models.CASCADE)

    grau_parentesco             =   models.CharField(max_length = 500, choices = grau_parentesco_choices, null = True, blank = True)
    nome                        =   models.CharField(max_length = 200, null = True, blank = True)
    data_nascimento             =   models.DateField(null = True, blank = True)
    CPF                         =   models.CharField(max_length = 14, null = True, blank = True)
    docscan_certidao_nascimento =   models.ImageField(upload_to = utilities.funcionario_media_path_CERTIDAONASCIMENTO, null = True, blank = True)
    docscan_CPF                 =   models.ImageField(upload_to = utilities.funcionario_media_path_CPF, null = True, blank = True)
    docscan_vacinacao           =   models.ImageField(upload_to = utilities.funcionario_media_path_VACINACAO, null = True, blank = True)
    docscan_RG                  =   models.ImageField(upload_to = utilities.funcionario_media_path_RG, null = True, blank = True)

    #def __str__(self):
    #    return self.basicinfo.primeiro_nome + ' ' + self.basicinfo.ultimo_nome + ' - ' + self.nome