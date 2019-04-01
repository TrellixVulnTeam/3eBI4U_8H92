from django.db import models
from django.core.validators import RegexValidator
from .utilities import (
    validateCPF, validateRG, funcionario_media_path_CERTIDAOCASAMENTO,
    funcionario_media_path_CERTIDAONASCIMENTO, funcionario_media_path_COMPROVANTEESCOLAR,
    funcionario_media_path_CPF, funcionario_media_path_TE, funcionario_media_path_CTPS, funcionario_media_path_RESERVISTA,
    funcionario_media_path_CV, funcionario_media_path_COMPROVANTERESIDENCIA, funcionario_media_path_VACINACAO, funcionario_media_path_RG,
    funcionario_media_path_PICTURE)

# App Logic ------------------------------------------------------------------------------------------------------------------------------------------

# Choice Fields Lists
brazilian_states_choices    = [
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
]
race_choices                = [
    ('INDIGENA', 'Indigena'), ('BRANCA', 'Branca'), ('NEGRA', 'Negra'), ('AMARELA', 'Amarela'), ('PARDA', 'Parda'), ('NAO_INFORMADO', 'Prefiro Não Informar')
]
gender_choices              = [
    ('MASCULINO', 'Masculino'), ('FEMININO', 'Feminino'), ('OUTRO', 'Outro'), ('NAO_INFORMADO', 'Prefiro Não Informar')
]
civil_state_choices         = [
    ('CASADO', 'Casado(a)'), ('SOLTEIRO', 'Solteiro(a)'), ('VIUVO', 'Viuvo(a)'), ('DIVORCIADO', 'Divorciado(a)')
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
    ('Fisica', 'Fisica'),
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
position_choices            = [
    ('Supervisor 1', 'Supervisor 1'),
    ('Supervisor 2', 'Supervisor 2'),
    ('Supervisor 3', 'Supervisor 3'),
    ('Seguranca 1', 'Seguranca 1'),
    ('Seguranca 2', 'Seguranca 2'),
    ('Seguranca 3', 'Seguranca 3'),
    ('Aux Limpeza', 'Aux Limpeza'),
    ('Aux administrativo', 'Aux administrativo'),
    ('Gerente', 'Gerente'),
    ('Diretor', 'Diretor')
]
grau_parentesco_choices     = [
    ('1', 'Cônjuge'),
    ('2','Companheiro (a) com o (a) qual tenha filhos ou viva a mais de 05 anos ou possua Declaração de união Estável '),
    ('3','Filho(a) ou Enteado(a)'),
    ('4','Filho(a) ou Enteado(a), universitario(a) ou cursando escola técnica de 2º Grau'),
    ('5','Irmão(ã), Neto(a) ou Bisneto(a) sem arrimo dos pais, do(a) qual detenha a guarda judicial '),
    ('6','Irmão(ã), Neto(a) ou Bisneto(a) sem arrimo dos pais, universitário(a) ou cursando escola técnica de 2º Grau do(a) qual detenha Guarda Judicial'),
    ('7','Pais, avós e bisavós'),
    ('8','Menor pobre do qual detenha guarda judicial'),
    ('9','A pessoa absolutamente incapaz, do qual seja tutor ou curador'),
    ('10','Ex-Cônjuge')
]

# Regex Validators 
phoneRegex = RegexValidator(
    regex=r'^(\+\d{0,4})?(\(\d{0,3}\))?([0-9\-]{7,15})$',
    message="Entre Telefone no Formato: '+99(99)999999999'."
)

# Models --------------------------------------------------------------------------------------------------------------------------------------------

# 1 - Basic Info
class BasicInfo(models.Model):

    id                          =   models.BigAutoField(primary_key = True)

    primeiro_nome               =   models.CharField(max_length = 100, null = True, blank = True)
    ultimo_nome                 =   models.CharField(max_length = 100, null = True, blank = True)
    data_nascimento             =   models.DateField(null = True, blank = True)
    genero                      =   models.CharField(max_length = 200, choices = gender_choices, null = True, blank = True)
    nacionalidade               =   models.CharField(max_length = 200, null = True, blank = True)
    estado_nascimento           =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    municipio_nascimento        =   models.CharField(max_length = 200, null = True, blank = True)
    numero_documento_CPF        =   models.CharField(max_length = 14, validators = [validateCPF], null = True, blank = True)
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

    ativo                       =   models.BooleanField(default = True)
    obs_desligamento            =   models.TextField(null = True, blank = True)

# 2 - Address Info
class AddressInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    end_residente_exterior      =   models.BooleanField(null = True, blank = True)
    end_geral                   =   models.CharField(max_length = 500, null = True, blank = True)
    end_numero                  =   models.IntegerField(null = True, blank = True)
    end_bairro                  =   models.CharField(max_length = 200, null = True, blank = True)
    end_complemento             =   models.CharField(max_length = 100, null = True, blank = True)
    end_municipio               =   models.CharField(max_length = 200, null = True, blank = True)
    end_estado                  =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    end_CEP                     =   models.CharField(max_length = 9, null = True, blank = True)
    end_pais                    =   models.CharField(max_length = 200, choices = country_choices, null = True, blank = True)
    end_residencia_propria      =   models.BooleanField(null = True, blank = True)
    end_comprado_FGTS           =   models.BooleanField(null = True, blank = True)

# 3 - Documents Info (No Attachments)
class DocumentsInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    docs_CTPS_numero_geral      =   models.IntegerField(null = True, blank = True)
    docs_CTPS_numero_serie      =   models.IntegerField(null = True, blank = True)
    docs_CTPS_UF                =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_CTPS_data_emissao      =   models.DateField(null = True, blank = True)
    docs_TE_numero_geral        =   models.DecimalField(max_digits = 12, decimal_places = 0, null = True, blank = True)
    docs_TE_secao               =   models.CharField(max_length = 10, null = True, blank = True)
    docs_TE_zona                =   models.CharField(max_length = 10, null = True, blank = True)
    docs_RG_numero_geral        =   models.DecimalField(max_digits = 11, decimal_places = 0, null = True, blank = True)
    docs_RG_emissor             =   models.CharField(max_length = 5, null = True, blank = True)
    docs_RG_UF                  =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_RG_data_emissao        =   models.DateField(null = True, blank = True)
    docs_RNE_numero_geral       =   models.CharField(max_length = 15, null = True, blank = True)
    docs_RNE_emissor            =   models.CharField(max_length = 5, null = True, blank = True)
    docs_RNE_UF                 =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_RNE_data_emissao       =   models.DateField(null = True, blank = True)
    docs_OC_numero_geral        =   models.CharField(max_length = 15, null = True, blank = True)
    docs_OC_emissor             =   models.CharField(max_length = 15, null = True, blank = True)
    docs_OC_UF                  =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_OC_data_emissao        =   models.DateField(null = True, blank = True)
    docs_CNH_numero_geral       =   models.CharField(max_length = 15, null = True, blank = True)
    docs_CNH_emissor            =   models.CharField(max_length = 10, null = True, blank = True)
    docs_CNH_UF                 =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    docs_CNH_data_emissao       =   models.DateField(null = True, blank = True)
    docs_CNH_categoria          =   models.CharField(max_length = 1, choices = CNH_category_choices, null = True, blank = True)
    docs_CNH_data_primeira      =   models.DateField(null = True, blank = True)
    docs_CNH_data_validade      =   models.DateField(null = True, blank = True) 

# 4 - Contact Info
class ContactInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    cont_tel_fixo               =   models.CharField(validators=[phoneRegex], max_length = 17, null = True, blank = True)
    cont_tel_cel                =   models.CharField(validators=[phoneRegex], max_length = 17, null = True, blank = True)
    cont_tel_recado             =   models.CharField(validators=[phoneRegex], max_length = 17, null = True, blank = True)
    cont_email                  =   models.EmailField(null = True, blank = True)

# 5 - Foreigner Info (If Needed)
class ForeignerInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    estr_data_chegada           =   models.DateField(null = True, blank = True)
    estr_naturalizado           =   models.BooleanField(null = True, blank = True)
    estr_data_naturalizacao     =   models.DateField(null = True, blank = True)
    estr_casado_brasileiro      =   models.BooleanField(null = True, blank = True)
    estr_filhos_brasileiros     =   models.BooleanField(null = True, blank = True)

# 6 - Handiccaped Info (If Needed)
class HandicappedInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    deficiencia_tipo            =   models.CharField(max_length = 200, choices = disableness_choices, null = True, blank = True)
    deficiencia_obs             =   models.CharField(max_length = 3000, null = True, blank = True)

# 7 - Banking Info
class BankingInfo(models.Model):

    id                          =   models.BigAutoField(primary_key = True)

    basicinfo                   =   models.ForeignKey(BasicInfo, models.CASCADE)

    banco_numero_codigo         =   models.DecimalField(max_digits = 4, decimal_places = 0, null = True, blank = True)
    banco_nome                  =   models.CharField(max_length = 200, choices = bank_choices, null = True, blank = True)
    banco_agencia               =   models.IntegerField(null = True, blank = True)
    banco_tipo_conta            =   models.CharField(max_length = 200, choices = [('Corrente', 'CC'), ('Poupança', 'CP')], null = True, blank = True)
    banco_numero_conta_root     =   models.CharField(max_length = 10, null = True, blank = True)

# 8 - Another Job Info (If Needed)
class AnotherJobInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    vinc_outra_emp_func         =   models.BooleanField(null = True, blank = True)
    vinc_outra_emp_soc          =   models.BooleanField(null = True, blank = True)
    vinc_outra_emp_nome         =   models.CharField(max_length = 300, null = True, blank = True)
    vinc_outra_emp_CNPJ         =   models.DecimalField(max_digits = 14, decimal_places = 0, null = True, blank = True)
    vinc_outra_emp_salario      =   models.DecimalField(max_digits = 10, decimal_places=2, null = True, blank = True)       
    vinc_comentarios            =   models.CharField(max_length = 3000, null = True, blank = True)

# 9 - Internship Info (If Needed)
class InternInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    estag_data_inicio           =   models.DateField(null = True, blank = True)
    estag_data_fim              =   models.DateField(null = True, blank = True)
    estag_obrigatorio           =   models.BooleanField(null = True, blank = True)
    estag_escolaridade          =   models.CharField(max_length = 200, choices = intern_schooling_choices, null = True, blank = True)
    estag_area_atuacao          =   models.CharField(max_length = 300, null = True, blank = True)
    estag_valor_bolsa           =   models.DecimalField(max_digits = 10, decimal_places=2, null = True, blank = True)
    estag_instituto_nome        =   models.CharField(max_length = 200, null = True, blank = True)
    estag_instituto_CNPJ        =   models.CharField(max_length = 18, null = True, blank = True)
    estag_instituto_end         =   models.CharField(max_length = 200, null = True, blank = True)
    estag_instituto_UF          =   models.CharField(max_length = 2, choices = brazilian_states_choices, null = True, blank = True)
    estag_instituto_CEP         =   models.CharField(max_length = 9, null = True, blank = True)
    estag_instituto_tel         =   models.CharField(validators=[phoneRegex], max_length = 17, null = True, blank = True)

# 10 - Position Info
class PositionInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    funcao_cargo                =   models.CharField(max_length = 200, choices = position_choices, null = True, blank = True)
    funcao_nivel                =   models.CharField(max_length = 1, choices = [('1','1'), ('2','2'), ('3','3')], null = True, blank = True)
    funcao_gestor               =   models.BooleanField(null = True, blank = True)
    funcao_CBO                  =   models.CharField(max_length = 50, null = True, blank = True)
    funcao_descricao            =   models.CharField(max_length = 3000, null = True, blank = True)

# 11 - Contractual Info
class ContractualInfo(models.Model):

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    contrat_data_admissao       =   models.DateField(null = True, blank = True)
    contrat_data_inicio         =   models.DateField(null = True, blank = True)
    contrat_cargo_inicial       =   models.CharField(max_length = 200, choices = position_choices, null = True, blank = True)
    contrat_vale_alim           =   models.BooleanField(null = True, blank = True)
    contrat_vale_alim_valor     =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_vale_ref            =   models.BooleanField(null = True, blank = True)
    contrat_vale_ref_valor      =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_cesta               =   models.BooleanField(null = True, blank = True)
    contrat_cesta_valor         =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_vale_comb           =   models.BooleanField(null = True, blank = True)
    contrat_vale_comb_valor     =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_vale_transp         =   models.BooleanField(null = True, blank = True)
    contrat_vale_transp_valor   =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_salario_atual       =   models.CharField(max_length = 20, null = True, blank = True)
    contrat_salario_base        =   models.CharField(max_length = 20, null = True, blank = True)

# 12 - Document File Attachments
class DocumentAttachments(models.Model):

    #   upload_to  =    os.path.join(str(basicinfo.numero_documento_cpf), %Y%m)

    basicinfo                   =   models.OneToOneField(BasicInfo, models.CASCADE, primary_key = True)

    docscan_picture             =   models.ImageField(upload_to = funcionario_media_path_PICTURE, null = True, blank = True)
    docscan_CPF                 =   models.ImageField(upload_to = funcionario_media_path_CPF, null = True, blank = True)
    docscan_TE                  =   models.ImageField(upload_to = funcionario_media_path_TE, null = True, blank = True)
    docscan_CTPS                =   models.ImageField(upload_to = funcionario_media_path_CTPS, null = True, blank = True)   
    docscan_reservista          =   models.ImageField(upload_to = funcionario_media_path_RESERVISTA, null = True, blank = True)   
    docscan_certidao_nascimento =   models.ImageField(upload_to = funcionario_media_path_CERTIDAONASCIMENTO, null = True, blank = True)   
    docscan_certidao_casamento  =   models.ImageField(upload_to = funcionario_media_path_CERTIDAOCASAMENTO, null = True, blank = True)   
    docscan_comprovante_resid   =   models.ImageField(upload_to = funcionario_media_path_COMPROVANTERESIDENCIA, null = True, blank = True)   
    docscan_comprovante_escolar =   models.ImageField(upload_to = funcionario_media_path_COMPROVANTEESCOLAR, null = True, blank = True)   
    docscan_CV                  =   models.FileField(upload_to  = funcionario_media_path_CV, null = True, blank = True)

# 13 - Dependent Info (If Needed)
class Dependente(models.Model):

    basicinfo                   =   models.ForeignKey(BasicInfo, models.CASCADE)

    grau_parentesco             =   models.CharField(max_length = 200, choices = grau_parentesco_choices, null = True, blank = True)
    nome                        =   models.CharField(max_length = 200, null = True, blank = True)
    data_nascimento             =   models.DateField(null = True, blank = True)
    CPF                         =   models.CharField(max_length = 11, null = True, blank = True)
    docscan_certidao_nascimento =   models.ImageField(upload_to = funcionario_media_path_CERTIDAONASCIMENTO, null = True, blank = True)   
    docscan_CPF                 =   models.ImageField(upload_to = funcionario_media_path_CPF, null = True, blank = True)
    docscan_vacinacao           =   models.ImageField(upload_to = funcionario_media_path_VACINACAO, null = True, blank = True)
    docscan_RG                  =   models.ImageField(upload_to = funcionario_media_path_RG, null = True, blank = True)

