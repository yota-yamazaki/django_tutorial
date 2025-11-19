from django.contrib import admin

class PollsAdminSite(admin.AdminSite):
    site_header = "投票管理"

class HeadOfficeAdminSite(admin.AdminSite):
    site_header = "本社管理"

polls_admin_site = PollsAdminSite(name="polls_admin")
head_office_admin_site = HeadOfficeAdminSite(name="head_office_admin")

