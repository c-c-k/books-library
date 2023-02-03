from pathlib import Path
from secrets import choice, randbelow
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from typing import Iterable


DJANGO_SECRET_TOKEN_FORMAT = 'django-secret-{}'

class TokenGenerationError(Exception):
    pass


def _concat_token_characters(character_groups):
    return tuple(
        character
        for character_group, _ in character_groups
        for character in character_group
    )


def _gen_candidate_token(token_characters, min_token_length, max_token_length):
    token_length = (
            min_token_length
            + randbelow(max_token_length - min_token_length)
    )
    return ''.join(choice(token_characters) for _ in range(token_length))


def _is_good_token(candidate_token, character_groups):
    # Check that candidate token contains enough characters from each
    # character group.
    return all(
        sum(
            character in candidate_token for character in character_group
        ) > min_group_characters
        for character_group, min_group_characters
        in character_groups
    )


def _validate_params(min_token_length, max_token_length, character_groups):
    # Check token min/max length validity.
    if max_token_length < min_token_length:
        raise TokenGenerationError(
            f'Maximal token length({max_token_length})'
            f' is lower than minimal token length({min_token_length}).'
        )
    # Check that a minimal length token will be long enough to contain the
    # minimal number of characters required from each character group.
    min_token_characters = sum(character_group[1]
                               for character_group
                               in character_groups)
    if min_token_length < min_token_characters:
        raise TokenGenerationError(
            f'Minimal token length ({min_token_length}) is too short to '
            'contain enough characters of all specified character groups'
            f'({min_token_characters})'
        )


def gen_secret_token(
        min_token_length: int = 50,
        max_token_length: int = 60,
        character_groups: Iterable[tuple[str, int]] = (
                (ascii_lowercase, 4),
                (ascii_uppercase, 4),
                (digits, 4),
                (punctuation, 4)
        ),
        max_token_generation_attempts: int = 100,
):
    """

    :param min_token_length: Minimal required length of secret token.
    :param max_token_length: Maximal acceptable length of secret token.
    :param character_groups: A Iterable of tuples of the structure
        (<valid token characters in group>,
         <minimal number of required characters from group>)
    :param max_token_generation_attempts: Safety param to prevent the
        function from getting practically stuck in an infinite loop while
        trying to generate a secret token due to low/impossible odds of
        generating a token answering the given parameters.
    :return: A secret token answering the given parameters.
    """
    _validate_params(min_token_length, max_token_length, character_groups)
    token_characters = _concat_token_characters(character_groups)
    for generation_attempt in range(max_token_generation_attempts):
        candidate_token = _gen_candidate_token(
            token_characters, min_token_length, max_token_length)
        if _is_good_token(candidate_token, character_groups):
            return candidate_token
    else:
        raise TokenGenerationError(
            'Failed to generate secret token after '
            f'{max_token_generation_attempts} attempts.'
        )


def create_new_django_secret_token(token_path):
    secret_token = DJANGO_SECRET_TOKEN_FORMAT.format(gen_secret_token())
    token_path.write_text(secret_token)


def get_django_secret_token(token_path: Path):
    if not token_path.exists():
        create_new_django_secret_token(token_path)
    return token_path.read_text()
