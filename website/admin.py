from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User
from .models import Department
from .models import Unit
from .models import Post
from .models import Role
from .models import Document
from .models import File
from .models import Resolution
from .models import Execution
from .models import Change
from .models import Notification
from .models import Meeting

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Unit)
admin.site.register(Post)
admin.site.register(Role)
admin.site.register(Document)
admin.site.register(File)
admin.site.register(Resolution)
admin.site.register(Execution)
admin.site.register(Change)
admin.site.register(Notification)
admin.site.register(Meeting)

