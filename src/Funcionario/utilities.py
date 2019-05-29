from datetime import date
from django.core.exceptions import ValidationError
import re

# VALIDATORS ---------------------------------------------------------------------------------------------------------------------

# CEP Validator That Prevents Number of Charactes Different Than 9
def validateCEP(value):
        if len(value) != 9:
                return ValidationError('CEP Inválido')
        return None

# CNPJ Validator That Prevents Invalid Verification Digits
def validateCNPJ(value):
        CNPJ = re.sub(r'[\-\.\/\\]', '', value)
        CNPJ = [int(x) for x in list(str(CNPJ))]
        CNPJ_root, CNPJ_VD, weights = CNPJ[:12], CNPJ[-2:], [5,4,3,2,9,8,7,6,5,4,3,2]

        CNPJ_weighted = sum([x*y for x, y in zip(CNPJ_root, weights)]) % 11

        VD_1 = 0 if CNPJ_weighted < 2 else (11 - CNPJ_weighted)

        CNPJ_weighted = sum([x*y for x, y in zip(CNPJ_root + [VD_1], [6] + weights)]) % 11

        VD_2 = 0 if CNPJ_weighted < 2 else (11 - CNPJ_weighted)

        if ((VD_1, VD_2) != (CNPJ_VD[0], CNPJ_VD[1])) or len(value) < 14:
                raise ValidationError('CNPJ Inválido')

        return None

# CPF Validator That Prevents Invalid Verification Digits
def validateCPF(value):

        CPF = re.sub(r'[\-\.\/\\]', '', value)
        CPF = [int(x) for x in list(str(CPF))]
        CPF_root, CPF_VD, weights = CPF[:9], CPF[-2:], [10, 9, 8, 7, 6, 5, 4, 3, 2]

        CPF_weighted = sum([x*y for x, y in zip(CPF_root, weights)]) % 11

        VD_1 = 0 if CPF_weighted < 2 else (11 - CPF_weighted)

        CPF_weighted = sum([x*y for x, y in zip(CPF_root + [VD_1], [11] + weights)]) % 11

        VD_2 = 0 if CPF_weighted < 2 else (11 - CPF_weighted)

        if ((VD_1, VD_2) != (CPF_VD[0], CPF_VD[1])) or len(value) < 11:
                raise ValidationError('CPF Inválido')

        return None

# Date Validator That Prevents Future Dates
def validateNoFutureDates(value):

        if value > date.today():
                raise ValidationError('Datas Futúras São Inválidas Neste Campo')





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
        return 'funcionario_{0}/CPF-CNH_{1}_{2}'.format(
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
        print('got called')
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