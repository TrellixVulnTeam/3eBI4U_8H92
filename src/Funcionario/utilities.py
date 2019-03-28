from datetime import date
# CPF Validator That Checks Verification Digits
def validateCPF(value_as_string, *args, **kwargs):
    CPF = [int(x) for x in list(str(value_as_string))]
    CPF_root, CPF_VD = CPF[:9], CPF[-2:]
    VD_1, VD_2 = 0, 0
    
    VD_1 = sum([(CPF_root[len(CPF_root) - i + 1] * i) for i in range(10, 1, -1)])
    
    VD_1 = 0 if VD_1 % 11 == 0 or VD_1 % 11 == 1 else (11 - (VD_1 % 11))

    VD_2 = sum([(VD_1 * i) if i == 2 else VD_2 + (CPF_root[len(CPF_root) - i + 2] * i) for i in range(11, 1, -1)])

    VD_2 = 0 if VD_2 % 11 == 0 or VD_2 % 11 == 1 else (11 - (VD_2 % 11))

    return True if (CPF_VD[0], CPF_VD[1]) == (VD_1, VD_2) else False

# RG Validator That Checks Verification Digit (Works for Sao Paulo, other states are uncertain due to ambiguous RG nature)
def validateRG(value_as_string, *args, **kwargs):
    CPF = [int(x) for x in list(str(value_as_string))]
    CPF_root, CPF_VD = CPF[-2], CPF[-1]
    VD = 0
    VD = 11 - (sum([CPF_root[i - 2] * i for i in range(2, 10)]) % 11)
    
    return True if CPF_VD == VD else False

# Form Conditions
def estrangeiro_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('Basic Info') or {}
    return cleaned_data.get('estrangeiro', True)
def outro_emprego_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('Basic Info') or {}
    return cleaned_data.get('outro_emprego', True)
def estagiario_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('Basic Info') or {}
    return cleaned_data.get('estagiario', True)
def deficiente_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('Basic Info') or {}
    return cleaned_data.get('deficiente', True)

# Media Files Path Creating Function - file will be uploaded to MEDIA_ROOT/Funcionario/<rd_int>_user_<id>/<filename>
def user_media_path_CPF(instance, filename):
    return 'user_{0}/CPF_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_TE(instance, filename):
    return 'user_{0}/TE_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_CTPS(instance, filename):
    return 'user_{0}/CTPS_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_RESERVISTA(instance, filename):
    return 'user_{0}/RESERVISTA_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_CERTIDAONASCIMENTO(instance, filename):
    return 'user_{0}/CERTIDAONASCIMENTO_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_CERTIDAOCASAMENTO(instance, filename):
    return 'user_{0}/CERTIDAOCASAMENTO_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_COMPROVANTERESIDENCIA(instance, filename):
    return 'user_{0}/COMPROVANTERESIDENCIA_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_COMPROVANTEESCOLAR(instance, filename):
    return 'user_{0}/COMPROVANTEESCOLAR_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_CV(instance, filename):
    return 'user_{0}/CV_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_VACINACAO(instance, filename):
    return 'user_{0}/VACINACAO_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path_RG(instance, filename):
    return 'user_{0}/RG_{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 
def user_media_path(instance, filename):
    return 'user_{0}/{1}_{2}'.format(
        instance.basicinfo.id,
        date.today(),
        filename
        ) 







