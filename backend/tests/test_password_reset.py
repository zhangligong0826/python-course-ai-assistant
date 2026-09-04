import hashlib

from open_webui.utils.password_reset import build_reset_url, hash_reset_token


def test_reset_token_is_stored_as_sha256_digest():
    raw = 'secret-reset-token'

    digest = hash_reset_token(raw)

    assert digest == hashlib.sha256(raw.encode()).hexdigest()
    assert raw not in digest


def test_reset_url_encodes_token_and_uses_configured_origin():
    assert build_reset_url('https://aiops.nankai.edu.cn/', 'a+b/c=') == (
        'https://aiops.nankai.edu.cn/auth/reset-password?token=a%2Bb%2Fc%3D'
    )
