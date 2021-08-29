def test_is_member(user, member):
    assert not user.is_member
    assert member.is_member
