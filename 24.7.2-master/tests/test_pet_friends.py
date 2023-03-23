from api import PetFriends
from settings import *

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_mail, password=valid_pass):
    """Получение токена авторизации"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    print(result)


def test_get_all_pets_with_valid_key(filter=''):
    """Получение списка питомцев"""
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_create_new_pet(name=valid_name, animal_type=valid_animal_type, age=valid_age):
    """Создание питомца"""
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == valid_name


def test_update_info_about_existing_pet(name=new_valid_name, animal_type=new_valid_animal_type, age=new_valid_age):
    """Обновление данных ранее созданного питомца"""
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_about_existing_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == new_valid_name
    else:
        raise Exception('No pet found')


def test_delete_recently_updated_pet():
    """Удаление питомца"""
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_positive(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets


def test_get_api_key_for_invalid_password(email=valid_mail, password=invalid_pass):
    """Получение токена авторизации с невалидными паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_api_key_for_invalid_mail(email=invalid_mail, password=valid_pass):
    """Получение токена авторизации с использованием невалидной почты"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print(result)


def test_create_new_pet_without_any_data(name='', animal_type='', age=''):
    """Создание питомца без передачи обязательных параматров имени, типа и возраста"""
    _, auth_key = pf.get_api_key(valid_mail, valid_pass)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    if status == 200:
        raise Exception('Here is a bug')
    else:
        assert status == 400


def test_create_new_pet_with_invalid_authority_key(name='', animal_type='', age=''):
    """Создание питомца без передачи обязательных параматров имени, типа и возраста"""
    auth_key = invalid_token
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    if status == 200:
        raise Exception('Here is a bug')
    else:
        assert status == 403


def test_get_all_pets_with_invalid_key(filter=''):
    """Получение списка питомцев c невалидным токеном авторизации"""
    auth_key = invalid_token
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403