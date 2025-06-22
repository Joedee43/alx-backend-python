from django.contrib import admin
from .models import Message

class ReplyInline(admin.StackedInline):
    model = Message
    fk_name = 'parent_message'
    extra = 0
    show_change_link = True
    fields = ('sender', 'receiver', 'content', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'truncated_content', 'sender', 'receiver', 'parent_message', 'timestamp')
    list_select_related = ('sender', 'receiver', 'parent_message')
    inlines = [ReplyInline]
    search_fields = ('content', 'sender__username', 'receiver__username')
    
    def truncated_content(self, obj):
        return obj.content[:75] + '...' if len(obj.content) > 75 else obj.content
    truncated_content.short_description = 'Content'