def test_is_member(user, member):
    assert member.is_member
    assert not user.is_member
