import random

from ord_mediascout_client import CreatePlatformWebApiDto, PlatformType


# НЕ работает в режиме "get or create", только "create" с новым url, потому url и название генерятся
def test_create_platform(client):
    rnd = random.randrange(111, 999)
    request_data = CreatePlatformWebApiDto(
        name='Test Platform {}'.format(rnd),
        type=PlatformType.Site,
        url='http://www.testplatform{}.ru/'.format(rnd),
        isOwner=False,
    )

    response_data = client.create_platform(request_data)

    assert response_data.id is not None
