# from stl_dsa.users.forms import UserCreationForm


# def test_clean_username(user):
#     # A user with proto_user params does not exist yet.

#     form = UserCreationForm(
#         {
#             "email": user.email,
#             "password1": user._password,
#             "password2": user._password,
#         }
#     )

# assert form.is_valid()
# assert form.clean_username() == user.email

# Creating a user.
# form.save()

# # The user with proto_user params already exists,
# # hence cannot be created.
# form = UserCreationForm(
#     {
#         "email": proto_user.email,
#         "password1": proto_user._password,
#         "password2": proto_user._password,
#     }
# )

# assert not form.is_valid()
# assert len(form.errors) == 1
# assert "email" in form.errors
