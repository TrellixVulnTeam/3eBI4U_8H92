# Generated by Django 2.1.7 on 2019-04-12 17:50

import Cliente.utilities
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankingInfo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('banco_numero_codigo', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('banco_nome', models.CharField(blank=True, choices=[('Banco do Brasil', 'Banco do Brasil'), ('Banco Central do Brasil', 'Banco Central do Brasil'), ('Banco da Amazônia', 'Banco da Amazônia'), ('Banco do Nordeste do Brasil', 'Banco do Nordeste do Brasil'), ('Banco Nacional de Desenvolvimento Econômico e Social', 'Banco Nacional de Desenvolvimento Econômico e Social'), ('Caixa Econômica Federal', 'Caixa Econômica Federal'), ('Banco Regional de Desenvolvimento do Extremo Sul', 'Banco Regional de Desenvolvimento do Extremo Sul'), ('Banco de Desenvolvimento de Minas Gerais', 'Banco de Desenvolvimento de Minas Gerais'), ('Banco de Brasília', 'Banco de Brasília'), ('Banco do Estado de Sergipe', 'Banco do Estado de Sergipe'), ('Banco do Estado do Espírito Santo', 'Banco do Estado do Espírito Santo'), ('Banco do Estado do Pará', 'Banco do Estado do Pará'), ('Banco do Estado do Rio Grande do Sul', 'Banco do Estado do Rio Grande do Sul'), ('Banco ABN Amro S.A.', 'Banco ABN Amro S.A.'), ('Banco Alfa', 'Banco Alfa'), ('Banco Banif', 'Banco Banif'), ('Banco BBM', 'Banco BBM'), ('Banco BMG', 'Banco BMG'), ('Banco Bonsucesso', 'Banco Bonsucesso'), ('Banco BTG Pactual', 'Banco BTG Pactual'), ('Banco Cacique', 'Banco Cacique'), ('Banco Caixa Geral - Brasil', 'Banco Caixa Geral - Brasil'), ('Banco Citibank', 'Banco Citibank'), ('Banco Credibel', 'Banco Credibel'), ('Banco Credit Suisse', 'Banco Credit Suisse'), ('Banco Fator', 'Banco Fator'), ('Banco Fibra', 'Banco Fibra'), ('Agibank', 'Agibank'), ('Banco Guanabara', 'Banco Guanabara'), ('Banco Industrial do Brasil', 'Banco Industrial do Brasil'), ('Banco Industrial e Comercial', 'Banco Industrial e Comercial'), ('Banco Indusval', 'Banco Indusval'), ('Banco Inter', 'Banco Inter'), ('Banco Itaú BBA', 'Banco Itaú BBA'), ('Banco ItaúBank', 'Banco ItaúBank'), ('Banco Itaucred Financiamentos', 'Banco Itaucred Financiamentos'), ('Banco Mercantil do Brasil', 'Banco Mercantil do Brasil'), ('Banco Modal', 'Banco Modal'), ('Banco Morada', 'Banco Morada'), ('Banco Pan', 'Banco Pan'), ('Banco Paulista', 'Banco Paulista'), ('Banco Pine', 'Banco Pine'), ('Banco Renner', 'Banco Renner'), ('Banco Ribeirão Preto', 'Banco Ribeirão Preto'), ('Banco Safra', 'Banco Safra'), ('Banco Santander', 'Banco Santander'), ('Banco Sofisa', 'Banco Sofisa'), ('Banco Topázio', 'Banco Topázio'), ('Banco Votorantim', 'Banco Votorantim'), ('Bradesco', 'Bradesco'), ('Itaú Unibanco', 'Itaú Unibanco'), ('Banco Original', 'Banco Original'), ('Nu Pagamentos S.A', 'Nu Pagamentos S.A')], max_length=200, null=True)),
                ('banco_agencia', models.IntegerField(blank=True, null=True)),
                ('banco_tipo_conta', models.CharField(blank=True, choices=[('Corrente', 'C. Corrente'), ('Poupança', 'Poupança')], max_length=200, null=True)),
                ('banco_numero_conta_root', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BasicInfo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('primeiro_nome', models.CharField(blank=True, max_length=100, null=True)),
                ('ultimo_nome', models.CharField(blank=True, max_length=100, null=True)),
                ('data_nascimento', models.DateField(blank=True, null=True, validators=[Cliente.utilities.validateNoFutureDates])),
                ('genero', models.CharField(blank=True, choices=[('MASCULINO', 'Masculino'), ('FEMININO', 'Feminino'), ('OUTRO', 'Outro'), ('NAO_INFORMADO', 'Prefiro Não Informar')], max_length=200, null=True)),
                ('nacionalidade', models.CharField(blank=True, max_length=200, null=True)),
                ('estado_nascimento', models.CharField(blank=True, choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, null=True)),
                ('municipio_nascimento', models.CharField(blank=True, max_length=200, null=True)),
                ('numero_documento_CPF', models.CharField(error_messages={'unique': 'CPF Já Registrado'}, max_length=14, validators=[Cliente.utilities.validateCPF])),
                ('numero_inscricao_NIS', models.IntegerField(blank=True, null=True)),
                ('numero_PIS_PASEP', models.IntegerField(blank=True, null=True)),
                ('numero_NIT_INSS', models.IntegerField(blank=True, null=True)),
                ('numero_codigo_NIT', models.IntegerField(blank=True, null=True)),
                ('raca_cor', models.CharField(blank=True, choices=[('INDIGENA', 'Indigena'), ('BRANCA', 'Branca'), ('NEGRA', 'Negra'), ('AMARELA', 'Amarela'), ('PARDA', 'Parda'), ('NAO_INFORMADO', 'Prefiro Não Informar')], max_length=200, null=True)),
                ('nome_completo_mae', models.CharField(blank=True, max_length=200, null=True)),
                ('nome_completo_pai', models.CharField(blank=True, max_length=200, null=True)),
                ('estado_civil', models.CharField(blank=True, choices=[('CASADO', 'Casado(a)'), ('SOLTEIRO', 'Solteiro(a)'), ('VIUVO', 'Viuvo(a)'), ('DIVORCIADO', 'Divorciado(a)'), ('UNIAO ESTAVEL', 'União Estável')], max_length=200, null=True)),
                ('escolaridade', models.CharField(blank=True, choices=[('Fundamental', 'Fundamental'), ('Médio', 'Médio'), ('Técnico', 'Técnico'), ('Superior', 'Superior')], max_length=200, null=True)),
                ('primeiro_emprego', models.BooleanField(blank=True, null=True)),
                ('estrangeiro', models.BooleanField(blank=True, null=True)),
                ('outro_emprego', models.BooleanField(blank=True, null=True)),
                ('estagiario', models.BooleanField(blank=True, null=True)),
                ('deficiente', models.BooleanField(blank=True, null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('ferias', models.BooleanField(default=False)),
                ('obs_desligamento', models.TextField(blank=True, null=True)),
                ('data_ultima_ativacao', models.DateTimeField(blank=True, null=True)),
                ('data_ultima_modificacao', models.DateTimeField(blank=True, null=True)),
                ('data_ultimo_desligamento', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AddressInfo',
            fields=[
                ('basicinfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Cliente.BasicInfo')),
                ('end_residente_exterior', models.BooleanField(blank=True, null=True)),
                ('end_geral', models.CharField(blank=True, max_length=500, null=True)),
                ('end_numero', models.IntegerField(blank=True, null=True)),
                ('end_bairro', models.CharField(blank=True, max_length=200, null=True)),
                ('end_complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('end_municipio', models.CharField(blank=True, max_length=200, null=True)),
                ('end_estado', models.CharField(blank=True, choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, null=True)),
                ('end_CEP', models.CharField(blank=True, max_length=9, null=True, validators=[Cliente.utilities.validateCEP])),
                ('end_pais', models.CharField(blank=True, choices=[('Afeganistão', 'Afeganistão'), ('África do Sul', 'África do Sul'), ('Akrotiri', 'Akrotiri'), ('Albânia', 'Albânia'), ('Alemanha', 'Alemanha'), ('Andorra', 'Andorra'), ('Angola', 'Angola'), ('Anguila', 'Anguila'), ('Antárctida', 'Antárctida'), ('Antígua e Barbuda', 'Antígua e Barbuda'), ('Arábia Saudita', 'Arábia Saudita'), ('Arctic Ocean', 'Arctic Ocean'), ('Argélia', 'Argélia'), ('Argentina', 'Argentina'), ('Arménia', 'Arménia'), ('Aruba', 'Aruba'), ('Ashmore and Cartier Islands', 'Ashmore and Cartier Islands'), ('Atlantic Ocean', 'Atlantic Ocean'), ('Austrália', 'Austrália'), ('Áustria', 'Áustria'), ('Azerbaijão', 'Azerbaijão'), ('Baamas', 'Baamas'), ('Bangladeche', 'Bangladeche'), ('Barbados', 'Barbados'), ('Barém', 'Barém'), ('Bélgica', 'Bélgica'), ('Belize', 'Belize'), ('Benim', 'Benim'), ('Bermudas', 'Bermudas'), ('Bielorrússia', 'Bielorrússia'), ('Birmânia', 'Birmânia'), ('Bolívia', 'Bolívia'), ('Bósnia e Herzegovina', 'Bósnia e Herzegovina'), ('Botsuana', 'Botsuana'), ('Brasil', 'Brasil'), ('Brunei', 'Brunei'), ('Bulgária', 'Bulgária'), ('Burquina Faso', 'Burquina Faso'), ('Burúndi', 'Burúndi'), ('Butão', 'Butão'), ('Cabo Verde', 'Cabo Verde'), ('Camarões', 'Camarões'), ('Camboja', 'Camboja'), ('Canadá', 'Canadá'), ('Catar', 'Catar'), ('Cazaquistão', 'Cazaquistão'), ('Chade', 'Chade'), ('Chile', 'Chile'), ('China', 'China'), ('Chipre', 'Chipre'), ('Clipperton Island', 'Clipperton Island'), ('Colômbia', 'Colômbia'), ('Comores', 'Comores'), ('Congo-Brazzaville', 'Congo-Brazzaville'), ('Congo-Kinshasa', 'Congo-Kinshasa'), ('Coral Sea Islands', 'Coral Sea Islands'), ('Coreia do Norte', 'Coreia do Norte'), ('Coreia do Sul', 'Coreia do Sul'), ('Costa do Marfim', 'Costa do Marfim'), ('Costa Rica', 'Costa Rica'), ('Croácia', 'Croácia'), ('Cuba', 'Cuba'), ('Curacao', 'Curacao'), ('Dhekelia', 'Dhekelia'), ('Dinamarca', 'Dinamarca'), ('Domínica', 'Domínica'), ('Egipto', 'Egipto'), ('Emiratos Árabes Unidos', 'Emiratos Árabes Unidos'), ('Equador', 'Equador'), ('Eritreia', 'Eritreia'), ('Eslováquia', 'Eslováquia'), ('Eslovénia', 'Eslovénia'), ('Espanha', 'Espanha'), ('Estados Unidos', 'Estados Unidos'), ('Estónia', 'Estónia'), ('Etiópia', 'Etiópia'), ('Faroé', 'Faroé'), ('Fiji', 'Fiji'), ('Filipinas', 'Filipinas'), ('Finlândia', 'Finlândia'), ('França', 'França'), ('Gabão', 'Gabão'), ('Gâmbia', 'Gâmbia'), ('Gana', 'Gana'), ('Gaza Strip', 'Gaza Strip'), ('Geórgia', 'Geórgia'), ('Geórgia do Sul e Sandwich do Sul', 'Geórgia do Sul e Sandwich do Sul'), ('Gibraltar', 'Gibraltar'), ('Granada', 'Granada'), ('Grécia', 'Grécia'), ('Gronelândia', 'Gronelândia'), ('Guame', 'Guame'), ('Guatemala', 'Guatemala'), ('Guernsey', 'Guernsey'), ('Guiana', 'Guiana'), ('Guiné', 'Guiné'), ('Guiné Equatorial', 'Guiné Equatorial'), ('Guiné-Bissau', 'Guiné-Bissau'), ('Haiti', 'Haiti'), ('Honduras', 'Honduras'), ('Hong Kong', 'Hong Kong'), ('Hungria', 'Hungria'), ('Iémen', 'Iémen'), ('Ilha Bouvet', 'Ilha Bouvet'), ('Ilha do Natal', 'Ilha do Natal'), ('Ilha Norfolk', 'Ilha Norfolk'), ('Ilhas Caimão', 'Ilhas Caimão'), ('Ilhas Cook', 'Ilhas Cook'), ('Ilhas dos Cocos', 'Ilhas dos Cocos'), ('Ilhas Falkland', 'Ilhas Falkland'), ('Ilhas Heard e McDonald', 'Ilhas Heard e McDonald'), ('Ilhas Marshall', 'Ilhas Marshall'), ('Ilhas Salomão', 'Ilhas Salomão'), ('Ilhas Turcas e Caicos', 'Ilhas Turcas e Caicos'), ('Ilhas Virgens Americanas', 'Ilhas Virgens Americanas'), ('Ilhas Virgens Britânicas', 'Ilhas Virgens Britânicas'), ('Índia', 'Índia'), ('Indian Ocean', 'Indian Ocean'), ('Indonésia', 'Indonésia'), ('Irão', 'Irão'), ('Iraque', 'Iraque'), ('Irlanda', 'Irlanda'), ('Islândia', 'Islândia'), ('Israel', 'Israel'), ('Itália', 'Itália'), ('Jamaica', 'Jamaica'), ('Jan Mayen', 'Jan Mayen'), ('Japão', 'Japão'), ('Jersey', 'Jersey'), ('Jibuti', 'Jibuti'), ('Jordânia', 'Jordânia'), ('Kosovo', 'Kosovo'), ('Kuwait', 'Kuwait'), ('Laos', 'Laos'), ('Lesoto', 'Lesoto'), ('Letónia', 'Letónia'), ('Líbano', 'Líbano'), ('Libéria', 'Libéria'), ('Líbia', 'Líbia'), ('Listenstaine', 'Listenstaine'), ('Lituânia', 'Lituânia'), ('Luxemburgo', 'Luxemburgo'), ('Macau', 'Macau'), ('Macedónia', 'Macedónia'), ('Madagáscar', 'Madagáscar'), ('Malásia', 'Malásia'), ('Malávi', 'Malávi'), ('Maldivas', 'Maldivas'), ('Mali', 'Mali'), ('Malta', 'Malta'), ('Man, Isle of', 'Man, Isle of'), ('Marianas do Norte', 'Marianas do Norte'), ('Marrocos', 'Marrocos'), ('Maurícia', 'Maurícia'), ('Mauritânia', 'Mauritânia'), ('México', 'México'), ('Micronésia', 'Micronésia'), ('Moçambique', 'Moçambique'), ('Moldávia', 'Moldávia'), ('Mónaco', 'Mónaco'), ('Mongólia', 'Mongólia'), ('Monserrate', 'Monserrate'), ('Montenegro', 'Montenegro'), ('Mundo', 'Mundo'), ('Namíbia', 'Namíbia'), ('Nauru', 'Nauru'), ('Navassa Island', 'Navassa Island'), ('Nepal', 'Nepal'), ('Nicarágua', 'Nicarágua'), ('Níger', 'Níger'), ('Nigéria', 'Nigéria'), ('Niue', 'Niue'), ('Noruega', 'Noruega'), ('Nova Caledónia', 'Nova Caledónia'), ('Nova Zelândia', 'Nova Zelândia'), ('Omã', 'Omã'), ('Pacific Ocean', 'Pacific Ocean'), ('Países Baixos', 'Países Baixos'), ('Palau', 'Palau'), ('Panamá', 'Panamá'), ('Papua-Nova Guiné', 'Papua-Nova Guiné'), ('Paquistão', 'Paquistão'), ('Paracel Islands', 'Paracel Islands'), ('Paraguai', 'Paraguai'), ('Peru', 'Peru'), ('Pitcairn', 'Pitcairn'), ('Polinésia Francesa', 'Polinésia Francesa'), ('Polónia', 'Polónia'), ('Porto Rico', 'Porto Rico'), ('Portugal', 'Portugal'), ('Quénia', 'Quénia'), ('Quirguizistão', 'Quirguizistão'), ('Quiribáti', 'Quiribáti'), ('Reino Unido', 'Reino Unido'), ('República Centro-Africana', 'República Centro-Africana'), ('República Checa', 'República Checa'), ('República Dominicana', 'República Dominicana'), ('Roménia', 'Roménia'), ('Ruanda', 'Ruanda'), ('Rússia', 'Rússia'), ('Salvador', 'Salvador'), ('Samoa', 'Samoa'), ('Samoa Americana', 'Samoa Americana'), ('Santa Helena', 'Santa Helena'), ('Santa Lúcia', 'Santa Lúcia'), ('São Bartolomeu', 'São Bartolomeu'), ('São Cristóvão e Neves', 'São Cristóvão e Neves'), ('São Marinho', 'São Marinho'), ('São Martinho', 'São Martinho'), ('São Pedro e Miquelon', 'São Pedro e Miquelon'), ('São Tomé e Príncipe', 'São Tomé e Príncipe'), ('São Vicente e Granadinas', 'São Vicente e Granadinas'), ('Sara Ocidental', 'Sara Ocidental'), ('Seicheles', 'Seicheles'), ('Senegal', 'Senegal'), ('Serra Leoa', 'Serra Leoa'), ('Sérvia', 'Sérvia'), ('Singapura', 'Singapura'), ('Sint Maarten', 'Sint Maarten'), ('Síria', 'Síria'), ('Somália', 'Somália'), ('Southern Ocean', 'Southern Ocean'), ('Spratly Islands', 'Spratly Islands'), ('Sri Lanca', 'Sri Lanca'), ('Suazilândia', 'Suazilândia'), ('Sudão', 'Sudão'), ('Sudão do Sul', 'Sudão do Sul'), ('Suécia', 'Suécia'), ('Suíça', 'Suíça'), ('Suriname', 'Suriname'), ('Svalbard e Jan Mayen', 'Svalbard e Jan Mayen'), ('Tailândia', 'Tailândia'), ('Taiwan', 'Taiwan'), ('Tajiquistão', 'Tajiquistão'), ('Tanzânia', 'Tanzânia'), ('Território Britânico do Oceano Índico', 'Território Britânico do Oceano Índico'), ('Territórios Austrais Franceses', 'Territórios Austrais Franceses'), ('Timor Leste', 'Timor Leste'), ('Togo', 'Togo'), ('Tokelau', 'Tokelau'), ('Tonga', 'Tonga'), ('Trindade e Tobago', 'Trindade e Tobago'), ('Tunísia', 'Tunísia'), ('Turquemenistão', 'Turquemenistão'), ('Turquia', 'Turquia'), ('Tuvalu', 'Tuvalu'), ('Ucrânia', 'Ucrânia'), ('Uganda', 'Uganda'), ('União Europeia', 'União Europeia'), ('Uruguai', 'Uruguai'), ('Usbequistão', 'Usbequistão'), ('Vanuatu', 'Vanuatu'), ('Vaticano', 'Vaticano'), ('Venezuela', 'Venezuela'), ('Vietname', 'Vietname'), ('Wake Island', 'Wake Island'), ('Wallis e Futuna', 'Wallis e Futuna'), ('West Bank', 'West Bank'), ('Zâmbia', 'Zâmbia'), ('Zimbabué', 'Zimbabué')], max_length=200, null=True)),
                ('end_residencia_propria', models.BooleanField(blank=True, null=True)),
                ('end_comprado_FGTS', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('basicinfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Cliente.BasicInfo')),
                ('cont_tel_fixo', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Entre Telefone no Formato: '(DDD)99999-9999'.", regex='^(\\+\\d{0,4})?(\\(\\d{0,3}\\))?([0-9\\-]{7,15})$')])),
                ('cont_tel_cel', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Entre Telefone no Formato: '(DDD)99999-9999'.", regex='^(\\+\\d{0,4})?(\\(\\d{0,3}\\))?([0-9\\-]{7,15})$')])),
                ('cont_tel_recado', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Entre Telefone no Formato: '(DDD)99999-9999'.", regex='^(\\+\\d{0,4})?(\\(\\d{0,3}\\))?([0-9\\-]{7,15})$')])),
                ('cont_email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContractualInfo',
            fields=[
                ('basicinfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Cliente.BasicInfo')),
                ('contrat_data_admissao', models.DateField(blank=True, null=True, validators=[Cliente.utilities.validateNoFutureDates])),
                ('contrat_data_inicio', models.DateField(blank=True, null=True)),
                ('contrat_cargo_inicial', models.CharField(blank=True, choices=[('Supervisor 1', 'Supervisor 1'), ('Supervisor 2', 'Supervisor 2'), ('Supervisor 3', 'Supervisor 3'), ('Seguranca 1', 'Seguranca 1'), ('Seguranca 2', 'Seguranca 2'), ('Seguranca 3', 'Seguranca 3'), ('Aux Limpeza', 'Aux Limpeza'), ('Aux administrativo', 'Aux administrativo'), ('Gerente', 'Gerente'), ('Diretor', 'Diretor')], max_length=200, null=True)),
                ('contrat_vale_alim', models.BooleanField(blank=True, null=True)),
                ('contrat_vale_alim_valor', models.CharField(blank=True, max_length=20, null=True)),
                ('contrat_vale_ref', models.BooleanField(blank=True, null=True)),
                ('contrat_vale_ref_valor', models.CharField(blank=True, max_length=20, null=True)),
                ('contrat_cesta', models.BooleanField(blank=True, null=True)),
                ('contrat_cesta_valor', models.CharField(blank=True, max_length=20, null=True)),
                ('contrat_vale_comb', models.BooleanField(blank=True, null=True)),
                ('contrat_vale_comb_valor', models.CharField(blank=True, max_length=20, null=True)),
                ('contrat_vale_transp', models.BooleanField(blank=True, null=True)),
                ('contrat_vale_transp_valor', models.CharField(blank=True, max_length=20, null=True)),
                ('contrat_salario_atual', models.CharField(blank=True, max_length=20, null=True)),
                ('contrat_salario_base', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentAttachments',
            fields=[
                ('basicinfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Cliente.BasicInfo')),
                ('docscan_picture', models.ImageField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_PICTURE)),
                ('docscan_CPF', models.ImageField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_CPF)),
                ('docscan_TE', models.ImageField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_TE)),
                ('docscan_CTPS', models.ImageField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_CTPS)),
                ('docscan_reservista', models.ImageField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_RESERVISTA)),
                ('docscan_certidao_nascimento', models.ImageField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_CERTIDAONASCIMENTO)),
                ('docscan_certidao_casamento', models.ImageField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_CERTIDAOCASAMENTO)),
                ('docscan_comprovante_resid', models.ImageField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_COMPROVANTERESIDENCIA)),
                ('docscan_comprovante_escolar', models.ImageField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_COMPROVANTEESCOLAR)),
                ('docscan_CV', models.FileField(blank=True, null=True, upload_to=Cliente.utilities.funcionario_media_path_CV)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentsInfo',
            fields=[
                ('basicinfo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Cliente.BasicInfo')),
                ('docs_CTPS_numero_geral', models.IntegerField(blank=True, null=True)),
                ('docs_CTPS_numero_serie', models.IntegerField(blank=True, null=True)),
                ('docs_CTPS_UF', models.CharField(blank=True, choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, null=True)),
                ('docs_CTPS_data_emissao', models.DateField(blank=True, null=True, validators=[Cliente.utilities.validateNoFutureDates])),
                ('docs_TE_numero_geral', models.DecimalField(blank=True, decimal_places=0, max_digits=12, null=True)),
                ('docs_TE_secao', models.CharField(blank=True, max_length=10, null=True)),
                ('docs_TE_zona', models.CharField(blank=True, max_length=10, null=True)),
                ('docs_RG_numero_geral', models.DecimalField(blank=True, decimal_places=0, max_digits=11, null=True)),
                ('docs_RG_emissor', models.CharField(blank=True, max_length=5, null=True)),
                ('docs_RG_UF', models.CharField(blank=True, choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, null=True)),
                ('docs_RG_data_emissao', models.DateField(blank=True, null=True, validators=[Cliente.utilities.validateNoFutureDates])),
                ('docs_RNE_numero_geral', models.CharField(blank=True, max_length=15, null=True)),
                ('docs_RNE_emissor', models.CharField(blank=True, max_length=5, null=True)),
                ('docs_RNE_UF', models.CharField(blank=True, choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, null=True)),
                ('docs_RNE_data_emissao', models.DateField(blank=True, null=True, validators=[Cliente.utilities.validateNoFutureDates])),
                ('docs_OC_numero_geral', models.CharField(blank=True, max_length=15, null=True)),
                ('docs_OC_emissor', models.CharField(blank=True, max_length=15, null=True)),
                ('docs_OC_UF', models.CharField(blank=True, choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, null=True)),
                ('docs_OC_data_emissao', models.DateField(blank=True, null=True, validators=[Cliente.utilities.validateNoFutureDates])),
                ('docs_CNH_numero_geral', models.CharField(blank=True, max_length=15, null=True)),
                ('docs_CNH_emissor', models.CharField(blank=True, max_length=10, null=True)),
                ('docs_CNH_UF', models.CharField(blank=True, choices=[('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'), ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'), ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'), ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'), ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'), ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'), ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO')], max_length=2, null=True)),
                ('docs_CNH_data_emissao', models.DateField(blank=True, null=True, validators=[Cliente.utilities.validateNoFutureDates])),
                ('docs_CNH_categoria', models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1, null=True)),
                ('docs_CNH_data_primeira', models.DateField(blank=True, null=True, validators=[Cliente.utilities.validateNoFutureDates])),
                ('docs_CNH_data_validade', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='bankinginfo',
            name='basicinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cliente.BasicInfo'),
        ),
    ]
