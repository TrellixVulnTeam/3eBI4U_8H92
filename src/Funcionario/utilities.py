from datetime import date
from django.core.exceptions import ValidationError
import re

# VALIDATORS ---------------------------------------------------------------------------------------------------------------------

# CNPJ Validator That Checks Verification Digits
def validateCNPJ(value):
        CNPJ = re.sub(r'[\-\.\/\\]', '', value)
        CNPJ = [int(x) for x in list(str(CNPJ))]
        CNPJ_root, CNPJ_VD, weights = CNPJ[:12], CNPJ[-2:], [5,4,3,2,9,8,7,6,5,4,3,2]

        CNPJ_weighted = sum([x*y for x, y in zip(CNPJ_root, weights)]) % 11

        VD_1 = 0 if CNPJ_weighted < 2 else (11 - CNPJ_weighted)

        CNPJ_weighted = sum([x*y for x, y in zip(CNPJ_root + [VD_1], [6] + weights)]) % 11

        VD_2 = 0 if CNPJ_weighted < 2 else (11 - CNPJ_weighted)

        return value if (VD_1, VD_2) == (CNPJ_VD[0], CNPJ_VD[1]) else ValidationError('CNPJ Invalido')

# CPF Validator That Checks Verification Digits
def validateCPF(value):
        
        CPF = re.sub(r'[\-\.\/\\]', '', value)
        CPF = [int(x) for x in list(str(CPF))]
        CPF_root, CPF_VD, weights = CPF[:9], CPF[-2:], [10, 9, 8, 7, 6, 5, 4, 3, 2]

        CPF_weighted = sum([x*y for x, y in zip(CPF_root, weights)]) % 11

        VD_1 = 0 if CPF_weighted < 2 else (11 - CPF_weighted)

        CPF_weighted = sum([x*y for x, y in zip(CPF_root + [VD_1], [11] + weights)]) % 11

        VD_2 = 0 if CPF_weighted < 2 else (11 - CPF_weighted)

        return value if (VD_1, VD_2) == (CPF_VD[0], CPF_VD[1]) else ValidationError('CNPJ Invalido')

        

# RG Validator That Checks Verification Digit (Works for Sao Paulo, other states are uncertain due to ambiguous RG nature)
def validateRG(value_as_string, *args, **kwargs):
        CPF = [int(x) for x in list(str(value_as_string))]
        CPF_root, CPF_VD = CPF[-2], CPF[-1]
        VD = 0
        VD = 11 - (sum([CPF_root[i - 2] * i for i in range(2, 10)]) % 11)

        return True if CPF_VD == VD else False

# FORM CONDITIONS -----------------------------------------------------------------------------------------------------------------
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


# MEDIA PATHS ---------------------------------------------------------------------------------------------------------------------
# Media Files Path Creating Functions - file will be uploaded to MEDIA_ROOT/Funcionario/funcionario_<BASICINFO.ID>/<DOCTYPE>_<DATE>_<FILENAME>

def funcionario_media_path_CPF(instance, filename):
        return 'funcionario_{0}/CPF_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_TE(instance, filename):
        return 'funcionario_{0}/TE_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_CTPS(instance, filename):
        return 'funcionario_{0}/CTPS_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_RESERVISTA(instance, filename):
        return 'funcionario_{0}/RESERVISTA_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_CERTIDAONASCIMENTO(instance, filename):
        return 'funcionario_{0}/CERTIDAONASCIMENTO_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_CERTIDAOCASAMENTO(instance, filename):
        return 'funcionario_{0}/CERTIDAOCASAMENTO_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_COMPROVANTERESIDENCIA(instance, filename):
        return 'funcionario_{0}/COMPROVANTERESIDENCIA_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_COMPROVANTEESCOLAR(instance, filename):
        return 'funcionario_{0}/COMPROVANTEESCOLAR_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_CV(instance, filename):
        return 'funcionario_{0}/CV_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_VACINACAO(instance, filename):
        return 'funcionario_{0}/VACINACAO_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_RG(instance, filename):
        return 'funcionario_{0}/RG_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path_PICTURE(instance, filename):
        return 'funcionario_{0}/PICTURE_{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 
def funcionario_media_path(instance, filename):
        return 'funcionario_{0}/{1}_{2}'.format(
                instance.basicinfo.id,
                date.today(),
                filename
        ) 