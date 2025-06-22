from django.contrib import admin
from .models import Message, MessageHistory

class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('edited_at', 'edited_by', 'content')
    can_delete = False

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'edited', 'last_edited')
    list_filter = ('edited', 'timestamp')
    inlines = [MessageHistoryInline]
    readonly_fields = ('timestamp',)

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'edited_at', 'edited_by')
    list_filter = ('edited_at',)
    readonly_fields = ('message', 'edited_at', 'edited_by', 'content')