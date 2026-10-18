from django.contrib import admin

from web.models.character import Character
# from django.contrib.auth.models import User


from web.models.user import UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',) # 逗号不要删！！！

# Register your models here.

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     # 👇 关键：把 create_time 加到列表显示
#     list_display = ('id', 'username', 'create_time')
#
#     readonly_fields = ('create_time',)

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    raw_id_fields = ('author', )
